from django.conf.urls.static import static
from django.urls import path

from apisport import settings
from .views import EventListView, EventGamesView, EventTrainingsView, RecentEventsView

urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/games/', EventGamesView.as_view(), name='event-games'),
    path('events/trainings/', EventTrainingsView.as_view(), name='event-trainings'),
    path('events/recent/', RecentEventsView.as_view(), name='recent-events'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
