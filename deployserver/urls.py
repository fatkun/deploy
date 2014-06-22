from django.conf.urls.defaults import patterns, include, url

from django.conf import settings


urlpatterns =  patterns('deploy.views.api_views',
                       url('^register$', 'register'),
                       url('^health$', 'health'),
) + \
              patterns('deploy.views.page_views',
                       url('^$', 'index'),
                       url('^index$', 'index'),
                       url('^detail$', 'detail'),
                       url('^login$', 'login'),
                       url('^logout$', 'logout'),
              )

urlpatterns += patterns('', (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}))