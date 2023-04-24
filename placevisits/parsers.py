import json

from placevisits.serializers import PlaceVisitSerializer
from placevisits.utils import *

def record_placevisits():
    path_to_json = '../Takeout-krithi/LocationHistory/SemanticLocationHistory/'
    json_files_list = []
    list_file_names(path_to_json, json_files_list)
    print(json_files_list)

    placevisit_list = []

    for f in json_files_list:
        with open(f) as json_file:
            timeline_data = json.load(json_file)
            for timeline in timeline_data['timelineObjects']:
                if "placeVisit" in timeline:
                    longitude = get_latlng(timeline.get('placeVisit').get('location').get('longitudeE7'))
                    latitude = get_latlng(timeline.get('placeVisit').get('location').get('latitudeE7'))
                    address = timeline.get('placeVisit').get('location').get('address')
                    google_place_id = timeline.get('placeVisit').get('location').get('placeId')
                    name = timeline.get('placeVisit').get('location').get('name', '')
                    visited_time_start = timeline.get('placeVisit').get('duration').get('startTimestamp')
                    visited_time_end = timeline.get('placeVisit').get('duration').get('endTimestamp')
                    # country = get_country(latitude, longitude)
                    not_null_but_empty = lambda i : i or ''

                    json_data = { 
                     'place': {
                        'latitude': latitude, 
                        'longitude': longitude, 
                        'google_place_id': not_null_but_empty(google_place_id), 
                        'address': not_null_but_empty(address), 
                        'name': name,
                        'is_private_place': not name,
                        # need to see what's the optimum way of obtaining country in case of repeating places
                        # 'country': not_null_but_empty(country),
                    },
                    'visited_time_start': not_null_but_empty(visited_time_start), 
                    'visited_time_end': not_null_but_empty(visited_time_end),
                    }
                    
                    if json_data != None:
                        placevisit_list.append(json_data)

    serializer = PlaceVisitSerializer(data=placevisit_list, many=True)
    is_valid = serializer.is_valid()
    print("Serializer is {is_valid}".format(is_valid=is_valid))
    if is_valid:
        serializer.save()
    else:
        print("Serializer error: {error}".format(error=serializer.errors))


