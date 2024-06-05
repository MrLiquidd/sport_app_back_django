import uuid

from django.db import models


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=155, blank=False)
    photo = models.ImageField(upload_to="images/", blank=True)
    specs = models.FileField(upload_to="files/", blank=True)

    def __str__(self):
        return self.title


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=255)
    city = models.ForeignKey('City', related_name='city_address', on_delete=models.PROTECT)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)
    flat_number = models.CharField(max_length=10, blank=True)
    default = models.BooleanField()
    deleted = models.BooleanField()

    def __str__(self):
        return self.street


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=255)
    deleted = models.BooleanField()

    def __str__(self):
        return self.city
