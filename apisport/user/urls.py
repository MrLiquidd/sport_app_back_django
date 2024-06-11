from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import api
from .views import UserInfoDetail, UpdateMobileView, UpdateGenderView, UpdateBornDateView, ChangePasswordView, \
    SoftDeleteUserView, CustomTokenObtainPairView

urlpatterns = [
    path('account/', api.me, name='account'),
    path('user-info/<uuid:user_id>/', UserInfoDetail.as_view(), name='user-info-detail'),

    path('signup/', api.signup, name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain'),

    path('update/mobile/', UpdateMobileView.as_view(), name='update-mobile'),
    path('update/gender/', UpdateGenderView.as_view(), name='update-gender'),
    path('update/borndate/', UpdateBornDateView.as_view(), name='update-born-date'),
    path('update/change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('soft-delete/<uuid:pk>', SoftDeleteUserView.as_view(), name='soft-delete-user'),

]
