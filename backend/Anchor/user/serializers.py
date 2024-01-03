# serializers.py

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_id",
            "username",
            "password",
        )

    def validate_password(self, value):
        return make_password(value)

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("displayName", "profileImage", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        instance.displayName = validated_data.get("displayName", instance.displayName)
        instance.profileImage = validated_data.get(
            "profileImage", instance.profileImage
        )

        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        instance.save()
        return instance
