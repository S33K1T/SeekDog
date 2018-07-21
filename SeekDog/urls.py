"""SeekDog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.poc import views as poc_view
from apps.info_collect import views as info_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', info_view.home_page),
    path('info-collection/', info_view.info_collect),
    path('info-collection/ajax-whois/', info_view.ajax_whois),
    path('info-collection/output-whois/', info_view.output_whois),
    path('info-collection/ajax-DnsInfo/', info_view.ajax_DnsInfo),
    path('info-collection/ajax-portScan/', info_view.ajax_portScan),
    path('info-collection/ajax-webFinger/', info_view.ajax_webFinger),
    path('info-collection/ajax-robots/', info_view.ajax_robots),
    path('info-collection/ajax-linkCheck/', info_view.ajax_linkCheck),
    path('info-collection/ajax-routerPop/', info_view.ajax_routerPop),
    path('info-collection/ajax-ipLookup/', info_view.ajax_ipLookup),
    path('poc/', poc_view.poc),
    path('ajax-POC/', poc_view.ajax_POC),
    path('fuzz/', include('apps.fuzz.urls'))
]
