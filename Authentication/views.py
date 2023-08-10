from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from Authentication.models import *
from .serializers import *

class UserRegistration(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            user = response.data
            user.pop('password')  # Remove password from response data
            return Response(user, status=status.HTTP_201_CREATED)
        return response