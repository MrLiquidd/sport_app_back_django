# Generated by Django 5.0.4 on 2024-06-05 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_event_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
