from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import HttpResponseForbidden
from accounts.mixins import RoleRequiredMixin
from .models import ParishGroup


# ============================
# LIST VIEW
# ============================
class ParishGroupListView(ListView):
    model = ParishGroup
    template_name = "groups/group_list.html"
    context_object_name = "groups"
    ordering = ["name"]

    def get_queryset(self):
        user = self.request.user

        # Admin / Provincial / Staff → see all
        if user.is_authenticated and user.role in ["admin", "provincial", "staff"]:
            return ParishGroup.objects.all()

        # Group leader → only their group
        if user.is_authenticated and user.role == "group_leader":
            return ParishGroup.objects.filter(leader=user)

        # Public → view all
        return ParishGroup.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["can_manage_groups"] = (
            user.is_authenticated and user.role in ["admin", "provincial", "staff"]
        )

        return context
    
    # def dispatch(self, request, *args, **kwargs):
    #     obj = self.get_object()

    #     if request.user.role == "group_leader" and obj.leader != request.user:
    #         return HttpResponseForbidden()

    #     return super().dispatch(request, *args, **kwargs)


# ============================
# DETAIL VIEW (PUBLIC SAFE)
# ============================
class ParishGroupDetailView(DetailView):
    model = ParishGroup
    template_name = "groups/group_detail.html"
    context_object_name = "group"

    def get_queryset(self):
        user = self.request.user
        queryset = ParishGroup.objects.all()

        # Public access allowed
        if not user.is_authenticated:
            return queryset

        if user.role in ["admin", "provincial", "staff"]:
            return queryset

        if user.role == "group_leader":
            return queryset.filter(leader=user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = self.object.members.all()
        return context


# ============================
# CREATE VIEW
# ============================
class ParishGroupCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = ParishGroup
    fields = ["name", "leader", "description", "logo"]
    template_name = "groups/group_form.html"
    success_url = reverse_lazy("group_list")


# ============================
# UPDATE VIEW
# ============================
class ParishGroupUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial", "staff", "group_leader"]

    model = ParishGroup
    fields = ["name", "description", "logo"]
    template_name = "groups/group_form.html"
    success_url = reverse_lazy("group_list")

    def get_queryset(self):
        user = self.request.user

        # Full access roles
        if user.role in ["admin", "provincial", "staff"]:
            return ParishGroup.objects.all()

        # Group leader → only own group
        if user.role == "group_leader":
            return ParishGroup.objects.filter(leader=user)

        return ParishGroup.objects.none()


# ============================
# DELETE VIEW
# ============================
class ParishGroupDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = ParishGroup
    template_name = "groups/group_confirm_delete.html"
    success_url = reverse_lazy("group_list")