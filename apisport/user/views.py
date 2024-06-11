from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserInfo, User
from .serializers import UserInfoSerializer, UpdateGenderSerializer, UpdateMobileSerializer, UpdateBornDateSerializer, \
    ChangePasswordSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserInfoDetail(APIView):
    def get(self, request, user_id):
        try:
            user_info = UserInfo.objects.get(user_id=user_id)
            serializer = UserInfoSerializer(user_info)
            return JsonResponse(serializer.data)
        except UserInfo.DoesNotExist:
            return Response({'error': 'UserInfo not found'}, status=404)


class UpdateMobileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = UpdateMobileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': True}, status=status.HTTP_200_OK)
        return Response({'result': False}, status=status.HTTP_400_BAD_REQUEST)


class UpdateGenderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        print(request.data)
        serializer = UpdateGenderSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': True}, status=status.HTTP_200_OK)
        return Response({'result': False}, status=status.HTTP_400_BAD_REQUEST)


class UpdateBornDateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = UpdateBornDateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': True}, status=status.HTTP_200_OK)
        return Response({'result': False}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            # Set the new password
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'result': True}, status=status.HTTP_200_OK)
        return Response({'result': False}, status=status.HTTP_400_BAD_REQUEST)


class SoftDeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            user = get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return Response({'status': False}, status=status.HTTP_404_NOT_FOUND)

        user.is_deleted = True
        user.save()

        return Response({'status': True}, status=status.HTTP_200_OK)
