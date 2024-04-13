from djoser.conf import settings
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import serializers
from rest_framework.settings import api_settings

from account.models import Account


class CurrentUserInfoSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Account
        fields = (
            'id',
            'username',
            'image',
            'email',
            'is_critic'
        )

    def update_image(self, instance, validated_data):
        image = validated_data.get('image', None)
        if image:
            instance.image = image
        instance.save()
        return instance


class CustomUserCreateSerializer(UserCreateSerializer):
    def validate(self, attrs):
        if Account.objects.filter(username=attrs.get("username")).exists():
            raise serializers.ValidationError({"username": "username already exists"})

        user = Account(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs

    class Meta(UserCreateSerializer.Meta):
        model = Account
        fields = tuple(Account.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
        )