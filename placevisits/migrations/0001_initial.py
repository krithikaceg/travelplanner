# Generated by Django 3.2.18 on 2023-03-29 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('google_place_id', models.CharField(blank=True, max_length=500, unique=True)),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('address', models.CharField(blank=True, max_length=1000)),
                ('country', models.CharField(blank=True, default='', max_length=100)),
                ('is_private_place', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['google_place_id'],
            },
        ),
        migrations.CreateModel(
            name='PlaceVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('visited_time_start', models.DateTimeField(blank=True)),
                ('visited_time_end', models.DateTimeField(blank=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placevisits.place')),
            ],
            options={
                'ordering': ['visited_time_start'],
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('duration', models.IntegerField()),
                ('country', models.CharField(default='', max_length=100, null=True)),
                ('score', models.FloatField(null=True)),
                ('is_private_trip', models.BooleanField(default=True)),
                ('places_visited', models.ManyToManyField(to='placevisits.PlaceVisit')),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
    ]