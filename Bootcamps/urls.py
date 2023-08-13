from django.urls import path
from .views import *

urlpatterns = [
   path('Bootcamps/',AllBootcamp.as_view(),name='bootcamps'),
   path('Bootcamps/<int:pk>/', BootcampDetail.as_view(), name='bootcamp-detail'),
]
