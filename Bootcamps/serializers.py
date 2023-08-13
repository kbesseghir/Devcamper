from rest_framework import serializers
from .models import *

class BootcampSerializer(serializers.Serializer):
    class Meta: 
        model= Bootcamp
        fields = ['id', 'name', 'description', 'average_rating', 'average_cost','address']