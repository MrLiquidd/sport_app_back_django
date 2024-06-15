import base64

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.files.base import ContentFile
from django.db.models import Q

from .models import UserInfo, Friends, User
from .serializers import UserInfoSerializer, UpdateGenderSerializer, UpdateMobileSerializer, UpdateBornDateSerializer, \
    ChangePasswordSerializer, CustomTokenObtainPairSerializer, UserModelSerializer


class Base64ImageParser(BaseParser):
    """
    Парсер для обработки изображений в формате base64.
    """

    media_type = 'image/*'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Преобразует данные изображения в формате base64 в объект ContentFile.
        """
        try:
            decoded_data = base64.b64decode(stream.read())
        except ValueError:
            raise ParseError('Некорректные данные изображения в формате base64.')

        return ContentFile(decoded_data)


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


class UserInfoUpdateAPIView(APIView):
    parser_classes = [JSONParser, Base64ImageParser]

    def put(self, request, *args, **kwargs):
        user_info = request.user.userinfo  # Получаем информацию о пользователе через аутентифицированного пользователя
        print(request.data)
        serializer = UserInfoSerializer(user_info, data=request.data.get('profileData'))
        if serializer.is_valid():
            serializer.save()

            photo_data = request.data.get('profileData').get('photo')
            if photo_data:
                image_data = photo_data.split(';base64,')[-1]
                image_file = ContentFile(base64.b64decode(image_data), name='photo.jpg')
                user_info.photo_id.photo = image_file
                user_info.photo_id.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class FriendsInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Найти друзей пользователя
        friends = Friends.objects.filter(
            Q(user_id=user_id) | Q(friend_id=user_id),
            deleted=False
        ).select_related('user_id', 'friend_id')

        # Список для хранения информации о друзьях
        friends_info = []

        for friend in friends:
            friend_user = friend.friend_id if friend.user_id.id == user_id else friend.user_id
            try:
                user_info = UserInfo.objects.select_related('photo_id').get(user_id=friend_user.id)
                serializer = UserInfoSerializer(user_info)
                friends_info.append(serializer.data)
            except UserInfo.DoesNotExist:
                continue

        return JsonResponse(friends_info, safe=False)


class FriendsSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({"error": "Query parameter 'query' is required"}, status=400)

        users = User.objects.filter(
            Q(email__icontains=query) |
            Q(username__icontains=query) |
            Q(mobile__icontains=query)
        )

        user_infos = UserInfo.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).select_related('user_id')

        # Собрать ID пользователей из UserInfo для объединения результатов
        user_info_user_ids = [user_info.user_id.id for user_info in user_infos]

        # Объединить результаты из User и UserInfo
        final_users = users | User.objects.filter(id__in=user_info_user_ids)

        # Сериализовать данные пользователей
        user_serializer = UserModelSerializer(final_users, many=True)
        user_info_serializer = UserInfoSerializer(user_infos, many=True)

        return JsonResponse({
            # "users": user_serializer.data,
            "user_infos": user_info_serializer.data
        })
