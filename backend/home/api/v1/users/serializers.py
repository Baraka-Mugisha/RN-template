from allauth.utils import generate_unique_username
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from home.api.v1.users.models import User


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(min_length=10)
    username = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User

        fields = [
            "id", "phone_number", "last_login", "is_superuser", "username", "first_name", "last_name", "email",
            "is_staff", "is_active", "date_joined", "phone_number_verified", "terms_condition_agree",
            "full_profile_image_url", "full_name", "url"
        ]
        read_only_fields = [
            "last_login", "is_superuser", "is_staff", "date_joined", "is_active", "phone_number_verified",
            "full_profile_image_url", "full_name", "url"
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }


class SignupSerializer(UserSerializer):
    def create(self, validated_data):
        try:
            validated_data["username"] = generate_unique_username([validated_data.get('phone_number'), 'user'])
            validated_data["is_active"] = False
            user = super(SignupSerializer, self).create(validated_data)
            # needs to first verify phone to be able to be activated
            # TODO: send SMS to verify user phone number, save the code to user model for later
            return user
        except IntegrityError:
            raise ValidationError({"error": "Phone number already used by another user"})


class VerifyPhoneNumberSerializer(UserSerializer):
    verification_code = serializers.CharField(min_length=6, max_length=6)
    phone_number = serializers.CharField(min_length=10)

    class Meta:
        model = User
        fields = ["verification_code", "phone_number"]

    def create(self, validated_data):
        try:
            user = User.objects.get(
                phone_number=validated_data.get("phone_number"),
                verification_code=validated_data.get("verification_code")
            )
            user.is_active = True
            user.phone_number_verified = True
            user.save()
            return user
        except User.DoesNotExist:
            raise ValidationError({"error": "Invalid or Expired code provided"})


class UserViewSetSerializer(UserSerializer):
    phone_number = serializers.CharField(min_length=10, read_only=True)
