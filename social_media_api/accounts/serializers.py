from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
["from rest_framework.authtoken.models import Token", "Token.objects.create", "get_user_model().objects.create_user"]

class UserRegistrationSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

class meta:
    model = get_user_model()
    fields = ['id', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        password = validated_data.pop ('password')
        user = get_user_model().objects.create_user(**validated_data, password=password)
        Token.objects.create(user=user)
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        return ('user_loggedin')
    
    user = authenticate(username=email, password=password)
    if user and user.is_active:
        token, _ = Token.objects.get_or_create(user=user)
        
class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
    
    def validate(self, attrs):
        # attrs (attributes) contain the cleaned data, it returns the data after field-level validation.
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'Error': 'password do not match'})
        return super().validate(attrs)
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        return data

class CustomUserSerializer(serializers.ModelSerializer):
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'bio', 'followers', 'following']