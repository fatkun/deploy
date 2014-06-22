# -*- coding: utf-8 -*-
__author__ = 'fatkun'
import os

VERSION = '1.0'
SERVER_URL = "http://localhost:8000"
REGISTER_URL = SERVER_URL + "/register"
HEALTH_URL = SERVER_URL + "/health"

MONITOR_INTERVAL = 120
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
WORKER_NAME = "deploy"