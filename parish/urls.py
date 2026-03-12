from django.urls import path
from .views import (
    GalleryListView,
    GalleryCreateView,
    GalleryUpdateView,
    GalleryDeleteView,
    AboutView,
    ContactView,ParishUpdateView,ParishLeaderCreateView,ParishLeaderDeleteView,ParishLeaderUpdateView
)

urlpatterns = [
    path("gallery/", GalleryListView.as_view(), name="gallery"),
    path("gallery/add/", GalleryCreateView.as_view(), name="gallery_add"),
    path("gallery/<int:pk>/edit/", GalleryUpdateView.as_view(), name="gallery_edit"),
    path("gallery/<int:pk>/delete/", GalleryDeleteView.as_view(), name="gallery_delete"),

    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("edit/", ParishUpdateView.as_view(), name="parish_edit"),

    path("leaders/add/", ParishLeaderCreateView.as_view(), name="leader_add"),
    path("leaders/<int:pk>/edit/", ParishLeaderUpdateView.as_view(), name="leader_edit"),
    path("leaders/<int:pk>/delete/", ParishLeaderDeleteView.as_view(), name="leader_delete"),

]