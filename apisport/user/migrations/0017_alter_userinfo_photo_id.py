# Generated by Django 5.0.4 on 2024-06-05 02:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_userinfo_deleted'),
        ('utily', '0005_alter_file_photo_alter_file_specs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='photo_id',
            field=models.ForeignKey(blank=True, default='3b94b662-3ecf-46cf-9b63-82ab0f12ce72', on_delete=django.db.models.deletion.PROTECT, related_name='file_user_photo_id', to='utily.file'),
        ),
    ]
