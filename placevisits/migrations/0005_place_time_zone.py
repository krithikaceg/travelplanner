# Generated by Django 3.2.18 on 2023-04-14 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placevisits', '0004_auto_20230411_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='time_zone',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]