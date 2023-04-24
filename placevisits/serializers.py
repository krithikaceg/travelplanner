from placevisits.models import PlaceVisit, Trip, Place
from rest_framework import serializers
from .utils import get_country, get_timezone


class PlaceSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)
    google_place_id = serializers.CharField(required=False, allow_blank=True, max_length=500)
    address = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    name = serializers.CharField(required=False, allow_blank=True, max_length=500)
    country = serializers.CharField(required=False, allow_blank=True, default='', max_length=100)
    is_private_place = serializers.BooleanField(default=True)

    class Meta:
        model = Place
        fields = ['id', 
                  'latitude', 
                  'longitude', 
                  'google_place_id',
                  'address',
                  'name',
                  'country',
                  'is_private_place'
                  ]
        
class PlaceVisitSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    visited_time_start = serializers.DateTimeField(required=False)
    visited_time_end = serializers.DateTimeField(required=False)
    place = PlaceSerializer() 

    class Meta:
        model = PlaceVisit
        fields = ['id', 
                  'visited_time_start', 
                  'visited_time_end',
                  'place'
                  ]
    
    def create(self, validated_data):
        place_data = validated_data.pop('place')
        # need to ensure that lat,lng determines the unique id
        # should not create duplicate place
        try:
            place = Place.objects.get(google_place_id = place_data.get('google_place_id'))
        except Place.DoesNotExist:
            # TODO get country here
            lat = place_data.get('latitude')
            lng = place_data.get('longitude')
            country = get_country(lat, lng)
            place_data['country'] = country
            place_data['timezone'] = get_timezone(lat, lng)
            place = Place.objects.create(**place_data)
        
        pv = PlaceVisit.objects.create(place = place, 
                                       **validated_data)
        return pv
    

class TripSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    places_visited = PlaceVisitSerializer(many=True, read_only=True) 
    duration = serializers.IntegerField()
    country = serializers.CharField(required=False, allow_null=True, max_length=100)
    score = serializers.FloatField(required=False, allow_null=True)
    is_private_trip = serializers.BooleanField(default=True)

    class Meta:
        model = Trip
        fields = ['id', 
                  'start_date', 
                  'end_date',
                  'places_visited',
                  'duration',
                  'country',
                  'score',
                  'is_private_trip'
                  ]
