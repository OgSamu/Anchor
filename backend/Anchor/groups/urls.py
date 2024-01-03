from django.urls import path
from . import views

urlpatterns = [
    path("groups/", views.group_list, name="group-list"),
    path("groups/<uuid:pk>/", views.group_detail, name="group-detail"),
]
