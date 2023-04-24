from django.urls import path
from placevisits import views

urlpatterns = [
    path('trips/', views.trip_list),
    path('placevisits/', views.placevisit_list),
    path('vacations/', views.get_non_private_trip_list),
    path('trips/<trip_id>', views.trip_details),
]
