from django.contrib import admin
from .models import PlaceVisit, Place, Trip

admin.site.register(PlaceVisit)
admin.site.register(Place)
admin.site.register(Trip)