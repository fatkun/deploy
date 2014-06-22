# -*- coding: utf-8 -*-

from deploy.models import *
from deploy import const
from deploy import utils
import datetime
import json
import logging

logger = logging.getLogger()

@utils.json_api
def fetch_task(request):
    hostname = request.REQUEST['hostname']
    user = request.REQUEST['user']
    subtasks = SubTask.objects.filter(host__hostname=hostname, host__user=user, state=const.State.INIT).all()

@utils.json_api
def register(request):
    hostname = request.REQUEST.get('hostname')
    username = request.REQUEST.get('username')
    version = request.REQUEST.get('version')

    host, created = Host.objects.get_or_create(hostname=hostname, username=username, defaults={'version': version})
    if not created:
        host.version = version
        host.save()

    return {'success': True, 'host_id': host.id}

@utils.json_api(logger=logger)
def health(request):
    host_id = request.REQUEST.get('host_id')
    infos = request.REQUEST.get('infos')
    now = datetime.datetime.now()
    host = Host.objects.get(id=host_id)

    infos = json.loads(infos, 'utf-8')
    for info in infos:
        type = info['type']
        data = info['data']
        health = Health.objects.create(host=host, type=type, data=data, modify_time=now)

    return {'success': True}