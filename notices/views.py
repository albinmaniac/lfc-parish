from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import HttpResponseForbidden
from accounts.mixins import RoleRequiredMixin
from .models import Notice
from django.utils.timezone import now


# ============================
# LIST (PUBLIC)
# ============================
class NoticeListView(ListView):
    model = Notice
    template_name = "notices/notice_list.html"
    context_object_name = "notices"
    ordering = ["-created_at"]

    def get_queryset(self):
        return Notice.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_seen_notices = now()
            request.user.save(update_fields=["last_seen_notices"])  # 🔥 optimized
        return super().get(request, *args, **kwargs)


# 🔹 DETAIL (FIXED ✅)
class NoticeDetailView(DetailView):
    model = Notice
    template_name = "notices/notice_detail.html"
    context_object_name = "notice"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["can_manage_notices"] = (
            user.is_authenticated and user.role in ["admin", "provincial", "staff"]
        )
        return context


# ============================
# CREATE
# ============================
class NoticeCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = Notice
    fields = ["title", "content", "image", "is_active"]
    template_name = "notices/notice_form.html"
    success_url = reverse_lazy("notice_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# ============================
# UPDATE (FIXED 🔥)
# ============================
class NoticeUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = Notice
    fields = ["title", "content", "image", "is_active"]
    template_name = "notices/notice_form.html"
    success_url = reverse_lazy("notice_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Login required")

        if request.user.role in ["admin", "provincial", "staff"]:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You cannot edit this notice.")


# ============================
# DELETE (FIXED 🔥)
# ============================
class NoticeDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = Notice
    template_name = "notices/notice_confirm_delete.html"
    success_url = reverse_lazy("notice_list")