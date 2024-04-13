from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("person/", views.person_list, name="person_list"),
    path("person/<qid>/", views.person_qid, name="person"),
    path("api/get_visdata", views.get_visdata_by_person, name="get_visdata"),
    path("balloon", views.balloon, name="balloon"),
    path("api/balloon", views.api_balloon, name="api_balloon"),
]

