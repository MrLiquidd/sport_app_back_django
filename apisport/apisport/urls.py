from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from apisport import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('event.urls'))
]
