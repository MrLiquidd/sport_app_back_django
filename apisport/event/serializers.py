from rest_framework import serializers
from event.models import Event, EventAddress, Visit


class EventSerializer(serializers.ModelSerializer):
    photo_id = serializers.SerializerMethodField()
    full_addresses = serializers.SerializerMethodField()
    user_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'price', 'event_type', 'about',
                  'min_age', 'quantity', 'photo_id', 'date',
                  'is_active', 'create_date', 'archive', 'deleted',
                  'full_addresses', 'user_count']

    def get_photo_id(self, obj):
        return obj.photo_id.photo.name

    def get_full_addresses(self, obj):
        event_addresses = EventAddress.objects.filter(event_id=obj)
        return [address.full_address for address in event_addresses][0]
