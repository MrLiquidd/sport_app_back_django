from rest_framework import serializers
from datetime import datetime, timedelta
import random

from apisport import settings
from .models import User, UserInfo, Friends
from .utils import send_otp


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
        """
        Validates if both password are same or not.
        """

        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        """
        Create method.

        Used to create the user
        """
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
    photo_id = serializers.FileField(source='photo_id.photo', read_only=True)
    friends_count = serializers.SerializerMethodField()

    class Meta:
        model = UserInfo
        fields = ['id', 'user', 'first_name', 'last_name', 'about_me', 'age', 'photo_id', 'city', 'deleted',
                  'friends_count']

    @staticmethod
    def get_friends_count(obj):
        return Friends.objects.filter(user_id=obj.user_id, deleted=False).count()

# class UserInfoSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source="user.id")
#     city = serializers.ReadOnlyField(source="city.city")
#     friends_count = serializers.SerializerMethodField()
#
#     class Meta:
#         model = UserInfo
#         fields = ['id', 'user', 'first_name', 'last_name',
#                   'about_me', 'age', 'photo_id', 'city', 'deleted', 'friends_count']
#
#     def get_friends_count(obj):
#         return Friends.objects.filter(user_id=obj.user, deleted=False).count()
