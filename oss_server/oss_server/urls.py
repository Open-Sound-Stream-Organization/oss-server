"""oss_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from repertoire.api.v1 import v1_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('repertoire/', include('repertoire.urls', namespace='repertoire')),
    url(r'^api/', include(v1_api.urls)),
    url(r'api/doc/', include(('tastypie_swagger.urls', "tastypie_swagger"), namespace='tastypie_swagger')),
]
