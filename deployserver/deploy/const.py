 # -*- coding: utf-8 -*-
__author__ = 'fatkun'

class State(object):
    EMPTY = 'empty'
    INIT = 'init'
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'

class InfoType:
    """收集信息类型"""
    PS = 'ps'
    LOAD = 'load'
    MEMORY = 'memory'