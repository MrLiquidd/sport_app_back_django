from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from user.models import UserInfo, User
from user.serializers import UserInfoSerializer


@api_view(['GET'])
def me(request):
    user = request.user
    if user.is_authenticated:
        print(request.user.born_date)
        return JsonResponse({
            'id': request.user.id,
            'email': request.user.email,
            'username': request.user.username,
            'mobile': request.user.mobile,
            'gender': request.user.gender,
            'born_date': request.user.born_date
        })


# @api_view(['GET'])
# def user_info(request, user_id):
#     user_info = UserInfo.objects.get(user_id=user_id)
#     serializer_class = UserInfoSerializer(user_info, many=False)
#     print(serializer_class.data)
#     return JsonResponse(serializer_class.data)
#

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    email = data.get('email')
    password1 = data.get('password1')
    password2 = data.get('password2')

    if password1 != password2:
        return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})

    try:
        user = User.objects.create_user(username=email, email=email, password=password1)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

    # Check if user is created and UserInfo is also created
    if user:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'User creation failed'})
