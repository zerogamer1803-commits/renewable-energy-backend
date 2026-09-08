from django.urls import path
from . import views

urlpatterns = [
    path('',         views.street_light_list,    name='street-light-list'),
    path('history/', views.street_light_history, name='street-light-history'),
    path('faults/',  views.fault_list,           name='fault-list'),
]
