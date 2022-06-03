from django.urls import path
from .views import WeatherViewSet

urlpatterns = [
    path('',WeatherViewSet.as_view({'get': 'list', 'post': 'create'}), name='weather'),
    path('<int:pk>', WeatherViewSet.as_view({'get': 'getById', 'delete': 'delete'}), name='find-delete-weather'),
]