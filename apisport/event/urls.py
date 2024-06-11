from django.conf.urls.static import static
from django.urls import path

from apisport import settings
from .views import EventListView, EventGamesView, EventTrainingsView, RecentEventsView, EventDetailView, create_visit, \
    check_visit, VisitDeleteView, check_favorite, create_favorite, FavoriteDeleteView, user_events, user_favorites

urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<uuid:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('events/games/', EventGamesView.as_view(), name='event-games'),
    path('events/trainings/', EventTrainingsView.as_view(), name='event-trainings'),
    path('events/recent/', RecentEventsView.as_view(), name='recent-events'),

    path('user/<uuid:user_id>/visits/', user_events, name='user-events'),
    path('events/check-visit/', check_visit, name='check-visit'),
    path('events/create-visit/', create_visit, name='create-visit'),
    path('events/delete-visit/', VisitDeleteView.as_view(), name='delete-visit'),

    path('user/<uuid:user_id>/favorites/', user_favorites, name='user-events'),
    path('events/check-favorite/', check_favorite, name='check-favorite'),
    path('events/create-favorite/', create_favorite, name='create-favorite'),
    path('events/delete-favorite/', FavoriteDeleteView.as_view(), name='delete-favorite'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
