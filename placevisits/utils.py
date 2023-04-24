import certifi
import decimal
import geopy.geocoders
import os
import ssl
import datetime
import pytz

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from math import radians, cos, sin, asin, sqrt
from timezonefinder import TimezoneFinder


ctx = ssl._create_unverified_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
locator = Nominatim(scheme='https', user_agent='2travelplanner' ,timeout=3)
obj = TimezoneFinder()

def get_latlng(latlng):
    if latlng == None:
        return
    if latlng > 1800000000:
        latlng -= 4294967296
    return float(round(decimal.Decimal(latlng)/10000000, 8))

def get_country(latitude, longitude):
    country = ''
    if latitude and longitude:
        try:
            ll = f"{latitude},{longitude}"
            location = locator.reverse(ll, language="en")
            country = location.raw.get('address').get('country')
        except GeocoderTimedOut as error_message:
            country = 'error'
            print("Error: geocode failed on input %s with message %s"%(ll, error_message))
             
    return country

def haversine(place1, place2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1 = place1.latitude
    lng1 = place1.longitude
    lat2 = place2.latitude
    lng2 = place2.longitude
    ll = [lng1, lat1, lng2, lat2]
    if None in ll:
        return None
    lng1, lat1, lng2, lat2 = map(radians, ll)

    # haversine formula 
    dlon = lng2 - lng1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 6371 for kms. Determines return value units.
    return c * r

def list_file_names(path_to_json, json_files_list):
    for pos_json in os.listdir(path_to_json):
        path = os.path.join(path_to_json, pos_json)
        if os.path.isdir(path):
            list_file_names(path, json_files_list)
        else:
            if path.endswith('.json'):
                json_files_list.append(path)

def get_time_duration_string(timedelta):
    days = timedelta.days
    seconds = timedelta.seconds
    minutes = round(seconds / 60)
    hours = round(minutes / 60)
    if days >= 1:
        return "{days} days".format(
                    days=days,
                    hours=hours
                )
    else:
        if hours >= 1:
            return "{hours} hours".format(
                        hours=hours,
                        minutes=minutes
                    )
        else:
            return "{minutes} minutes".format(minutes=minutes)

def get_datetime_local_time(dt, tz):
    timezone = pytz.timezone(tz)
    return dt + timezone.utcoffset(dt)

def get_timezone(lat, lng):
    return obj.timezone_at(lng=lng, lat=lat)

