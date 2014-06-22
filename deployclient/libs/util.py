# -*- coding: utf-8 -*-
__author__ = 'fatkun'

import urllib2, urllib
import socket
import getpass
import json
import time
import os
import logging
from cloghandler import ConcurrentRotatingFileHandler


def retries(max_tries=5, delay=5, backoff=2, exceptions=(Exception,), hook=None):
    """Function decorator implementing retrying logic.

    delay: Sleep this many seconds * backoff * try number after failure
    backoff: Multiply delay by this factor after each failure
    exceptions: A tuple of exception classes; default (Exception,)
    hook: A function with the signature myhook(tries_remaining, exception);
          default None

    The decorator will call the function up to max_tries times if it raises
    an exception.

    By default it catches instances of the Exception class and subclasses.
    This will recover after all but the most fatal errors. You may specify a
    custom tuple of exception classes with the 'exceptions' argument; the
    function will only be retried if it raises one of the specified
    exceptions.

    Additionally you may specify a hook function which will be called prior
    to retrying with the number of remaining tries and the exception instance;
    see given example. This is primarily intended to give the opportunity to
    log the failure. Hook is not called after failure if no retries remain.
    """

    def dec(func):
        def f2(*args, **kwargs):
            mydelay = delay
            tries = range(max_tries)
            tries.reverse()
            for tries_remaining in tries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if tries_remaining > 0:
                        if hook is not None:
                            hook(tries_remaining, e, mydelay)
                        time.sleep(mydelay)
                        mydelay = mydelay * backoff
                    else:
                        raise
                else:
                    break

        return f2

    return dec


def post(url, params, max_tries=5):
    @retries(max_tries=max_tries)
    def _post(url, params):
        response = urllib2.urlopen(url, urllib.urlencode(params), 30)
        content = response.read()
        ret = json.loads(content)
        return ret

    return _post(url, params)


def get_hostname():
    return socket.gethostname()


def get_username():
    return getpass.getuser()

def execute(cmd):
    import subprocess
    run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = run.communicate()
    code = run.returncode
    return code, stdout, stderr

def load_stat():
    loadavg = {}
    code, stdout, stderr = execute("cat /proc/loadavg")
    if code == 0:
        con = stdout.split()
        loadavg['lavg_1'] = con[0]
        loadavg['lavg_5'] = con[1]
        loadavg['lavg_15'] = con[2]
    else:
        return None
    return loadavg

def memory_stat():
    mem = {'Buffers': 0, 'Cached': 0}
    code, stdout, stderr = execute("cat /proc/meminfo")
    if code == 0:
        for line in stdout.split("\n"):
            if len(line) < 2: continue
            name = line.split(':')[0]
            var = line.split(':')[1].split()[0]
            mem[name] = long(var) / 1024
        mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
    else:
        return None
    return mem

def ps_stat():
    code, stdout, stderr = execute("ps uxf")
    if code == 0:
        return {'data': stdout[:65530]}
    else:
        return None

logging.basicConfig(level=logging.NOTSET)
__loggers = {}

def build_logger_env(worker_name, log_level=logging.NOTSET):
    """规范化log输出"""

    logdir_path = os.path.join(os.path.dirname(__file__),
                                    os.pardir,
                                    'log'
                                    )
    if not os.path.exists(logdir_path):
        os.makedirs(logdir_path)
    logger = __loggers.get(worker_name)
    if logger:
        return logger
    logger = logging.getLogger(worker_name)
    logger.propagate = 0                    # 拒绝 父Logger 产生日志
    logger.setLevel(log_level)
    ch = ConcurrentRotatingFileHandler(os.path.join(logdir_path, '%s.log'%worker_name),
                                      'a',
                                      50*1024*1024,
                                      5
                                      )
    ch.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s.%(funcName)s[%(lineno)d] MSG:%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    __loggers.setdefault(worker_name, logger)
    return logger
