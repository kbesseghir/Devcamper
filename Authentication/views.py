from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
import Authentication
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from Authentication.models import *
from .serializers import *
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle

import logging

class UserRegistration(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        # ...

        try:
            response = super().create(request, *args, **kwargs)
            if response.status_code == status.HTTP_201_CREATED:
                user = response.data
                if 'password' in user:
                    user.pop('password')
                logging.Logger.info(f"User registered: {user['email']}")
                return Response(user, status=status.HTTP_201_CREATED)
            return response
        except Exception as e:
            logging.Logger.error(f"User registration failed: {e}")
            raise

class UserLogin(APIView):
    throttle_classes = [UserRateThrottle]  # Add rate limiting to this view
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        logger = logging.getLogger(__name__)

        if email is None or password is None:
            logger.warning('Login attempt with missing email or password')
            return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            EmailValidator(email)
        except ValidationError:
            logger.warning('Login attempt with invalid email format')
            return Response({'error': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            logger.warning('Login attempt with non-existent user')
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            logger.warning('Login attempt with invalid password')
            return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            logger.warning('Login attempt with disabled user account')
            return Response({'error': 'User account is disabled.'}, status=status.HTTP_403_FORBIDDEN)

        logger.info(f"User logged in: {user.email}")
        refresh = RefreshToken.for_user(user)
        response = Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
        response.set_cookie('token', refresh.access_token, max_age=30 * 24 * 60 * 60, secure=True, httponly=True)
        return response

class UserLogout(APIView):
    def post(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)

        response = Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        response.delete_cookie('token')
        logger.info('User logged out')
        return response




