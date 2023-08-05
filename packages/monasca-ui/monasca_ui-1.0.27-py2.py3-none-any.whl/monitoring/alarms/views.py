# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.import logging

import json
import logging

from django.conf import settings  # noqa
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse  # noqa
from django.shortcuts import redirect
from django.template import defaultfilters as filters
from django.utils.translation import ugettext as _  # noqa
from django.views.generic import View  # noqa
from django.views.generic import TemplateView  # noqa
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from horizon import exceptions
from horizon import forms
from horizon import tables

import monascaclient.exc as exc
from monitoring.alarms import constants
from monitoring.alarms import forms as alarm_forms
from monitoring.alarms import tables as alarm_tables
from monitoring import api

LOG = logging.getLogger(__name__)
SERVICES = getattr(settings, 'MONITORING_SERVICES', [])

LIMIT = 10
def get_icon(status):
    if status == 'chicklet-success':
        return constants.OK_ICON
    if status == 'chicklet-error':
        return constants.CRITICAL_ICON
    if status == 'chicklet-warning':
        return constants.WARNING_ICON
    if status == 'chicklet-unknown':
        return constants.UNKNOWN_ICON
    if status == 'chicklet-notfound':
        return constants.NOTFOUND_ICON


priorities = [
    {'status': 'chicklet-success', 'severity': 'OK'},
    {'status': 'chicklet-unknown', 'severity': 'UNDETERMINED'},
    {'status': 'chicklet-warning', 'severity': 'LOW'},
    {'status': 'chicklet-warning', 'severity': 'MEDIUM'},
    {'status': 'chicklet-warning', 'severity': 'HIGH'},
    {'status': 'chicklet-error', 'severity': 'CRITICAL'},
]
index_by_severity = {d['severity']: i for i, d in enumerate(priorities)}


def get_status(alarms):
    if not alarms:
        return 'chicklet-notfound'
    status_index = 0
    for a in alarms:
        severity = alarm_tables.show_severity(a)
        severity_index = index_by_severity[severity]
        status_index = max(status_index, severity_index)
    return priorities[status_index]['status']


def generate_status(request):
    try:
        alarms = api.monitor.alarm_list(request)
    except Exception as e:
        messages.error(request,
                       _('Unable to list alarms: %s') % str(e))
        alarms = []
    alarms_by_service = {}
    for a in alarms:
        service = alarm_tables.show_service(a)
        service_alarms = alarms_by_service.setdefault(service, [])
        service_alarms.append(a)
    for row in SERVICES:
        row['name'] = unicode(row['name'])
        for service in row['services']:
            service_alarms = alarms_by_service.get(service['name'], [])
            service['class'] = get_status(service_alarms)
            service['icon'] = get_icon(service['class'])
            service['display'] = unicode(service['display'])
    return SERVICES


class IndexView(View):
    def dispatch(self, request, *args, **kwargs):
        return redirect(constants.URL_PREFIX + 'alarm', service='all')


class AlarmServiceView(tables.DataTableView):
    table_class = alarm_tables.AlarmsTable
    template_name = constants.TEMPLATE_PREFIX + 'alarm.html'

    def dispatch(self, *args, **kwargs):
        self.service = kwargs['service']
        del kwargs['service']
        return super(AlarmServiceView, self).dispatch(*args, **kwargs)

    def get_data(self):
        page_offset = self.request.GET.get('page_offset')
        contacts = []

        if page_offset == None:
            page_offset = 0

        if self.service == 'all':
            try:
                results = api.monitor.alarm_list(self.request, page_offset,
                                                 LIMIT)
                paginator = Paginator(results, LIMIT)
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
            except Exception:
                messages.error(self.request, _("Could not retrieve alarms"))
            return contacts
        else:
            try:
                results = api.monitor.alarm_list_by_service(self.request,
                                                            self.service,
                                                            page_offset,
                                                            LIMIT)
            except Exception:
                messages.error(self.request, _("Could not retrieve alarms"))
                results = []
            return results

    def get_context_data(self, **kwargs):
        context = super(AlarmServiceView, self).get_context_data(**kwargs)
        results = []
        page_offset = self.request.GET.get('page_offset')

        if page_offset == None:
            page_offset = 0

        if self.service == 'all':
            try:
                results = api.monitor.alarm_list(self.request, page_offset,
                                                 LIMIT)
                paginator = Paginator(results, LIMIT)
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
            except Exception:
                messages.error(self.request, _("Could not retrieve alarms"))
        else:
            try:
                results = api.monitor.alarm_list_by_service(self.request,
                                                            self.service,
                                                            page_offset,
                                                            LIMIT)
            except Exception:
                messages.error(self.request, _("Could not retrieve alarms"))
                results = []

        context["contacts"] = results
        context["service"] = self.service

        if len(results) < LIMIT:
            context["page_offset"] = None
        else:
            context["page_offset"] = results[-1]["id"]

        return context


def transform_alarm_history(results, name):
    newlist = []
    for item in results:
        temp = {}
        temp['alarm_id'] = item['alarm_id']
        temp['name'] = name
        temp['old_state'] = item['old_state']
        temp['new_state'] = item['new_state']
        temp['timestamp'] = item['timestamp']
        temp['reason'] = item['reason']
        temp['metrics'] = item['metrics']
        temp['reason_data'] = item['reason_data']
        newlist.append(temp)
    return newlist


class AlarmHistoryView(tables.DataTableView):
    table_class = alarm_tables.AlarmHistoryTable
    template_name = constants.TEMPLATE_PREFIX + 'alarm_history.html'

    def dispatch(self, *args, **kwargs):
        return super(AlarmHistoryView, self).dispatch(*args, **kwargs)

    def get_data(self):
        page_offset=self.request.GET.get('page_offset')
        contacts=[]
        id = self.kwargs['id']
        name = self.kwargs['name']
        results = []
        if page_offset == None:
            page_offset = 0
        try:
            results = api.monitor.alarm_history(self.request, id, page_offset,
                                                LIMIT)
            paginator = Paginator(results, LIMIT)
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        except Exception:
            messages.error(self.request,
                           _("Could not retrieve alarm history for %s") % id)
        return transform_alarm_history(contacts, name)

    def get_context_data(self, **kwargs):
        context = super(AlarmHistoryView, self).get_context_data(**kwargs)
        id = self.kwargs['id']
        try:
            alarm = api.monitor.alarm_get(self.request, id)
        except Exception:
            messages.error(self.request,
                           _("Could not retrieve alarm for %s") % id)
        context['alarm'] = alarm

        contacts = []
        page_offset = self.request.GET.get('page_offset')

        if page_offset == None:
            page_offset = 0
        try:
            results = api.monitor.alarm_history(self.request, id,  page_offset,
                                                LIMIT)
            paginator = Paginator(results, LIMIT)
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        except Exception:
            messages.error(self.request,
                           _("Could not retrieve alarm history for %s") % id)
            return context

        context["contacts"] = contacts
        if len(contacts.object_list) < LIMIT:
            context["page_offset"] = None
        else:
            context["page_offset"] = contacts.object_list[-1]["id"]

        return context

