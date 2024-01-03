from django.urls import path, re_path
from . import views
from django.conf.urls import include
from rest_framework import routers

app_name = "goals"

urlpatterns = [
    path("", views.goalsList, name="list"),  # GET all goals, POST a new goal
]
