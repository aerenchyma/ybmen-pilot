from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from ybmenpilot.views import get_access_token

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ybmenpilot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^getaccess', 'ybmenpilot.views.get_access_token',csrf_exempt(get_access_token),name='get_access_token'),
    url(r'^admin/', include(admin.site.urls)),
)
