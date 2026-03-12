from django.urls import path
from .views import (
    NoticeListView,
    NoticeCreateView,
    NoticeUpdateView,
    NoticeDeleteView,
)

urlpatterns = [
    path("", NoticeListView.as_view(), name="notice_list"),
    path("add/", NoticeCreateView.as_view(), name="notice_add"),
    path("<int:pk>/edit/", NoticeUpdateView.as_view(), name="notice_edit"),
    path("<int:pk>/delete/", NoticeDeleteView.as_view(), name="notice_delete"),
]