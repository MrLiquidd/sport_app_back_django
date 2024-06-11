# Generated by Django 5.0.4 on 2024-06-07 16:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_userfavoriteevents'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfavoriteevents',
            unique_together={('user_id', 'event_id')},
        ),
        migrations.AlterUniqueTogether(
            name='visit',
            unique_together={('user_id', 'event_id')},
        ),
    ]