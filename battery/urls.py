from django.urls import path
from . import views

urlpatterns = [
    path('',         views.battery_list,    name='battery-list'),
    path('history/', views.battery_history, name='battery-history'),
]
