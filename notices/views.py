from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from accounts.mixins import RoleRequiredMixin
from .models import Notice


# 🔹 LIST (Public)
class NoticeListView(ListView):
    model = Notice
    template_name = "notices/notice_list.html"
    context_object_name = "notices"
    ordering = ["-created_at"]

    def get_queryset(self):
        return Notice.objects.filter(is_active=True)


# 🔹 DETAIL (Public)
class NoticeDetailView(DetailView):
    model = Notice
    template_name = "notices/notice_detail.html"
    context_object_name = "notice"


# 🔹 CREATE (Admin + Provincial)
class NoticeCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial"]

    model = Notice
    fields = ["title", "content", "image", "is_active"]
    template_name = "notices/notice_form.html"
    success_url = reverse_lazy("notice_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# 🔹 UPDATE
class NoticeUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial"]

    model = Notice
    fields = ["title", "content", "image", "is_active"]
    template_name = "notices/notice_form.html"
    success_url = reverse_lazy("notice_list")

    def dispatch(self, request, *args, **kwargs):
        notice = self.get_object()

        # Admin → full control
        if request.user.role == "admin":
            return super().dispatch(request, *args, **kwargs)

        # Provincial → only their own notices
        if request.user.role == "provincial" and notice.created_by == request.user:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You cannot edit this notice.")


# 🔹 DELETE (Admin only)
class NoticeDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin"]

    model = Notice
    template_name = "notices/notice_confirm_delete.html"
    success_url = reverse_lazy("notice_list")