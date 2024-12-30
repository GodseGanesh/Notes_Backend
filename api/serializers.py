from rest_framework.serializers import ModelSerializer
from .models import Notes
from django.contrib.auth.models import User
from rest_framework import serializers


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password1=validated_data['password1'],
            password2=validated_data['password2'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user
