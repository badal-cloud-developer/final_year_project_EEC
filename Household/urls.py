from django.urls import path
from .views import *

urlpatterns = [
    path('',waste_report,name='waste_report'),
    path('illegal_report/',illegal_dumping,name='illegal_report'),
    path('household_profile/',household_profile,name='household_profile'),
    path('household_notification/',household_notification,name='household_notification'),
    path('map_view/',map_view,name='map_view'),
    path('reports/', all_reports, name='all_reports'),
    path('like/<int:report_id>/', like_report, name='like_report'),
    
    
]