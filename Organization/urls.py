from django.urls import path
from . import views

urlpatterns = [
    path('get-location/', views.get_location, name='get_location'),
    path('requests/', views.requests_view, name='requests'),
    path('accepted_requests/', views.accepted_requests, name='accepted_requests'),
    path('route/', views.route_view, name='route'),
    path('receiver_profile/', views.profile_view, name='receiver_profile'),
    path('accept_request/<int:report_id>/', views.accept_request, name='accept_request'),
    path('send-notification/', views.send_notification_whatsapp, name='send_notification'),
    
    
]
