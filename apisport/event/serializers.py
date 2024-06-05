from rest_framework import serializers
from event.models import Event, EventAddress


class EventSerializer(serializers.ModelSerializer):
    photo_id = serializers.FileField(source='photo_id.photo', read_only=True)
    full_addresses = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'price', 'event_type', 'about',
                  'min_age', 'quantity', 'photo_id', 'date',
                  'is_active', 'create_date', 'archive', 'deleted',
                  'full_addresses']

    def get_full_addresses(self, obj):
        event_addresses = EventAddress.objects.filter(event_id=obj)
        return [address.full_address for address in event_addresses][0]
