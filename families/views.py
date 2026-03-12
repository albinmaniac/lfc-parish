from django.views.generic import ListView, DetailView,CreateView, UpdateView, DeleteView
from .models import Family, FamilyMember,FamilyUnit
from django.urls import reverse_lazy
from django.shortcuts import redirect,render,get_object_or_404
from accounts.models import IsAdminMixin, IsFamilyHeadMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from django.http import HttpResponseForbidden
from accounts.mixins import RoleRequiredMixin


class FamilyListView(ListView):
    model = Family
    template_name = "families/family_list.html"
    context_object_name = "families"

    def get_queryset(self):
        user = self.request.user
        queryset = Family.objects.all().order_by("house_name")

        # Public users (not logged in)
        if not user.is_authenticated:
            return queryset   # allow viewing all families publicly

        # Role-based filtering
        if user.role in ["admin", "provincial"]:
            pass  # see all

        elif user.role == "unit_president":
            unit = getattr(user, "unit_president", None)
            if unit:
                queryset = queryset.filter(family_unit=unit)
            else:
                queryset = queryset.none()

        elif user.role == "family_head":
            queryset = queryset.filter(family_head=user)

        else:
            queryset = queryset.none()

        # Search filter
        search = self.request.GET.get("q")
        unit_filter = self.request.GET.get("unit")

        if search:
            queryset = queryset.filter(house_name__icontains=search)

        if unit_filter and user.role in ["admin", "provincial"]:
            queryset = queryset.filter(family_unit_id=unit_filter)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context["can_manage_families"] = (
            user.is_authenticated and
            user.role in ["admin", "provincial"]
        )

        return context
        

class FamilyDetailView(DetailView):
    model = Family
    template_name = "families/family_detail.html"
    context_object_name = "family"

    def get_queryset(self):
        user = self.request.user

        if user.role in ["admin", "provincial"]:
            return Family.objects.all()

        if user.role == "unit_president":
            return Family.objects.filter(family_unit=user.unit_president)

        if user.role == "family_head":
            return Family.objects.filter(family_head=user)

        return Family.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = self.object.members.all()
        return context
    

    
class FamilyCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin"]

    model = Family
    fields = ['house_name', 'address', 'family_unit', 'family_head', 'family_photo']
    template_name = "families/family_form.html"
    success_url = reverse_lazy("family_list")


class FamilyUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "unit_president", "family_head"]

    model = Family
    fields = ['house_name', 'address', 'family_photo']
    template_name = "families/family_form.html"
    success_url = reverse_lazy("family_list")

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return Family.objects.all()

        if user.role == "unit_president":
            return Family.objects.filter(family_unit=user.unit_president)

        if user.role == "family_head":
            return Family.objects.filter(family_head=user)

        return Family.objects.none()
    


class FamilyDeleteView(RoleRequiredMixin, DeleteView):
    
    model = Family
    allowed_roles = ["admin"]
    template_name = "families/family_confirm_delete.html"
    success_url = reverse_lazy("family_list")





class FamilyMemberCreateView(LoginRequiredMixin, CreateView):
    model = FamilyMember
    fields = ["name", "photo", "dob", "parish_groups", "is_family_head"]
    template_name = "families/member_form.html"

    def dispatch(self, request, *args, **kwargs):
        family = Family.objects.get(pk=self.kwargs["family_id"])

        # Admin → allowed
        if request.user.role == "admin":
            return super().dispatch(request, *args, **kwargs)

        # Family Head → allowed for their own family
        if family.family_head == request.user:
            return super().dispatch(request, *args, **kwargs)

        # Unit President → only for families inside their unit
        if request.user.role == "unit_president":
            if family.family_unit == getattr(request.user, "unit_president", None):
                return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You are not allowed to add members.")

    def form_valid(self, form):
        family = Family.objects.get(pk=self.kwargs["family_id"])
        form.instance.family = family
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("family_detail", kwargs={"pk": self.kwargs["family_id"]})
    

class FamilyMemberUpdateView(LoginRequiredMixin, UpdateView):
    model = FamilyMember
    fields = ["name", "photo", "dob", "parish_groups", "is_family_head"]
    template_name = "families/member_form.html"

    def dispatch(self, request, *args, **kwargs):
        member = self.get_object()
        family = member.family

        if request.user.role == "admin":
            return super().dispatch(request, *args, **kwargs)

        if family.family_head == request.user:
            return super().dispatch(request, *args, **kwargs)

        if request.user.role == "unit_president":
            if family.family_unit == getattr(request.user, "unit_president", None):
                return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You are not allowed to edit members.")

    def get_success_url(self):
        return reverse_lazy("family_detail", kwargs={"pk": self.object.family.id})


class FamilyMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = FamilyMember
    template_name = "families/member_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        member = self.get_object()
        family = member.family

        if request.user.role == "admin":
            return super().dispatch(request, *args, **kwargs)

        if family.family_head == request.user:
            return super().dispatch(request, *args, **kwargs)

        if request.user.role == "unit_president":
            if family.family_unit == getattr(request.user, "unit_president", None):
                return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You are not allowed to edit members.")

    def get_success_url(self):
        return reverse_lazy("family_detail", kwargs={"pk": self.object.family.id})
    


class MyFamilyView(DetailView):
    model = Family
    template_name = "families/family_detail.html"
    context_object_name = "family"

    def get_object(self):
        return get_object_or_404(Family, family_head=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = self.object.members.all()
        return context
    


class FamilyUnitCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial"]

    model = FamilyUnit
    fields = ["name", "president"]
    template_name = "families/unit_form.html"
    success_url = reverse_lazy("unit_list")


class FamilyUnitUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial"]

    model = FamilyUnit
    fields = ["name", "president"]
    template_name = "families/unit_form.html"
    success_url = reverse_lazy("unit_list")


class FamilyUnitDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin"]

    model = FamilyUnit
    template_name = "families/unit_confirm_delete.html"
    success_url = reverse_lazy("unit_list")

    
class FamilyUnitListView(ListView):
    model = FamilyUnit
    template_name = "families/unit_list.html"
    context_object_name = "units"
    ordering = ["name"]


class FamilyUnitDetailView(DetailView):
    model = FamilyUnit
    template_name = "families/unit_detail.html"
    context_object_name = "unit"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["families"] = self.object.families.all()
        return context