from django.urls import path
from .views import *

urlpatterns = [
    path('',entry,name='login'),
    path('signup/',sign_up,name='signup'),
    path('logout/', logout_view, name='logout'),
]