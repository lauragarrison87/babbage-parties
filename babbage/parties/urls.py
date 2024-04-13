from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("person/", views.person_list, name="person_list"),
    path("person/<qid>/", views.person_qid, name="person"),
]
