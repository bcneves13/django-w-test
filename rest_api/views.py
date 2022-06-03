from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.exceptions import ValidationError
from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from .models import Weather
from .serializers import WeatherSerializer
from rest_framework.authtoken.models import Token
import json


class WeatherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Weather.objects.all().order_by('-id')
    serializer_class = WeatherSerializer

    @action(detail=True, methods=['get'])
    def list(self, request):
        date_filter = request.GET.get('date', None)
        city_filter = request.GET.get('city', None)
        sort = request.GET.get('sort', None)
        if date_filter:
            queryset = Weather.objects.filter(date=date_filter)
        elif city_filter:
            queryset = Weather.objects.filter(city=city_filter.capitalize()) if ',' not in city_filter else Weather.objects.filter(city__in=[city.strip().capitalize() for city in city_filter.split(',')])
        else:
            queryset = Weather.objects.all().order_by('id')
        
        if sort == 'date' or sort == '-date':
            queryset = queryset.order_by(sort)

        serialize = WeatherSerializer(queryset, many=True)
        status = 200 if len(serialize.data) > 0 else 404
        return JsonResponse(serialize.data, safe=False, status=status)
    
    @action(detail=True, methods=['get'])
    def getById(self, request, pk):
        queryset = get_object_or_404(Weather, pk=pk)
        serialize = WeatherSerializer(queryset)
        return JsonResponse(serialize.data, safe=False, status=200)
    
    @action(detail=True, methods=['post'])	
    def create(self, request):
        insert_data = dict()
        for key, value in request.data.items():
            insert_data[key] = value
        
        try:
            insert_data['lat'] = str(round(insert_data['lat'], 4))
            insert_data['lon'] = str(round(insert_data['lon'], 4))
            insert_data['temperatures'] = json.dumps(insert_data['temperatures'], separators=(',', ':'))
            instance = Weather(**insert_data)
            instance.full_clean()
            instance.save()
        except (TypeError,ValidationError, KeyError) as Error:
            return JsonResponse({'message': 'Erro ao inserir: {}'.format(Error)}, safe=False, status=400)
        insert_data['id'] = instance.pk
        insert_data['lat'] = round(float(insert_data['lat']), 4)
        insert_data['lon'] = round(float(insert_data['lon']), 4)
        insert_data['temperatures'] = json.loads(insert_data['temperatures'])
        return JsonResponse(insert_data, safe=False, status=201)
    
    @action(detail=True, methods=['delete'])
    def delete(self, request, pk):
        queryset = get_object_or_404(Weather, pk=pk)
        queryset.delete()
        return JsonResponse({'message': '{} removido com sucesso'.format(pk)})