from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count, Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response

from event.models import Event, Visit, UserFavoriteEvents, EventAddress
from event.serializers import EventSerializer
from user.models import User


class EventListView(generics.ListAPIView):
    queryset = Event.objects.annotate(user_count=Count('event_visit__user_id'))
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class EventDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @staticmethod
    def get(request, event_id):
        try:
            event = Event.objects.annotate(user_count=Count('event_visit__user_id')).get(pk=event_id)
            serializer = EventSerializer(event, context={'request': request})
            return JsonResponse(serializer.data, safe=False)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=404)


class EventGamesView(generics.ListAPIView):
    queryset = Event.objects.annotate(user_count=Count('event_visit__user_id'))
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Event.objects.filter(event_type=Event.GAME)


class EventTrainingsView(generics.ListAPIView):
    queryset = Event.objects.annotate(user_count=Count('event_visit__user_id'))
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Event.objects.filter(event_type=Event.TRAINING)


class RecentEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        events = Event.objects.annotate(user_count=Count('event_visit__user_id')).order_by('-create_date')[:2]
        serializer = EventSerializer(events, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def user_events(request, user_id):
    user = get_object_or_404(User, id=user_id)

    visits = Visit.objects.filter(user_id=user, deleted=False).select_related('event_id')

    event_ids = visits.values_list('event_id', flat=True)
    event_addresses = EventAddress.objects.filter(event_id__in=event_ids, deleted=False)
    prefetch_addresses = Prefetch('event_event_address', queryset=event_addresses, to_attr='addresses')

    events = Event.objects.filter(id__in=event_ids).annotate(user_count=Count('event_visit')).prefetch_related(
        prefetch_addresses)

    events_data = []
    for event in events:
        full_address = event.addresses[0].full_address if event.addresses else ""
        event_data = {
            "id": event.id,
            "title": event.title,
            "price": event.price,
            "event_type": event.event_type,
            "about": event.about,
            "min_age": event.min_age,
            "quantity": event.quantity,
            "photo_id": event.photo_id.photo.name,
            "date": event.date,
            "is_active": event.is_active,
            "create_date": event.create_date,
            "archive": event.archive,
            "deleted": event.deleted,
            "user_count": event.user_count,
            "full_addresses": full_address
        }
        events_data.append(event_data)

    return JsonResponse(events_data, safe=False)



@api_view(['POST'])
def check_visit(request):
    user_id = request.data.get('user_id')
    event_id = request.data.get('event_id')

    user = get_object_or_404(User, id=user_id)
    event = get_object_or_404(Event, id=event_id)

    try:
        visit = Visit.objects.get(user_id=user, event_id=event)
        return Response({'exists': True})
    except Visit.DoesNotExist:
        return Response({'exists': False})


@api_view(['POST'])
def create_visit(request):
    user_id = request.data.get('user_id')
    event_id = request.data.get('event_id')
    message = 'success'

    user = get_object_or_404(User, id=user_id)
    event = get_object_or_404(Event, id=event_id)

    try:
        visit = Visit.objects.create(
            user_id=user,
            event_id=event,
            status=1,
            deleted=False
        )
        return Response({'exists': True})
    except Exception as e:
        return Response({'exists': False})


class VisitDeleteView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        event_id = request.data.get('event_id')
        if not user_id or not event_id:
            return Response({'error': 'user_id and event_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            visit = Visit.objects.get(user_id=user_id, event_id=event_id)
            visit.delete()
            return Response({'exists': False})
        except Visit.DoesNotExist:
            return Response({'error': 'Visit not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def user_favorites(request, user_id):
    # Получаем пользователя по ID
    user = get_object_or_404(User, id=user_id)

    # Получаем все посещения, связанные с пользователем
    visits = UserFavoriteEvents.objects.filter(user_id=user, deleted=False).select_related('event_id')

    # Извлекаем все события, связанные с посещениями и добавляем количество пользователей
    event_ids = visits.values_list('event_id', flat=True)
    event_addresses = EventAddress.objects.filter(event_id__in=event_ids, deleted=False)
    prefetch_addresses = Prefetch('event_event_address', queryset=event_addresses, to_attr='addresses')

    events = Event.objects.filter(id__in=event_ids).annotate(user_count=Count('event_visit')).prefetch_related(
        prefetch_addresses)

    events_data = []
    for event in events:
        full_address = event.addresses[0].full_address if event.addresses else ""
        event_data = {
            "id": event.id,
            "title": event.title,
            "price": event.price,
            "event_type": event.event_type,
            "about": event.about,
            "min_age": event.min_age,
            "quantity": event.quantity,
            "photo_id": event.photo_id.photo.name,
            "date": event.date,
            "is_active": event.is_active,
            "create_date": event.create_date,
            "archive": event.archive,
            "deleted": event.deleted,
            "user_count": event.user_count,
            "full_addresses": full_address
        }
        events_data.append(event_data)

    return JsonResponse(events_data, safe=False)


@api_view(['POST'])
def check_favorite(request):
    user_id = request.data.get('user_id')
    event_id = request.data.get('event_id')

    user = get_object_or_404(User, id=user_id)
    event = get_object_or_404(Event, id=event_id)

    try:
        favorite = UserFavoriteEvents.objects.get(user_id=user, event_id=event)
        return Response({'exists': True})
    except UserFavoriteEvents.DoesNotExist:
        return Response({'exists': False})


@api_view(['POST'])
def create_favorite(request):
    user_id = request.data.get('user_id')
    event_id = request.data.get('event_id')
    message = 'success'

    user = get_object_or_404(User, id=user_id)
    event = get_object_or_404(Event, id=event_id)

    try:
        favorite = UserFavoriteEvents.objects.create(
            user_id=user,
            event_id=event,
            deleted=False
        )
        return Response({'exists': True})
    except Exception as e:
        print(e)
        return Response({'exists': False})


class FavoriteDeleteView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        event_id = request.data.get('event_id')
        if not user_id or not event_id:
            return Response({'error': 'user_id and event_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            favorite = UserFavoriteEvents.objects.get(user_id=user_id, event_id=event_id)
            favorite.delete()
            return Response({'exists': False})
        except UserFavoriteEvents.DoesNotExist:
            return Response({'error': 'Visit not found'}, status=status.HTTP_404_NOT_FOUND)
