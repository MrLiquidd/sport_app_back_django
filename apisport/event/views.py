from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from event.models import Event
from event.serializers import EventSerializer


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class EventGamesView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Event.objects.filter(event_type=Event.GAME)


class EventTrainingsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Event.objects.filter(event_type=Event.TRAINING)


class RecentEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        events = Event.objects.order_by('-create_date')[:2]
        serializer = EventSerializer(events, many=True)
        return JsonResponse(serializer.data, safe=False)

    # def get_queryset(self):
    #     return Event.objects.order_by('-create_date')[:5]
