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
from django.urls import path,include
from apps.poc import views as poc_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('poc/', poc_view.poc),
<<<<<<< HEAD
    path('ajax-POC/', poc_view.ajax_POC)
=======
    path('fuzz/',include('apps.fuzz.urls'))
>>>>>>> e828efea7c69c248d5678ad08bafe2793542acfb
]
