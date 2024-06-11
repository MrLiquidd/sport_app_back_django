from django.contrib import admin
from .models import Event, EventAddress, Visit, UserFavoriteEvents

admin.site.register(Event)
admin.site.register(EventAddress)
admin.site.register(Visit)
admin.site.register(UserFavoriteEvents)