# Generated by Django 5.0.4 on 2024-06-01 14:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userinfo_age'),
        ('utily', '0002_alter_address_flat_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='city',
            field=models.ForeignKey(blank=True, default='9f39b0d5-c4a2-46f8-8005-781a187ac29d', on_delete=django.db.models.deletion.CASCADE, related_name='user_city', to='utily.city'),
        ),
    ]
