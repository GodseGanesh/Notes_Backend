from rest_framework.serializers import ModelSerializer
from .models import Notes
from django.contrib.auth.models import User
from rest_framework import serializers


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email = validated_data['email']
        )
        return user
