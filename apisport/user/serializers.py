from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from datetime import datetime, timedelta
import random

from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apisport import settings
from .models import User, UserInfo, Friends
from .utils import send_otp


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.is_deleted:
            raise AuthenticationFailed('User account is deleted.')
        return data

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={
            "min_length": "Password must be longer than {} characters".format(
                settings.MIN_PASSWORD_LENGTH
            )
        },
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={
            "min_length": "Password must be longer than {} characters".format(
                settings.MIN_PASSWORD_LENGTH
            )
        },
    )

    class Meta:
        model = User
        fields = ('username', 'user_type_id', 'blocked')

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        otp = random.randint(1000, 9999)
        otp_expiry = datetime.now() + timedelta(minutes=10)

        user = User(
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            otp=otp,
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY
        )
        user.set_password(validated_data["password1"])
        user.save()
        send_otp(validated_data["phone_number"], otp)
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    city = serializers.ReadOnlyField(source="city.city")
    photo_id = serializers.SerializerMethodField()
    friends_count = serializers.SerializerMethodField()

    class Meta:
        model = UserInfo
        fields = ['id', 'user', 'first_name', 'last_name', 'about_me', 'age', 'photo_id', 'city', 'deleted',
                  'friends_count']

    @staticmethod
    def get_friends_count(obj):
        return Friends.objects.filter(user_id=obj.user_id, deleted=False).count()

    @staticmethod
    def get_photo_id(obj):
        return obj.photo_id.photo.name


class UpdateMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile']


class UpdateGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['gender']


class UpdateBornDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['born_date']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is not correct')
        return value
