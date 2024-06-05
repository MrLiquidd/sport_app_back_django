from rest_framework import routers
from user.views import UserInfoViewSet

router = routers.DefaultRouter()
router.register(r'user_info_list', UserInfoViewSet, basename='user-info')