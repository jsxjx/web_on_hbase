"""CKG_QAR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main_web.views.index', name='home'),
    url(r'^storing_data/$', 'main_web.views.storing_data'),
    url(r'^query_single_para_html/$','main_web.views_query.query_single_para_html',
        name = 'query_single_para_html'),
    url(r'^ajax_single_para/$', 'main_web.views_query.ajax_single_para',
        name = 'ajax_single_para')
]
