from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView, 
    RetrieveUpdateAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from user.permissions import IsOwner
from user.serializers import LoginSerializer, UserSerializer
# Create your views here.

class UserCreateView(CreateAPIView):
    """ User create view """
    serializer_class = UserSerializer    
    permission_classes = [AllowAny]

class UserLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserManageView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsOwner, )

    def get_object(self):
        """ Get a selected user """
        return self.request.user

class UserListView(ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = get_user_model().objects.all()