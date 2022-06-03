from django.contrib import admin
from .models import Weather
# Register your models here.

@admin.register(Weather)
class ListWeathers(admin.ModelAdmin):
    list_display = ('id', 'date', 'lat', 'lon', 'city', 'state', 'temperatures')
    list_filter = ('date',)
    search_fields = ('id',)
