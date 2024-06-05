from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
def me(request):
    user = request.user
    if user.is_authenticated:
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username
        })
