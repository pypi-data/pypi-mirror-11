# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Baruwa - Web 2.0 MailScanner front-end.
# Copyright (C) 2010-2015  Andrew Colin Kissa <andrew@topdog.za.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"Domains controller"

import socket
import struct
import logging

import arrow

from urlparse import urlparse

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import redirect, abort
from pylons.i18n.translation import _
from webhelpers import paginate
from celery.result import AsyncResult
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError, DataError
from repoze.what.predicates import All, not_anonymous
from sphinxapi import SphinxClient, SPH_MATCH_EXTENDED2
from repoze.what.plugins.pylonshq import ActionProtector, ControllerProtector

from baruwa.lib.base import BaseController
from baruwa.lib.helpers import flash, flash_info, flash_alert
from baruwa.lib.auth.predicates import OnlyAdminUsers, OnlySuperUsers
from baruwa.lib.auth.predicates import OwnsDomain
from baruwa.lib.caching_query import FromCache
from baruwa.lib.query import get_dom_crcs
from baruwa.lib.backend import update_domain_backend
from baruwa.lib.audit import audit_log
from baruwa.lib.query import clean_sphinx_q, restore_sphinx_q
from baruwa.lib.misc import check_num_param
from baruwa.lib.misc import convert_dom_to_json, extract_sphinx_opts
from baruwa.tasks.domains import exportdomains, test_smtp_server
from baruwa.model.meta import Session
from baruwa.model.auth import LDAPSettings, RadiusSettings
from baruwa.model.accounts import domain_owners
from baruwa.model.accounts import organizations_admins as oa
from baruwa.model.domains import DomainAlias
from baruwa.model.domains import Domain, DeliveryServer, AuthServer
from baruwa.forms.domains import DelDomainAlias, EditDomainForm
from baruwa.forms.domains import BulkDelDomains, AddLDAPSettingsForm
from baruwa.forms.domains import AddDomainForm, AddDeliveryServerForm
from baruwa.forms.domains import AddAuthForm, AUTH_PROTOCOLS, EditDomainAlias
from baruwa.forms.domains import AddDomainAlias, AddRadiusSettingsForm
from baruwa.lib.audit.msgs import domains as auditmsgs
from baruwa.lib.api import create_domain, domain_update_form, update_domain, \
    domain_update_if_changed, delete_domain, create_destination, \
    update_destination, update_if_changed, delete_destination, \
    create_auth, edit_auth, delete_auth, auth_update_if_changed, \
    create_alias, edit_alias, delete_alias, get_organizations
from baruwa.lib.backend import update_ldap_backend


log = logging.getLogger(__name__)


