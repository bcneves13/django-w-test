from django.db import models
from django.core.exceptions import ValidationError 
from datetime import datetime

def validate_decimals(value):
    try:
        return round(float(value), 4)
    except:
        raise ValidationError(
            ('%(value)s is not an integer or a float  number'),
            params={'value': value},
        )
# Implement your models here

def validate_date(value):
    try:
        return datetime.strptime(str(value), '%Y-%m-%d')
    except ValueError:
        raise ValueError('{} is not a valid date'.format(value))
class Weather(models.Model):
    date = models.DateField(blank=False, validators=[validate_date])
    lat = models.DecimalField(blank=False, max_digits=15, decimal_places=4, validators=[validate_decimals])
    lon = models.DecimalField(blank=False, max_digits=15, decimal_places=4, validators=[validate_decimals])
    city = models.CharField(blank=False, max_length=100)
    state = models.CharField(blank=False, max_length=100)
    temperatures = models.TextField(blank=False)
