from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from accounts.mixins import RoleRequiredMixin
from .models import ParishGroup


# 🔹 LIST VIEW
class ParishGroupListView(ListView):
    model = ParishGroup
    template_name = "groups/group_list.html"
    context_object_name = "groups"
    ordering = ["name"]

    def get_queryset(self):
        user = self.request.user

        # Admin & Provincial → see all
        if user.is_authenticated and user.role in ["admin", "provincial"]:
            return ParishGroup.objects.all()

        # Group leader → only their group
        if user.is_authenticated and user.role == "group_leader":
            return ParishGroup.objects.filter(leader=user)

        # Public users → can view all (if groups are public)
        return ParishGroup.objects.all()


# 🔹 DETAIL VIEW
class ParishGroupDetailView(DetailView):
    model = ParishGroup
    template_name = "groups/group_detail.html"
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = self.object.members.all()
        return context


# 🔹 CREATE VIEW (Admin only)
class ParishGroupCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin"]

    model = ParishGroup
    fields = ["name", "leader", "description", "logo"]  # added logo
    template_name = "groups/group_form.html"
    success_url = reverse_lazy("group_list")


# 🔹 UPDATE VIEW (Admin + Group Leader)
class ParishGroupUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "group_leader"]

    model = ParishGroup
    fields = ["name", "description", "logo"]   # Leader should not change leader
    template_name = "groups/group_form.html"
    success_url = reverse_lazy("group_list")

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return ParishGroup.objects.all()

        if user.role == "group_leader":
            return ParishGroup.objects.filter(leader=user)

        return ParishGroup.objects.none()


# 🔹 DELETE VIEW (Admin only)
class ParishGroupDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin"]

    model = ParishGroup
    template_name = "groups/group_confirm_delete.html"
    success_url = reverse_lazy("group_list")