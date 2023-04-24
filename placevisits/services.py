from placevisits.models import PlaceVisit, Place, Trip
from placevisits.utils import get_country, haversine

def get_countries_travelled():
    countries = Place.objects.values_list('country', flat=True)
    return list(filter(lambda x: x != '', set(countries)))

def generate_trips():
    # for every user
    places_visited = PlaceVisit.objects.order_by('visited_time_start')
    trip = {}
    trip['places'] = []
    start_place = places_visited[0]
    trip['start_date'] = start_place.visited_time_start
    
    for prev_place_visited, next_place_visited in zip(places_visited, places_visited[1:]):

        if is_different_trip(prev_place_visited, next_place_visited) :
            # conclude the previous trip
            trip['places'].append(prev_place_visited.id)
            trip['end_date'] = prev_place_visited.visited_time_end
            trip['duration'] = (trip['end_date'] - trip['start_date']).days + 1
            
            # trip['country'] = get_country(prev_place_visited.place.latitude, prev_place_visited.place.longitude) or ''
            
            places_visited_in_this_trip = PlaceVisit.objects.filter(id__in=trip['places'])
            countries = list(places_visited_in_this_trip.values_list('place__country', flat=True)
                             .distinct()
                             .order_by())
            countries = [x for x in countries if x != '']
            if len(countries) > 0:
                trip['country'] = countries[0]
            else:
                trip['country'] = ''
            score = trip_score(places_visited_in_this_trip)
            is_private_trip = score < 0.4
            t = Trip(start_date=trip['start_date'], 
                     end_date=trip['end_date'], 
                     duration = trip['duration'], 
                     country=trip['country'],
                     score=score,
                     is_private_trip=is_private_trip
                    )
            t.save()
            t.places_visited.add(*list(places_visited_in_this_trip))
            # Can we serialize this data and save the trips in bulk instead of saving them individually?
            # trips.append(trip)
            # Create a new trip
            trip = {}
            trip['places'] = []
            trip['start_date'] = next_place_visited.visited_time_start
        else:
            trip['places'].append(prev_place_visited.id)
            
    # Conclude the last trip
    # code logic repeated - needs refactoring
    last_place_visited = places_visited.last()
    trip['places'].append(last_place_visited.id)
    trip['end_date'] = last_place_visited.visited_time_end
    trip['duration'] = (trip['end_date'] - trip['start_date']).days + 1
    trip['country'] = get_country(last_place_visited.place.latitude, last_place_visited.place.longitude)
    places_visited_in_this_trip = PlaceVisit.objects.filter(id__in=trip['places'])
    
    score = trip_score(places_visited_in_this_trip)
    is_private_trip = score < 0.4

    t = Trip(start_date=trip['start_date'], 
                     end_date=trip['end_date'], 
                     duration = trip['duration'], 
                     country=trip['country'],
                     score=score,
                     is_private_trip=is_private_trip
            )
    t.save()
    
    t.places_visited.add(*list(places_visited_in_this_trip))

def trip_score_1(places_visited_in_this_trip):
    public_places_visited_in_this_trip = places_visited_in_this_trip.filter(place__is_private_place=False)
    return float(public_places_visited_in_this_trip.count()/places_visited_in_this_trip.count())

def trip_score_2(places_visited_in_this_trip):
    #implementing the logic for obtaining score
    private_pv_duration = visited_duration_in_minutes(places_visited_in_this_trip.filter(place__is_private_place=True))
    pub_pv_duration = visited_duration_in_minutes(places_visited_in_this_trip.filter(place__is_private_place=False))
    total_duration = private_pv_duration + pub_pv_duration
    
    # trip lesser than a day are given zero score
    if total_duration < (24 * 60):
        return 0
    return round(pub_pv_duration/(total_duration), 2)

def visited_duration_in_minutes(places_visited_in_this_trip):
    duration = 0
    for pv in places_visited_in_this_trip:
        duration += float((pv.visited_time_end - pv.visited_time_start).seconds / 60)
    return duration

def trip_score(places_visited_in_this_trip):
    return trip_score_2(places_visited_in_this_trip)

def is_different_trip(prev_place_visited, current_place_visited):
    # if the places travelled are more than one day apart, they are considered different trips
    if (current_place_visited.visited_time_start.date() - prev_place_visited.visited_time_end.date()).days > 1:
        return True
    hav = haversine(prev_place_visited.place, current_place_visited.place)
    if hav and hav > 40:
        return True
                
    return False
