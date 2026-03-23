from django.urls import path
from .views import (
    FamilyListView,
    FamilyDetailView,
    FamilyCreateView,
    FamilyDeleteView,
    FamilyUpdateView,
    FamilyMemberCreateView,
    FamilyMemberDetailView,
    FamilyMemberUpdateView,
    FamilyMemberDeleteView,
    MyFamilyView,FamilyUnitListView,FamilyUnitDetailView,
    FamilyUnitCreateView,
    FamilyUnitUpdateView,
    FamilyUnitDeleteView,
)

urlpatterns = [
    path("", FamilyListView.as_view(), name="family_list"),
    path("<int:pk>/", FamilyDetailView.as_view(), name="family_detail"),
    path("add/", FamilyCreateView.as_view(), name="family_add"),
    path("<int:pk>/edit/", FamilyUpdateView.as_view(), name="family_edit"),
    path("<int:pk>/delete/", FamilyDeleteView.as_view(), name="family_delete"),

    # Member management
    path(
        "family/<int:family_id>/member/add/",
        FamilyMemberCreateView.as_view(),
        name="member_add"
    ),

    path("members/<int:pk>/", FamilyMemberDetailView.as_view(), name="member_detail"),
    path(
        "member/<int:pk>/edit/",
        FamilyMemberUpdateView.as_view(),
        name="member_edit"
    ),
    path(
        "member/<int:pk>/delete/",
        FamilyMemberDeleteView.as_view(),
        name="member_delete"
    ),
    path("my-family/", MyFamilyView.as_view(), name="my_family"),

    path("units/add/", FamilyUnitCreateView.as_view(), name="unit_add"),
    path("units/<int:pk>/edit/", FamilyUnitUpdateView.as_view(), name="unit_edit"),
    path("units/<int:pk>/delete/", FamilyUnitDeleteView.as_view(), name="unit_delete"),
    path("units/", FamilyUnitListView.as_view(), name="unit_list"),
    path("units/<int:pk>/", FamilyUnitDetailView.as_view(), name="unit_detail"),
]