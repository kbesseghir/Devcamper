from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
    path('get_current_user/', GetCurrentUser.as_view(), name='get_current_user'),
    path('update_user_info/', UpdateUserInfo.as_view(), name='update_user_info'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailsView.as_view(), name='user-detail'),
    path('users/create/', CreateUserView.as_view(), name='user-create'),
    path('users/<int:pk>/update/', UpdateUserView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='user-delete'),
]
