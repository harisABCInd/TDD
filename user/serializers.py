from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=64, write_only=True)
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True, "min_length": 5},
        }
    
    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        if validated_data['password'] != confirm_password:
            raise ValidationError("Password does not match")
        
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        confirm_password = validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("Password does not match")
            user.set_password(password)
            user.save()
            
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    attrs['user'] = user
                    return attrs
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to login with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')