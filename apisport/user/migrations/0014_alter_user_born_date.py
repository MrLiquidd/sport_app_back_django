# Generated by Django 5.0.4 on 2024-06-04 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_user_born_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='born_date',
            field=models.DateField(default='2000-01-01', null=True),
        ),
    ]