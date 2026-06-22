from django.urls import path
from .views import *

urlpatterns = [
    path('',waste_status, name='waste_status' ),
    path('vehicle_details/',vehicle_details, name='vehicle_details' ),
    path('waste_graph/',waste_graph, name='waste_graph' ),
    path('user_recyclers/',user_recyclers, name='user_recyclers' ),
    path('schedule/',schedule, name='schedule' ),
    path('illegal_dumping/',illegal_dumping, name='illegal_dumping' ),
    path('cost_estimation/',cost_estimation, name='cost_estimation' ),
    path('profile/',Profile, name='profile' ),
    path("dumping/<int:pk>/status/", update_dumping_status,
         name="update_dumping_status"),
]
