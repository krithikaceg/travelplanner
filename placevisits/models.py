from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# from placevisits.utils import get_country
# from django.db.models.signals import pre_save
from django.dispatch import receiver

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Place(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    google_place_id = models.CharField(max_length=500, blank=True, unique=True)
    # sometimes name is empty. need to handle that.
    name = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=1000, blank=True)
    country = models.CharField(max_length=100, blank=True, default='')
    is_private_place = models.BooleanField(default=True)
    time_zone = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['google_place_id']
        # unique_together = ['google_place_id']

    def __str__(self):
        
        return ("Name: {name}, "
                "Coordinates: ({lat},{lng}), "
                "Country: {country}, ").format(
                name=self.name,
                lat = self.latitude, 
                lng=self.longitude, 
                country=self.country)

class PlaceVisit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    visited_time_start = models.DateTimeField(blank=True)
    visited_time_end = models.DateTimeField(blank=True)
    
    # Need to add as a foreign key once User object is created
    # user_id

    class Meta:
        ordering = ['visited_time_start']

    def __str__(self):
        
        return ("Coordinates: ({lat},{lng}), "
                "country: {country}, "
                "visited time: {start} - {end}").format(
                lat = self.place.latitude, 
                lng=self.place.longitude, 
                country=self.place.country, 
                start= self.visited_time_start.date(),
                end=self.visited_time_end.date())

class Trip(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    places_visited = models.ManyToManyField(PlaceVisit)
    duration = models.IntegerField()
    country = models.CharField(max_length=100, null=True, default='')
    score = models.FloatField(default=0)
    is_private_trip = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_date', 'end_date']

    def __str__(self):
        return ("visited Date: {start_date} - "
        "{end_date} "
        "duration: {duration} "
        "country: {country} "
        "score: {score} "
        "travel:{travel}"
        ).format(
            start_date= self.start_date.date(),
            end_date= self.end_date.date(),
            duration= self.duration,
            country= self.country,
            score=self.score,
            travel=not self.is_private_trip
        )
    
    
    
# @receiver(pre_save, sender=Place)
# def my_callback(sender, instance, *args, **kwargs):
#     if not instance.country:
#         instance.country = get_country(instance.latitude, instance.longitude)
