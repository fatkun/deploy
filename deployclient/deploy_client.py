 # -*- coding: utf-8 -*-
__author__ = 'fatkun'
from libs import util
import config
import time
import sys
import json
import os

logger = util.build_logger_env(config.WORKER_NAME)

class DeployClient(object):
    host_id = None

    def __init__(self):
        self.register()
        self.health_stat()

    def register(self):
        params = {"version": config.VERSION, "hostname": util.get_hostname(), "username": util.get_username()}
        content = util.post(config.REGISTER_URL, params)
        self.host_id = content['host_id']

    def health_stat(self):
        while True:
            try:
                logger.debug("start collect info")
                send_array = []
                load_info = util.load_stat()
                send_array.append({'type': 'load', 'data': json.dumps(load_info)})
                mem_info = util.memory_stat()
                send_array.append({'type': 'memory', 'data': json.dumps(mem_info)})
                ps_info = util.ps_stat()
                send_array.append({'type': 'ps', 'data': json.dumps(ps_info)})
                util.post(config.HEALTH_URL, {'host_id': self.host_id, 'infos': json.dumps(send_array)})
            except Exception, e:
                logger.exception("health stat error")
            time.sleep(config.MONITOR_INTERVAL)

if __name__ == '__main__':
    if os.name == 'posix':
        from libs.deamon import forkAsDaemon
        base_dir = os.path.dirname(__file__)
        pidfile = ".".join(['deploy', 'pid'])
        pidfile = os.path.join(base_dir, 'log', pidfile)
        forkAsDaemon(pidfile)

    DeployClient()