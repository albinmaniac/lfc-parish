from django.urls import path
from .views import (
    EventListView,
    EventCreateView,
    EventUpdateView,
    EventDetailView,
    EventDeleteView,

)

urlpatterns = [
    path("", EventListView.as_view(), name="event_list"),
    path("<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("add/", EventCreateView.as_view(), name="event_add"),
    path("<int:pk>/edit/", EventUpdateView.as_view(), name="event_edit"),
    path("<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
]