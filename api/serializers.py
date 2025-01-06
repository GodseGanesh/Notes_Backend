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
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password since it's not a User model field
        return User.objects.create_user(**validated_data)

