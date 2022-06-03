from rest_framework import serializers
from .models import Weather
import json
import decimal
# Implement your serializers here
class WeatherSerializer(serializers.Serializer):
    class Meta:
        model = Weather
        fields = ('id', 'date', 'lat', 'lon', 'city', 'state', 'temperatures')
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateField()
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    lat = serializers.SerializerMethodField()
    lon = serializers.SerializerMethodField()
    temperatures = serializers.SerializerMethodField()
    def get_lat(self, obj):
        return round(float(obj.lat), 4)
    def get_lon(self, obj):
        return round(float(obj.lon), 4)
    def get_temperatures(self, obj):
        return json.loads(obj.temperatures)