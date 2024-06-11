import uuid

from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from utily.models import File, Address, City
from django.contrib.auth.base_user import AbstractBaseUser


class CustomUserManager(UserManager):
    def _create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    password = models.CharField(max_length=255)
    username = models.CharField(blank=True, default='')
    mobile = models.CharField(max_length=50, blank=False, null=True, default='')
    gender = models.CharField(max_length=20,  blank=False, null=True, default='')
    born_date = models.DateField(blank=False, null=True, default='2000-01-01')

    create_date = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class UserInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.OneToOneField(User, on_delete=models.PROTECT, blank=False)
    first_name = models.CharField(max_length=30, blank=True, default='')
    last_name = models.CharField(max_length=30, blank=True, default='')
    about_me = models.TextField(max_length=150, blank=True, default='')
    age = models.IntegerField(default=0, null=True, blank=True)
    photo_id = models.ForeignKey(File, related_name='file_user_photo_id', on_delete=models.PROTECT, blank=True,
                                 default='3b94b662-3ecf-46cf-9b63-82ab0f12ce72')
    city = models.ForeignKey(City, related_name='user_city', on_delete=models.CASCADE, blank=True,
                             default='9f39b0d5-c4a2-46f8-8005-781a187ac29d')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


class UserAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, related_name='user_user_address', on_delete=models.PROTECT, blank=False)
    full_address = models.CharField(max_length=100, blank=True)
    address = models.ForeignKey(Address, related_name='address_user_address', on_delete=models.PROTECT, blank=False)
    default = models.BooleanField()
    deleted = models.BooleanField()

    def __str__(self):
        return self.full_address



class Friends(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, related_name='user_id_friends', on_delete=models.PROTECT)
    friend_id = models.ForeignKey(User, related_name='friend_id_friends', on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField()


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, related_name='user_chat', on_delete=models.PROTECT)
    friend_id = models.ForeignKey(User, related_name='friend_chat', on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField()


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(blank=False)
    user_id = models.ForeignKey(User, related_name='user_message', on_delete=models.PROTECT)
    chat = models.ForeignKey(Chat, related_name='chat_message', on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField()


class MessageFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id = models.ForeignKey(Message, related_name='message_message_file', on_delete=models.PROTECT)
    models.ForeignKey(File, related_name='file_message_file', on_delete=models.PROTECT)
    deleted = models.BooleanField()


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, related_name='user_rating', on_delete=models.PROTECT)
    rate = models.IntegerField()
    deleted = models.BooleanField()
