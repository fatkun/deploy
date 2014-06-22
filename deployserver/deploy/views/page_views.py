# -*- coding: utf-8 -*-

__author__ = 'fatkun'
from deploy.models import *
from deploy import const
from deploy import utils
import datetime
import json
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from common.natsort import natsorted
from settings import LOGIN_PASSWORD
from django.core.urlresolvers import reverse

@utils.login_required
def index(request):
    hosts = Host.objects.all()

    hosts_group = {}
    for host in hosts:
        tags = host.tags
        if not tags:
            tags = u'其他'
        if tags not in hosts_group:
            hosts_group[tags] = []
        hosts_group[tags].append(host)

    for key in hosts_group:
        hosts_group[key] = natsorted(hosts_group[key], key=lambda x: x.hostname)


    return render_to_response('index.html', {'hosts_group': hosts_group})

@utils.login_required
def detail(request):
    host_id = request.REQUEST.get('host_id')
    host = Host.objects.get(id=host_id)

    health_info = {const.InfoType.LOAD: None, const.InfoType.MEMORY: None, const.InfoType.PS: None}
    modify_time = None
    health = Health.objects.filter(host__id=host_id, type=const.InfoType.LOAD).order_by('-modify_time')[:1]
    if health:
        modify_time = health[0].modify_time
        health_info[const.InfoType.LOAD] = json.loads(health[0].data, encoding='utf-8')
    health = Health.objects.filter(host__id=host_id, type=const.InfoType.MEMORY).order_by('-modify_time')[:1]
    if health:
        health_info[const.InfoType.MEMORY] = json.loads(health[0].data, encoding='utf-8')
    health = Health.objects.filter(host__id=host_id, type=const.InfoType.PS).order_by('-modify_time')[:1]
    if health:
        health_info[const.InfoType.PS] = json.loads(health[0].data, encoding='utf-8')



    return render_to_response('detail.html', {'host': host, 'health_info': health_info, 'modify_time': modify_time})

def login(request):
    login = request.REQUEST.get('login')
    password = request.POST.get('password')
    if login == '1':
        if LOGIN_PASSWORD == password:
            request.session['login'] = True
            return HttpResponseRedirect(reverse(r'deploy.views.page_views.index'))

    return render_to_response('login.html')

def logout(request):
    if 'login' in request.session:
        del request.session['login']
    return HttpResponseRedirect(reverse(r'deploy.views.page_views.login'))