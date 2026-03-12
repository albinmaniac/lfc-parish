from django.urls import path
from .views import (
    ParishGroupListView,
    ParishGroupCreateView,
    ParishGroupUpdateView,
    ParishGroupDeleteView,
    ParishGroupDetailView,
)

urlpatterns = [
    path("", ParishGroupListView.as_view(), name="group_list"),
    path("add/", ParishGroupCreateView.as_view(), name="group_add"),
    path("<int:pk>/edit/", ParishGroupUpdateView.as_view(), name="group_edit"),
    path("<int:pk>/delete/", ParishGroupDeleteView.as_view(), name="group_delete"),
    path("<int:pk>/", ParishGroupDetailView.as_view(), name="group_detail"),
    path("<int:pk>/edit/", ParishGroupUpdateView.as_view(), name="group_edit"),
]
