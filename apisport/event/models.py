import uuid

from django.db import models

from user.models import User
from utily.models import File, Address


class Event(models.Model):
    TRAINING = 'Тренировки'
    GAME = 'Игры'

    EVENT_TYPE_CHOICES = [
        (TRAINING, 'Тренировка'),
        (GAME, 'Игра'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    price = models.IntegerField(default=350)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default=TRAINING)
    about = models.TextField(max_length=300)
    min_age = models.IntegerField()
    quantity = models.IntegerField()
    photo_id = models.ForeignKey(File, related_name='file_event_photo_id', on_delete=models.PROTECT)
    date = models.DateTimeField()
    is_active = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)
    archive = models.BooleanField()
    deleted = models.BooleanField()

    def __str__(self):
        return self.title


class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, related_name='user_visit', on_delete=models.PROTECT)
    event_id = models.ForeignKey(Event, related_name='event_visit', on_delete=models.PROTECT)
    status = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField()

    class Meta:
        # Уникальный индекс для связки user_id и event_id
        unique_together = ('user_id', 'event_id')

    def __str__(self):
        return f'{self.event_id}'


class UserFavoriteEvents(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, related_name='user_favorite', on_delete=models.PROTECT)
    event_id = models.ForeignKey(Event, related_name='event_favorite', on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField()

    class Meta:
        unique_together = ('user_id', 'event_id')

    def __str__(self):
        return f'{self.user_id}'


class EventAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.ForeignKey(Event, related_name='event_event_address', on_delete=models.PROTECT)
    full_address = models.CharField(max_length=100)
    address = models.ForeignKey(Address, related_name='address_address_event', on_delete=models.PROTECT)
    default = models.BooleanField()
    deleted = models.BooleanField()

    def __str__(self):
        return self.full_address
