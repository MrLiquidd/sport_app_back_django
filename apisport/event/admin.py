from django.contrib import admin
from .models import Event, EventAddress, Visit

admin.site.register(Event)
admin.site.register(EventAddress)
admin.site.register(Visit)