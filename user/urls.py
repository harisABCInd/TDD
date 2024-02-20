from django.urls import path
from user.views import (
    UserCreateView, 
    UserListView, 
    UserLoginView, 
    UserManageView
)

app_name = 'user'

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserManageView.as_view(), name='profile'),
    path('list', UserListView.as_view(), name='list')
    # Add more URL patterns as needed
]