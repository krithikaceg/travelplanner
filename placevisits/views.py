import datetime

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from placevisits.models import PlaceVisit, Trip
from placevisits.serializers import PlaceVisitSerializer, TripSerializer
from placevisits.utils import get_time_duration_string, get_datetime_local_time

@csrf_exempt
def placevisit_list(request):
    """
    List all place visits
    """
    if request.method == 'GET':
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        placeVisits = PlaceVisit.objects.all()
        if date_start != None and date_end != None:
            week_start = datetime.datetime.strptime(date_start, "%m-%d-%Y").date().isocalendar()[1]
            week_end = datetime.datetime.strptime(date_end, "%m-%d-%Y").date().isocalendar()[1]
            placeVisits = placeVisits.filter(
                visited_time_start__week__range = (week_start, week_end))
        serializer = PlaceVisitSerializer(placeVisits, many=True)
        return JsonResponse(serializer.data, safe=False)
    
@csrf_exempt
def trip_list(request):
    """
    List all place visits
    """
    if request.method == 'GET':
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        trips = Trip.objects.all()
        if date_start != None and date_end != None:
            week_start = datetime.datetime.strptime(date_start, "%m-%d-%Y").date().isocalendar()[1]
            week_end = datetime.datetime.strptime(date_end, "%m-%d-%Y").date().isocalendar()[1]
            # Need to handle the case when the time interval falls through new year
            trips = trips.filter(start_date__week__range = (week_start, week_end))
        serializer = TripSerializer(trips, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def get_non_private_trip_list(request):
    """
    List all place visits
    """
    if request.method == 'GET':
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        trips = Trip.objects.filter(
                is_private_trip=False
                )
        if date_start != None and date_end != None:
            week_start = datetime.datetime.strptime(date_start, "%m-%d-%Y").date().isocalendar()[1]
            week_end = datetime.datetime.strptime(date_end, "%m-%d-%Y").date().isocalendar()[1]
            # Need to handle the case when the time interval falls through new year
            trips = trips.filter(
                start_date__week__range = (week_start, week_end)
                )
        trips = trips.order_by('-start_date')
        serializer = TripSerializer(trips, many=True)
        return JsonResponse(serializer.data, safe=False)
    
@csrf_exempt
def trip_details(request, trip_id):
    if request.method == 'GET':
        trip = Trip.objects.get(id=trip_id)

        # Not generating itinerary for private trip
        if trip.is_private_trip:
            res_json = {
                "id": trip_id,
                "itinerary" : [],
                "start_date" : '',
                "end_date": '',
                "duration": '',
                "country": '',
                "is_private_trip": trip.is_private_trip,
            }
            return JsonResponse(res_json, safe=False)
        public_places_visited = trip.places_visited.filter(place__is_private_place=False)
        start_dtt = public_places_visited[0].visited_time_start
        time_zone = public_places_visited[0].place.time_zone
        # start_dtt_local = get_datetime_local_time(start_dtt, time_zone)
        complete_itinerary = {}

        for pv in public_places_visited:
            name = pv.place.name
            time_duration = pv.visited_time_end - pv.visited_time_start
            time_duration_str = get_time_duration_string(time_duration)
            address = pv.place.address
            day = (pv.visited_time_start - start_dtt).days + 1
            # day = (get_datetime_local_time(pv.visited_time_start, time_zone) - start_dtt_local).days + 1
            itinerary = {   "name": name,
                            "address": address,
                            "time": time_duration_str,
                            "day" : day,
                        }
            if day in complete_itinerary.keys():
                complete_itinerary[day].append(itinerary)
            else:
                complete_itinerary[day] = [itinerary]
            
            # complete_itinerary.append(itinerary)
            result = [{ "day": key, "day_itinerary": complete_itinerary[key]} for key in complete_itinerary.keys() ]
        
        res_json = {
            "id": trip_id,
            "itinerary" : result,
            "start_date" : trip.start_date,
            "end_date": trip.end_date,
            "duration": trip.duration,
            "country": trip.country,
            "is_private_trip": trip.is_private_trip,
        }
        
        return JsonResponse(res_json, safe=False)

