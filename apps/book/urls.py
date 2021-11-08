from django.urls import path
import os
from . import views


app_name = 'book'
urlpatterns = [
    path('', views.index, name="index"),
    path('api/', views.api, name="api"),
]
