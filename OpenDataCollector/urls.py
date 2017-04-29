from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect

urlpatterns = [
    url(r'^$', lambda _: redirect('admin:index'), name='index'),
    url(r'^admin/', admin.site.urls),
]
