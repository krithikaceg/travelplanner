# Generated by Django 3.2.18 on 2023-03-29 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placevisits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='country',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]