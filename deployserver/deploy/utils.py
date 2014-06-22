# -*- coding: utf-8 -*-
__author__ = 'fatkun'
import json
from django.http import HttpResponse, HttpResponseRedirect

def json_api(*args, **kwargs):
    logger = kwargs.get('logger')
    def f_wrapper(func):
        def new_fun(*args, **kwargs):
            try:
                ret = func(*args, **kwargs)
                if not ret.get('success'):
                    ret['success'] = True
                result = json.dumps(ret)
            except Exception, e:
                if logger:
                    logger.exception("%s" % e)
                result = {'success': False, 'msg': "%s" % e}
            return HttpResponse(result)
        return new_fun

    if not args:
        return f_wrapper
    else:
        f = args[0]
        new_f = f_wrapper(f)
        return new_f

def login_required(func):
    def new_fun(request, *args, **kwargs):
        if not request.session.get('login', False):
            return HttpResponseRedirect("/login")
        else:
            return func(request, *args, **kwargs)
    return new_fun