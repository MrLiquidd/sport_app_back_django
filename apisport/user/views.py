from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserInfo
from .serializers import UserInfoSerializer


class UserInfoDetail(APIView):
    def get(self, request, user_id):
        try:
            user_info = UserInfo.objects.get(user_id=user_id)
            serializer = UserInfoSerializer(user_info)
            return JsonResponse(serializer.data)
        except UserInfo.DoesNotExist:
            return Response({'error': 'UserInfo not found'}, status=404)

# class UserInfoViewSet(generics.RetrieveDestroyAPIView):
#     queryset = UserInfo.objects.filter(user_id=user_id)
#     serializer_class = UserInfoSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly, )
#
#     @action(methods=['get'], detail=True)
#     def user_info(self, request, pk):
#         user_id = self.kwargs.get("user_id")
#         return Response({'user_info': user_info})


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     UserModel View.
#     """
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     @action(detail=True, methods=["PATCH"])
#     def verify_otp(self, request, pk=None):
#         instance = self.get_object()
#         if (
#                 not instance.is_active
#                 and instance.otp == request.data.get("otp")
#                 and instance.otp_expiry
#                 and timezone.now() < instance.otp_expiry
#         ):
#             instance.is_active = True
#             instance.otp_expiry = None
#             instance.max_otp_try = settings.MAX_OTP_TRY
#             instance.otp_max_out = None
#             instance.save()
#             return Response(
#                 "Successfully verified the user.", status=status.HTTP_200_OK
#             )
#
#         return Response(
#             "User active or Please enter the correct OTP.",
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#
#     @action(detail=True, methods=["PATCH"])
#     def regenerate_otp(self, request, pk=None):
#         """
#         Regenerate OTP for the given user and send it to the user.
#         """
#         instance = self.get_object()
#         if int(instance.max_otp_try) == 0 and timezone.now() < instance.otp_max_out:
#             return Response(
#                 "Max OTP try reached, try after an hour",
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         otp = random.randint(1000, 9999)
#         otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
#         max_otp_try = int(instance.max_otp_try) - 1
#
#         instance.otp = otp
#         instance.otp_expiry = otp_expiry
#         instance.max_otp_try = max_otp_try
#         if max_otp_try == 0:
#             # Set cool down time
#             otp_max_out = timezone.now() + datetime.timedelta(hours=1)
#             instance.otp_max_out = otp_max_out
#         elif max_otp_try == -1:
#             instance.max_otp_try = settings.MAX_OTP_TRY
#         else:
#             instance.otp_max_out = None
#             instance.max_otp_try = max_otp_try
#         instance.save()
#         send_otp(instance.phone_number, otp)
#         return Response("Successfully generate new OTP.", status=status.HTTP_200_OK)
