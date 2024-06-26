# Generated by Django 5.0.4 on 2024-06-04 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_remove_userinfo_age_user_born_date'),
        ('utily', '0002_alter_address_flat_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='age',
            field=models.IntegerField(blank=True, default=23, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='born_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='about_me',
            field=models.TextField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='first_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='photo_id',
            field=models.ForeignKey(blank=True, default='3b94b662-3ecf-46cf-9b63-82ab0f12ce72', on_delete=django.db.models.deletion.CASCADE, related_name='file_user_photo_id', to='utily.file'),
        ),
    ]
