# Generated by Django 5.0.4 on 2024-06-04 18:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_user_born_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
