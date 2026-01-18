from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email','password','confirm_password']
        
    def validate(self,attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('passwords donot match!')
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('confirm_password')
        
        user = User(
            email = validated_data['email'],
            is_active = False
        )
        
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self,attrs):
        email = attrs['email']
        password = attrs['password']
        
        
        if not email or not password:
            raise serializers.ValidationError("Must include both 'email' and 'password'.")
        
        user = authenticate(email=attrs['email'], password =attrs['password'])
              
        
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        attrs['user'] = user

        return attrs
        
        