from django.urls import path
from .views import *

urlpatterns = [
   path('',AllBootcamp.as_view(),name='bootcamps'),
   path('<int:pk>/', BootcampDetail.as_view(), name='bootcamp-detail'),
   path('CreateBootcamp/',CreateBootcamp.as_view(), name='create-bootcamp'),
]
