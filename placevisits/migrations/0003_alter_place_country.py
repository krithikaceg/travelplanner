# Generated by Django 3.2.18 on 2023-03-29 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placevisits', '0002_alter_place_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='country',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
