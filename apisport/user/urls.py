from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static

from . import api
from .views import UserInfoDetail

router = SimpleRouter()
# router.register(r'user-info', UserInfoViewSet)

urlpatterns = [
    path('account/', api.me, name='account'),
    path('user-info/<uuid:user_id>/', UserInfoDetail.as_view(), name='user-info-detail'),

    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),

    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]