@ControllerProtector(All(not_anonymous(), OnlyAdminUsers()))
class DomainsController(BaseController):
    "Domains controller"
    def __before__(self):
        "set context"
        BaseController.__before__(self)
        if self.identity:
            c.user = self.identity['user']
        else:
            c.user = None
        c.selectedtab = 'domains'

    def _get_server(self, destinationid):
        "utility"
        try:
            cachekey = u'deliveryserver-%s' % destinationid
            qry = Session.query(DeliveryServer)\
                    .filter(DeliveryServer.id == destinationid)\
                    .options(FromCache('sql_cache_med', cachekey))
            if self.invalidate:
                qry.invalidate()
            server = qry.one()
        except NoResultFound:
            server = None
        return server

    def _get_authserver(self, authid):
        "Get an auth server"
        try:
            cachekey = u'authserver-%s' % authid
            qry = Session.query(AuthServer).filter(AuthServer.id == authid)\
                .options(FromCache('sql_cache_med', cachekey))
            if self.invalidate:
                qry.invalidate()
            server = qry.one()
        except NoResultFound:
            server = None
        return server

    def _get_alias(self, aliasid):
        "Get a domain alias"
        try:
            cachekey = u'domainalias-%s' % aliasid
            qry = Session.query(DomainAlias).filter(DomainAlias.id == aliasid)\
                .options(FromCache('sql_cache_med', cachekey))
            if self.invalidate:
                qry.invalidate()
            alias = qry.one()
        except NoResultFound:
            alias = None
        return alias

    def index(self, page=1, orgid=None, format=None):
        "Browse domains"
        num_items = session.get('domains_num_items', 10)
        c.form = BulkDelDomains(request.POST, csrf_context=session)
        if request.method == 'POST':
            if c.form.domainid.data and c.form.whatdo.data == 'disable':
                Session.query(Domain).filter(
                        Domain.id.in_(c.form.domainid.data)
                ).update({'status': False}, synchronize_session='fetch')
                Session.commit()
            if c.form.domainid.data and c.form.whatdo.data == 'enable':
                Session.query(Domain).filter(
                        Domain.id.in_(c.form.domainid.data)
                ).update({'status': True}, synchronize_session='fetch')
                Session.commit()
            if c.form.domainid.data and c.form.whatdo.data == 'delete':
                session['bulk_domain_delete'] = c.form.domainid.data
                session.save()
                # redirect for confirmation
                redirect(url('domains-confirm-delete'))
        domains = Session.query(Domain).options(
                joinedload(Domain.organizations))
        domcount = Session.query(Domain.id)

        if orgid and c.user.is_superadmin:
            domains = domains.join(domain_owners).filter(
                        domain_owners.c.organization_id == orgid)
            domcount = domcount.join(domain_owners).filter(
                        domain_owners.c.organization_id == orgid)
        if c.user.is_domain_admin:
            domains = domains.join(domain_owners,
                    (oa, domain_owners.c.organization_id ==
                        oa.c.organization_id))\
                    .filter(oa.c.user_id == c.user.id)
            domcount = domcount.join(domain_owners,
                    (oa, domain_owners.c.organization_id ==
                        oa.c.organization_id))\
                    .filter(oa.c.user_id == c.user.id)

        pages = paginate.Page(domains, page=int(page),
                                items_per_page=num_items,
                                item_count=domcount.count())
        if format == 'json':
            response.headers['Content-Type'] = 'application/json'
            data = convert_dom_to_json(pages, orgid)
            return data

        c.orgid = orgid
        c.page = pages
        return self.render('/domains/index.html')

    def search(self, format=None):
        "Search for domains"
        total_found = 0
        search_time = 0
        num_items = session.get('domains_num_items', 10)
        qry = request.GET.get('q', '')
        org = request.GET.get('o', None)
        page = int(request.GET.get('p', 1))
        # if q:
        kwds = {'presliced_list': True}
        conn = SphinxClient()
        sphinxopts = extract_sphinx_opts(config['sphinx.url'])
        conn.SetServer(sphinxopts.get('host', '127.0.0.1'))
        conn.SetMatchMode(SPH_MATCH_EXTENDED2)
        if page == 1:
            conn.SetLimits(0, num_items, 500)
        else:
            offset = (page - 1) * num_items
            conn.SetLimits(offset, num_items, 500)
        if org:
            conn.SetFilter('orgs', [int(org)])
        if c.user.is_domain_admin:
            crcs = get_dom_crcs(Session, c.user)
            conn.SetFilter('domain_name', crcs)
        qry = clean_sphinx_q(qry)
        try:
            results = conn.Query(qry, 'domains, domains_rt')
        except (socket.timeout, struct.error):
            redirect(request.path_qs)
        qry = restore_sphinx_q(qry)
        if results and results['matches']:
            ids = [hit['id'] for hit in results['matches']]
            domains = Session.query(Domain)\
                    .options(joinedload('organizations'))\
                    .filter(Domain.id.in_(ids))\
                    .all()
            total_found = results['total_found']
            search_time = results['time']
            domaincount = total_found
        else:
            domains = []
            domaincount = 0

        c.page = paginate.Page(domains, page=page,
                                items_per_page=num_items,
                                item_count=domaincount,
                                **kwds)
        c.q = qry
        c.org = org
        c.total_found = total_found
        c.search_time = search_time
        return self.render('/domains/searchresults.html')

    @ActionProtector(OwnsDomain())
    def detail(self, domainid):
        "Domain details"
        domain = self._get_domain(domainid)
        if not domain:
            abort(404)
        c.domain = domain
        return self.render('/domains/detail.html')

    @ActionProtector(OnlySuperUsers())
    def add(self, orgid=None):
        "Add a domain"
        c.form = AddDomainForm(request.POST, csrf_context=session)
        c.form.organizations.query = get_organizations(orgid)
        if request.method == 'POST' and c.form.validate():
            try:
                domain = create_domain(c.form, c.user,
                            request.host, request.remote_addr)
                try:
                    from baruwa.tasks.invite import create_mx_records
                    create_mx_records.apply_async(args=[domain.name])
                except ImportError:
                    pass
                flash(_('The domain: %(dom)s has been created') %
                    dict(dom=domain.name))
                redirect(url(controller='domains'))
            except IntegrityError:
                Session.rollback()
                msg = _('The domain name %(dom)s already exists') % \
                        dict(dom=domain.name)
                flash_alert(msg)
                log.info(msg)

        return self.render('/domains/new.html')

    @ActionProtector(OwnsDomain())
    def edit(self, domainid):
        "Edit a domain"
        domain = self._get_domain(domainid)
        if not domain:
            abort(404)

        c.id = domainid
        c.form = domain_update_form(c.user, request.POST, domain,
                                get_organizations, session)
        if request.method == 'POST' and c.form.validate():
            kwd = dict(domainid=domain.id)
            if domain_update_if_changed(c.form, domain):
                try:
                    update_domain(domain, c.user, request.host,
                                    request.remote_addr)
                    flash(_('The domain: %(dom)s has been updated') %
                        dict(dom=domain.name))
                    kwd['uc'] = 1
                except IntegrityError:
                    Session.rollback()
                    msg = _('The domain %(dom)s could not be updated') % \
                            dict(dom=domain.name)
                    flash(msg)
                    log.info(msg)
            else:
                msg = _('No changes were made to the domain')
                flash_info(msg)
                log.info(msg)
            redirect(url('domain-detail', **kwd))
        return self.render('/domains/edit.html')

    @ActionProtector(OwnsDomain())
    def delete(self, domainid):
        "Delete a domain"
        domain = self._get_domain(domainid)
        if not domain:
            abort(404)

        c.id = domainid
        c.form = EditDomainForm(request.POST, domain, csrf_context=session)
        del c.form.organizations
        if request.method == 'POST':
            if c.form.validate():
                delete_domain(domain, c.user, request.host,
                                request.remote_addr)
                flash(_('The domain has been deleted'))
                redirect(url(controller='domains'))
        else:
            flash(_('The domain: %(name)s and all associated data will'
                ' be deleted, This action cannot be reversed.') %
                dict(name=domain.name))
        return self.render('/domains/delete.html')

    def confirm_delete(self):
        "Confirm bulk delete of domains"
        domainids = session.get('bulk_domain_delete', [])
        if not domainids:
            redirect(url(controller='domains', action='index'))

        num_items = 10
        if len(domainids) > num_items and len(domainids) <= 20:
            num_items = 20
        if len(domainids) > num_items and len(domainids) <= 50:
            num_items = 50
        if len(domainids) > num_items and len(domainids) <= 100:
            num_items = 100

        domains = Session.query(Domain).filter(Domain.id.in_(domainids))\
                    .options(joinedload('organizations'))
        domcount = Session.query(Domain.id).filter(Domain.id.in_(domainids))

        if c.user.is_domain_admin:
            domains = domains.join(domain_owners,
                        (oa,
                        domain_owners.c.organization_id ==
                        oa.c.organization_id))\
                        .filter(oa.c.user_id == c.user.id)
            domcount = domcount.join(domain_owners,
                        (oa, domain_owners.c.organization_id ==
                        oa.c.organization_id))\
                        .filter(oa.c.user_id == c.user.id)

        if request.method == 'POST':
            tasks = []
            for domain in domains.all():
                info = auditmsgs.DELETEDOMAIN_MSG % dict(d=domain.name)
                tasks.append((c.user.username,
                        4, unicode(info), request.host,
                        request.remote_addr,
                        arrow.utcnow().datetime))
                Session.delete(domain)
            Session.commit()
            del session['bulk_domain_delete']
            update_domain_backend(None, True)
            session.save()
            for task in tasks:
                audit_log(*task)
            flash(_('The domains have been deleted'))
            redirect(url(controller='domains'))
        else:
            flash(_('The following domains are about to be deleted,'
                    ' this action is not reversible, Do you wish to'
                    ' continue ?'))

        try:
            c.page = paginate.Page(domains, page=1,
                                    items_per_page=num_items,
                                    item_count=domcount.count())
        except DataError, error:
            msg = _('An error occured try again')
            flash_alert(msg)
            msg = _('An error occured try again: %s' % error)
            log.info(msg)
            redirect(url(controller='domains', action='index'))
        return self.render('/domains/confirmbulkdel.html')

    @ActionProtector(OwnsDomain())
    def adddestination(self, domainid):
        "Add a destination server"
        domain = self._get_domain(domainid)
        if not domain:
            abort(404)

        c.id = domainid
        c.form = AddDeliveryServerForm(request.POST, csrf_context=session)
        if request.method == 'POST' and c.form.validate():
            server = DeliveryServer()
            server.from_form(c.form)
            try:
                create_destination(domain, server, c.user,
                                request.host, request.remote_addr)
                flash(_('The destination server has been created'))
                redirect(url(controller='domains', action='detail',
                        domainid=domain.id))
            except IntegrityError:
                Session.rollback()
                msg = _('The destination server %(dest)s already exists ') % \
                        dict(dest=server.address)
                flash_alert(msg)
                log.info(msg)
        return self.render('/domains/adddestination.html')

    @ActionProtector(OwnsDomain())
    def editdestination(self, destinationid):
        "Edit destination server"
        server = self._get_server(destinationid)
        if not server:
            abort(404)
        c.form = AddDeliveryServerForm(request.POST,
                                        server,
                                        csrf_context=session)
        if request.method == 'POST' and c.form.validate():
            kwd = dict(domainid=server.domain_id)
            if update_if_changed(c.form, server):
                try:
                    update_destination(server, c.user, request.host,
                                        request.remote_addr)
                    self.invalidate = 1
                    self._get_server(destinationid)
                    kwd['uc'] = 1
                    flash(_('The destination server has been updated'))
                    redirect(url('domain-detail', **kwd))
                except IntegrityError:
                    Session.rollback()
                    msg = _('The update failed')
                    flash_alert(msg)
                    log.info(msg)
            else:
                msg = _('No changes were made to the destination server')
                flash_info(msg)
                log.info(msg)
                redirect(url('domain-detail', **kwd))
        c.id = destinationid
        c.domainid = server.domain_id
        return self.render('/domains/editdestination.html')

    @ActionProtector(OwnsDomain())
    def testdestination(self, destinationid):
        "Test mail destination server"
        server = self._get_server(destinationid)
        if not server:
            abort(404)

        taskid = request.GET.get('taskid', None)
        if not taskid:
            to_addr = 'postmaster@%s' % server.domains.name
            task = test_smtp_server.apply_async(args=[
                                    server.address,
                                    server.port,
                                    '<>',
                                    to_addr,
                                    server.id,
                                    3])
            taskid = task.task_id
            if 'taskids' not in session:
                session['taskids'] = []
            session['taskids'].append(taskid)
            session['testdest-count'] = 1
            session.save()
            redirect(url.current(taskid=taskid))
        else:
            result = AsyncResult(taskid)
            if result is None or taskid not in session['taskids']:
                flash(_('The connection test failed try again later'))
                redirect(url('domain-detail', domainid=server.domain_id))
            if result.ready():
                if ('smtp' in result.result and 'ping' in result.result
                    and result.result['smtp'] and result.result['ping']):
                    msg = _('The server: %s is up and accepting mail from us'
                            % server.address)
                    flash(msg)
                    log.info(msg)
                else:
                    if 'ping' in result.result['errors']:
                        errors = result.result['errors']['ping']
                    else:
                        errors = result.result['errors']['smtp']
                    msg = _('The server: %s is not accepting mail from us: %s') \
                            % (server.address, errors)
                    flash(msg)
                    log.info(msg)
                redirect(url('domain-detail', domainid=server.domain_id))
            else:
                try:
                    session['testdest-count'] += 1
                except KeyError:
                    session['testdest-count'] = 1
                session.save()
                if (session['testdest-count'] >= 10 and
                    result.state in ['PENDING', 'RETRY', 'FAILURE']):
                    result.revoke()
                    del session['testdest-count']
                    session.save()
                    msg = 'Failed to initialize backend, try again later'
                    flash_alert(msg)
                    log.info(msg)
                    redirect(url('domain-detail', domainid=server.domain_id))

        c.server = server
        c.domainid = server.domain_id
        c.taskid = taskid
        c.finished = False
        return self.render('/domains/testdestination.html')

    @ActionProtector(OwnsDomain())
    def deletedestination(self, destinationid):
        "Delete destination server"
        server = self._get_server(destinationid)
        if not server:
            abort(404)
        c.form = AddDeliveryServerForm(request.POST,
                                        server,
                                        csrf_context=session)
        if request.method == 'POST':
            if c.form.validate():
                domainid = delete_destination(server, c.user,
                                    request.host, request.remote_addr)
                flash(_('The destination server has been deleted'))
                redirect(url('domain-detail', domainid=domainid))
        else:
            flash(_('The destination server: %(s)s will be deleted,'
                ' This action is not reversible') % dict(s=server.address))
        c.id = destinationid
        c.domainid = server.domain_id
        return self.render('/domains/deletedestination.html')

    @ActionProtector(OwnsDomain())
    def add_auth(self, domainid):
        "Add auth server"
        domain = self._get_domain(domainid)
        if not domain:
            abort(404)
        c.form = AddAuthForm(request.POST, csrf_context=session)
        if request.method == 'POST' and c.form.validate():
            server = AuthServer()
            server.from_form(c.form)
            try:
                create_auth(domain, server, c.user,
                            request.host, request.remote_addr)
                flash(_('The authentication settings have been created'))
                redirect(url(controller='domains', action='detail',
                        domainid=domain.id))
            except IntegrityError:
                Session.rollback()
                auth = dict(AUTH_PROTOCOLS)[str(server.protocol)]
                msg = _('The host %(dest)s already configured for %(auth)s '
                        'authentication for this domain') % \
                        dict(dest=server.address, auth=auth)
                flash_alert(msg)
                log.info(msg)
        c.domainid = domainid
        c.domainname = domain.name
        return self.render('/domains/addauth.html')

    @ActionProtector(OwnsDomain())
    def edit_auth(self, authid):
        "Edit auth server"
        server = self._get_authserver(authid)
        if not server:
            abort(404)
        c.form = AddAuthForm(request.POST, server, csrf_context=session)
        if request.method == 'POST' and c.form.validate():
            kwd = dict(domainid=server.domain_id)
            if auth_update_if_changed(c.form, server):
                try:
                    edit_auth(server, c.user, request.host,
                            request.remote_addr)
                    flash(_('The authentication settings have been updated'))
                    self.invalidate = 1
                    self._get_authserver(authid)
                    kwd['uc'] = 1
                    redirect(url('domain-detail', **kwd))
                except IntegrityError:
                    Session.rollback()
                    msg = _('The authentication settings update failed')
                    flash_alert(msg)
                    log.info(msg)
            else:
                msg = _('No changes were made to the authentication settings')
                flash_info(msg)
                log.info(msg)
                redirect(url('domain-detail', **kwd))
        c.domainid = server.domains.id
        c.domainname = server.domains.name
        c.authid = authid
        return self.render('/domains/editauth.html')

    @ActionProtector(OwnsDomain())
    def delete_auth(self, authid):
        "Delete auth server"
        server = self._get_authserver(authid)
        if not server:
            abort(404)
        c.form = AddAuthForm(request.POST, server, csrf_context=session)
        if request.method == 'POST' and c.form.validate():
            domainid = server.domains.id
            delete_auth(server, c.user, request.host, request.remote_addr)
            flash(_('The authentication settings have been deleted'))
            redirect(url('domain-detail', domainid=domainid))
        else:
            flash(_('The authentication server: %(s)s will be deleted,'
                ' This action is not reversible') % dict(s=server.address))
        c.domainid = server.domains.id
        c.domainname = server.domains.name
        c.authid = authid
        return self.render('/domains/deleteauth.html')

    @ActionProtector(OwnsDomain())
    def auth_settings(self, domainid, sid, proto=5):
        "Authentication settings"
        domain = self._get_domain(domainid)
        if not domain:
            abort(404)
        try:
            protocols = {'4': 'radius',
                        '5': 'ldap',
                        '6': 'yubikey',
                        '7': 'oauth'}
            protocol = protocols[proto]
            server = Session.query(AuthServer)\
                    .filter(AuthServer.id == sid)\
                    .filter(AuthServer.domain_id == domainid)\
                    .filter(AuthServer.protocol == proto).one()
        except KeyError:
            msg = _('The protocol supplied does not use extra settings')
            flash_alert(msg)
            log.info(msg)
            redirect(url(controller='domains',
                    action='detail',
                    domainid=domain.id))
        except NoResultFound:
            msg = _('Please add an authentication server for the '
                    '%(proto)s protocol Before attempting to configure '
                    'the %(proto)s settings') % dict(proto=proto)
            flash_alert(msg)
            log.info(msg)
            redirect(url(controller='domains',
                    action='detail',
                    domainid=domain.id))
        forms = {'4': AddRadiusSettingsForm, '5': AddLDAPSettingsForm}
        form = forms[proto]
        if (hasattr(server, protocol + 'settings') and
            getattr(server, protocol + 'settings')):
            authobj = getattr(server, protocol + 'settings')[0]
            c.form = form(request.POST, authobj, csrf_context=session)
        else:
            authobj = None
            c.form = form(request.POST, csrf_context=session)
        if request.method == 'POST' and c.form.validate():
            updated = False
            if authobj:
                settings = getattr(server, protocol + 'settings')[0]
            else:
                settingsdict = {'4': RadiusSettings, '5': LDAPSettings}
                settings = settingsdict[proto]()
            for field in c.form:
                if field.name == 'csrf_token':
                    continue
                if authobj:
                    if field.name == 'bindpw' and field.data == '':
                        continue
                    if getattr(settings, field.name) != field.data:
                        if field.name == 'bindpw' and field.data == 'None':
                            setattr(settings, field.name, '')
                        else:
                            setattr(settings, field.name, field.data)
                        updated = True
                else:
                    setattr(settings, field.name, field.data)
            try:
                if authobj is None:
                    settings.auth_id = server.id
                if updated or authobj is None:
                    Session.add(settings)
                    Session.commit()
                    if proto == '5':
                        update_ldap_backend()
                if authobj:
                    msg = _('The %(proto)s settings have been updated') \
                            % dict(proto=protocol)
                    flash(msg)
                    log.info(msg)
                else:
                    msg = _('The %(proto)s settings have been created') \
                            % dict(proto=protocol)
                    flash(msg)
                    log.info(msg)
                info = auditmsgs.AUTHSETTINGS_MSG % \
                    dict(d=domain.name, a=proto)
                audit_log(c.user.username,
                        2, unicode(info), request.host,
                        request.remote_addr, arrow.utcnow().datetime)
                redirect(url(controller='domains', action='detail',
                domainid=domain.id))
            except IntegrityError:
                Session.rollback()
                msg = _('The auth settings already exist, '
                        'use update to modify them')
                flash_alert(msg)
                log.info(msg)
        else:
            if proto == '4' and 'authobj' in locals():
                flash(_('The Radius secret is not be displayed in'
                    ' the form, To update type the new secret in '
                    '"Radius secret" below.'))
        c.domain = domain
        c.proto = proto
        c.sid = sid
        return self.render('/domains/authsettings.html')

    @ActionProtector(OwnsDomain())
    def rulesets(self, domainid):
        "Scanner rulesets"
        domain = self._get_domain(domainid)
        if not domain:
            abort(404)
        c.domainid = domain.id
        c.domainname = domain.name
        return self.render('/domains/rulesets.html')

    @ActionProtector(OwnsDomain())
    def addalias(self, domainid):
        "Add alias domain"
        domain = self._get_domain(domainid)
        if not domain:
            abort(404)

        c.form = AddDomainAlias(request.POST, csrf_context=session)
        c.form.domain.query = Session.query(Domain)\
                                    .filter(Domain.id == domainid)
        if request.method == 'POST' and c.form.validate():
            alias = DomainAlias()
            alias.from_form(c.form)
            try:
                create_alias(domain, alias, c.user,
                            request.host, request.remote_addr)
                flash(_('The domain alias: %s has been created') % alias.name)
                redirect(url(controller='domains', action='detail',
                        domainid=domain.id))
            except IntegrityError:
                Session.rollback()
                msg = _('The domain alias: %s already exists') % alias.name
                flash_alert(msg)
                log.info(msg)

        c.domainid = domain.id
        c.domainname = domain.name
        return self.render('/domains/addalias.html')

    def editalias(self, aliasid):
        "Edit alias domain"
        alias = self._get_alias(aliasid)
        if not alias:
            abort(404)

        c.form = EditDomainAlias(request.POST, alias, csrf_context=session)
        c.form.domain.query = Session.query(Domain)\
                            .filter(Domain.id == alias.domain_id)
        if request.method == 'POST' and c.form.validate():
            if update_if_changed(c.form, alias):
                try:
                    edit_alias(alias, c.user, request.host,
                                request.remote_addr)
                    flash(_('The domain alias: %s has been updated') %
                            alias.name)
                    redirect(url('domain-detail', domainid=alias.domain_id))
                except IntegrityError:
                    Session.rollback()
                    msg = _('The update failed')
                    flash_alert(msg)
                    log.info(msg)
            else:
                msg = _('No changes were made to the domain alias')
                flash_info(msg)
                log.info(msg)
                redirect(url('domain-detail', domainid=alias.domain_id))

        c.aliasid = aliasid
        c.domainid = alias.domain_id
        c.domainname = alias.domain.name
        return self.render('/domains/editalias.html')

    def deletealias(self, aliasid):
        "Delete alias domain"
        alias = self._get_alias(aliasid)
        if not alias:
            abort(404)

        c.form = DelDomainAlias(request.POST, alias, csrf_context=session)
        c.form.domain.query = Session.query(Domain)\
                            .filter(Domain.id == alias.domain_id)
        if request.method == 'POST' and c.form.validate():
            domainid, aliasname = delete_alias(alias, c.user,
                                    request.host, request.remote_addr)
            flash(_('The domain alias: %s has been deleted') % aliasname)
            redirect(url('domain-detail', domainid=domainid))

        c.aliasid = aliasid
        c.domainid = alias.domain_id
        c.domainname = alias.domain.name
        return self.render('/domains/deletealias.html')

    def export_domains(self, orgid=None):
        "export domains"
        task = exportdomains.apply_async(args=[
                c.user.id, orgid])
        session['taskids'].append(task.task_id)
        session['dexport-count'] = 1
        session.save()
        msg = _('Domains export is being processed')
        flash(msg)
        log.info(msg)
        redirect(url('domains-export-status', taskid=task.task_id))

    def export_status(self, taskid):
        "export status"
        result = AsyncResult(taskid)
        if result is None or taskid not in session['taskids']:
            msg = _('The task status requested has expired or does not exist')
            flash(msg)
            log.info(msg)
            redirect(url(controller='domains', action='index'))

        if result.ready():
            finished = True
            flash.pop_messages()
            if isinstance(result.result, Exception):
                msg = _('Error occured in processing %s') % result.result
                if c.user.is_superadmin:
                    flash_alert(msg)
                    log.info(msg)
                else:
                    flash_alert(_('Backend error occured during processing.'))
                    log.info(msg)
                redirect(url(controller='domains'))
            results = dict(
                        f=True if not result.result['global_error'] else False,
                        id=taskid, global_error=result.result['global_error'])
        else:
            try:
                session['dexport-count'] += 1
            except KeyError:
                session['dexport-count'] = 1
            session.save()
            if (session['dexport-count'] >= 10 and
                result.state in ['PENDING', 'RETRY', 'FAILURE']):
                result.revoke()
                msg = _('The export could not be processed, try again later')
                flash_alert(msg)
                log.info(msg)
                del session['dexport-count']
                session.save()
                redirect(url(controller='domains'))
            finished = False
            results = dict(f=None, global_error=None)

        c.finished = finished
        c.results = results
        c.success = result.successful()
        done = request.GET.get('d', None)
        if finished and (done and done == 'y'):
            info = auditmsgs.EXPORTDOM_MSG % dict(d='all')
            audit_log(c.user.username,
                    5, unicode(info), request.host,
                    request.remote_addr, arrow.utcnow().datetime)
            response.content_type = 'text/csv'
            response.headers['Cache-Control'] = 'max-age=0'
            csvdata = result.result['f']
            disposition = 'attachment; filename=domains-export-%s.csv' % taskid
            response.headers['Content-Disposition'] = str(disposition)
            response.headers['Content-Length'] = len(csvdata)
            return csvdata
        return self.render('/domains/exportstatus.html')

    # pylint: disable-msg=R0201
    def setnum(self, format=None):
        "Set number of items returned"
        num = check_num_param(request)

        if num and num in [10, 20, 50, 100]:
            session['domains_num_items'] = num
            session.save()
        nextpage = request.headers.get('Referer', '/')
        if '://' in nextpage:
            from_url = urlparse(nextpage)
            nextpage = from_url[2]
        redirect(nextpage)
