from django.shortcuts import render
from .models import *
from rest_framework import generics
from .serializers import *
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *
from permission import *

class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Maximum number of items per page

class AllBootcamp(generics.ListAPIView):
    queryset =Bootcamp.objects.all()
    Serializer= BootcampSerializer
    pagination_class = CustomPagination  
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name', 'average_rating', 'average_cost']  # Fields for sorting
    search_fields = ['name', 'description','country','street','city','address','zipcode']  # Fields for searching
    
class BootcampDetail(generics.RetrieveAPIView):
    queryset =Bootcamp.objects.all()
    Serializer= BootcampSerializer


class CreateBootcamp(generics.CreateAPIView):
    queryset =Bootcamp.objects.all()
    Serializer= BootcampSerializer
    permission_classes = [IsPublisherOrAdmin]
      
    def perform_create(self, serializer):
        user = self.request.user

        # Check if the user is a publisher and has already created a bootcamp
        if user.role == 'publisher' and Bootcamp.objects.filter(user=user).exists():
            raise serializers.ValidationError('Publishers can create only one bootcamp.')

        serializer.save(user=user) 