from django.contrib import admin

from .models import User, UserInfo, Friends

admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(Friends)