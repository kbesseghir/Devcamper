from django.shortcuts import render
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *
from permission import *
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework import generics
from .serializers import *

class ListBootcampReviews(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        bootcamp_id = self.kwargs['bootcamp_id']
        return Review.objects.filter(bootcamp_id=bootcamp_id)
    
class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Maximum number of items per page


class AllReviews(generics.ListAPIView):
    queryset =Review.objects.all()
    serializer_class =   ReviewSerializer
    pagination_class = CustomPagination  
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['rating']  
    search_fields = ['titel']  


class ReviewDetail(generics.RetrieveAPIView):
    queryset =Review.objects.all()
    serializer_class = ReviewSerializer


class CreateReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):

        if request.user.role == 'publisher' :
                return Response({'message': 'You can nott create a review.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response({'message': 'Review created successfully.'}, status=status.HTTP_201_CREATED)
    



class UpdateReview(generics.RetrieveUpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwner]  # Use the custom permission class

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Review updated successfully.'}, status=status.HTTP_200_OK)
    


class DeleteReview(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    permission_classes = [IsOwner]  # Use the custom permission class

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.delete()
        return Response({'message': 'Review deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    