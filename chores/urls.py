from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "complete/<int:occurrence_id>/",
        views.complete_occurrence,
        name="complete_occurrence",
    ),
]