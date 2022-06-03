# Wire up our API here
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('weather/', include('rest_api.urls')),
]
