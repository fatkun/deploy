# -*- coding: utf-8 -*-
__author__ = 'fatkun'

import datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from django.core.management import setup_environ
import settings
setup_environ(settings)

from deploy.models import *

delete_time = datetime.datetime.now() - datetime.timedelta(days=1)
Health.objects.filter(modify_time__lte=delete_time).delete()