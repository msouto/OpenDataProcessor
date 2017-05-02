from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect

from base.admin import admin_site

urlpatterns = [
    url(r'^$', lambda _: redirect('admin:index'), name='index'),
    url(r'^admin/', admin_site.urls),
]
