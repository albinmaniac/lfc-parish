from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Family, FamilyMember, FamilyUnit
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from accounts.mixins import RoleRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages


# ============================
# FAMILY LIST (PUBLIC SAFE)
# ============================
class FamilyListView(ListView):
    model = Family
    template_name = "families/family_list.html"
    context_object_name = "families"

    def get_queryset(self):
        user = self.request.user
        queryset = Family.objects.all().order_by("house_name")

        if not user.is_authenticated:
            return queryset

        if user.role in  ["admin", "provincial", "staff"]:
            return queryset

        if user.role == "unit_president":
            return queryset.filter(family_unit=user.unit_president)

        if user.role == "family_head":
            return queryset.filter(family_head=user)

        return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["can_manage_families"] = (
            user.is_authenticated and user.role in [
                "admin",
                "provincial",
                "staff",
                "unit_president",
                "family_head"
            ]
        )
        return context
    



# ============================
# FAMILY DETAIL (PUBLIC SAFE)
# ============================
from django.contrib import messages
from django.shortcuts import redirect

class FamilyDetailView(DetailView):
    model = Family
    template_name = "families/family_detail.html"
    context_object_name = "family"

    def get_queryset(self):
        user = self.request.user
        queryset = Family.objects.all()

        if not user.is_authenticated:
            return queryset

        if user.role in ["admin", "provincial", "staff"]:
            return queryset

        if user.role == "unit_president":
            return queryset.filter(family_unit=user.unit_president)

        if user.role == "family_head":
            return queryset.filter(family_head=user)

        return queryset.none()

    def get_object(self, queryset=None):
        queryset = self.get_queryset()

        try:
            return queryset.get(pk=self.kwargs["pk"])
        except Family.DoesNotExist:
            messages.warning(
                self.request,
                "You don’t have access to this family."
            )
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # 🔥 Handle no access
        if not self.object:
            return redirect("family_list")  # or "home"

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


# ============================
# FAMILY CRUD
# ============================
from django.contrib.auth import get_user_model

User = get_user_model()


class FamilyCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial", "unit_president", "family_head", "staff"]

    model = Family
    fields = ['house_name', 'address', 'family_unit', 'family_head', 'family_photo']
    template_name = "families/family_form.html"
    success_url = reverse_lazy("family_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        # ✅ Unit President → fixed unit
        if user.role == "unit_president":
            form.fields["family_unit"].initial = user.unit_president
            form.fields["family_unit"].queryset = FamilyUnit.objects.filter(
                pk=user.unit_president.id
            )

        # ✅ Family Head → auto assign himself
        if user.role == "family_head":
            form.fields["family_head"].initial = user
            form.fields["family_head"].queryset = User.objects.filter(id=user.id)

        return form

    def form_valid(self, form):
        user = self.request.user

        # 🔥 Unit President → enforce unit
        if user.role == "unit_president":
            form.instance.family_unit = user.unit_president

        # 🔥 Family Head → enforce ownership
        if user.role == "family_head":
            form.instance.family_head = user

        return super().form_valid(form)


class FamilyUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial", "unit_president", "family_head","staff"]

    model = Family
    fields = ['house_name', 'address', 'family_photo',"family_unit"]
    template_name = "families/family_form.html"
    success_url = reverse_lazy("family_list")

    def get_queryset(self):
        user = self.request.user

        if user.role in ["admin", "provincial","staff"]:
            return Family.objects.all()

        if user.role == "unit_president":
            return Family.objects.filter(family_unit=user.unit_president)

        if user.role == "family_head":
            return Family.objects.filter(family_head=user)

        return Family.objects.none()


class FamilyDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin", "provincial","staff", "unit_president","family_head"]

    model = Family
    template_name = "families/family_confirm_delete.html"
    success_url = reverse_lazy("family_list")


# ============================
# MEMBER CRUD (FIXED 🔥)
# ============================
class FamilyMemberCreateView(LoginRequiredMixin, CreateView):
    model = FamilyMember
    fields = ["name", "photo", "dob", "parish_groups", "is_family_head","relation"]
    template_name = "families/member_form.html"

    def dispatch(self, request, *args, **kwargs):
        family = get_object_or_404(Family, pk=self.kwargs["family_id"])

        if request.user.role in ["admin", "provincial","staff"]:
            return super().dispatch(request, *args, **kwargs)

        if family.family_head == request.user:
            return super().dispatch(request, *args, **kwargs)

        if request.user.role == "unit_president":
            if family.family_unit == request.user.unit_president:
                return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("Not allowed")

    def form_valid(self, form):
        family = get_object_or_404(Family, pk=self.kwargs["family_id"])
        form.instance.family = family
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("family_detail", kwargs={"pk": self.kwargs["family_id"]})
    
# ============================
# MEMBER DETAIL (PUBLIC SAFE)
# ============================
class FamilyMemberDetailView(DetailView):
    model = FamilyMember
    template_name = "families/member_detail.html"
    context_object_name = "member"

    def get_queryset(self):
        # ✅ Allow all users (even anonymous) to view
        return FamilyMember.objects.select_related("family").all()

class FamilyMemberUpdateView(LoginRequiredMixin, UpdateView):
    model = FamilyMember
    fields = ["name", "photo", "dob", "parish_groups", "is_family_head","relation"]
    template_name = "families/member_form.html"

    def dispatch(self, request, *args, **kwargs):
        member = self.get_object()
        family = member.family

        if request.user.role in ["admin", "provincial","staff"]:
            return super().dispatch(request, *args, **kwargs)

        if family.family_head == request.user:
            return super().dispatch(request, *args, **kwargs)

        if request.user.role == "unit_president":
            if family.family_unit == request.user.unit_president:
                return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("Not allowed")

    def get_success_url(self):
        return reverse_lazy("family_detail", kwargs={"pk": self.object.family.id})


class FamilyMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = FamilyMember
    template_name = "families/member_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        member = self.get_object()
        family = member.family

        if request.user.role in ["admin", "provincial","staff"]:
            return super().dispatch(request, *args, **kwargs)

        if family.family_head == request.user:
            return super().dispatch(request, *args, **kwargs)

        if request.user.role == "unit_president":
            if family.family_unit == request.user.unit_president:
                return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("Not allowed")

    def get_success_url(self):
        return reverse_lazy("family_detail", kwargs={"pk": self.object.family.id})


# ============================
# MY FAMILY
# ============================
class MyFamilyView(LoginRequiredMixin, DetailView):
    model = Family
    template_name = "families/family_detail.html"
    context_object_name = "family"

    def get_object(self):
        family = Family.objects.filter(family_head=self.request.user).first()

        if not family:
            messages.info(self.request, "You don't have a family yet. Please create one.")
            return None   # ⚠️ handled in get()

        return family

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # 🔥 If no family → redirect instead of crash
        if not self.object:
            return redirect("family_add")

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = self.object.members.all()
        return context
    


# ============================
# FAMILY UNIT
# ============================
class FamilyUnitCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = FamilyUnit
    fields = ["name", "president"]
    template_name = "families/unit_form.html"
    success_url = reverse_lazy("unit_list")


class FamilyUnitUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = FamilyUnit
    fields = ["name", "president"]
    template_name = "families/unit_form.html"
    success_url = reverse_lazy("unit_list")


class FamilyUnitDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = FamilyUnit
    template_name = "families/unit_confirm_delete.html"
    success_url = reverse_lazy("unit_list")


class FamilyUnitListView(ListView):
    model = FamilyUnit
    template_name = "families/unit_list.html"
    context_object_name = "units"
    ordering = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["can_manage_units"] = (
            user.is_authenticated and user.role in ["admin", "provincial", "staff"]
        )
        return context
    
    def get_queryset(self):
        user = self.request.user

        # ✅ Check authentication FIRST
        if not user.is_authenticated:
            return FamilyUnit.objects.all()  # or .all() if public

        if user.role in ["admin", "provincial", "staff"]:
            return FamilyUnit.objects.all()

        if user.role == "unit_president":
            return FamilyUnit.objects.filter(pk=user.unit_president.id)

        return FamilyUnit.objects.none()


class FamilyUnitDetailView(DetailView):
    model = FamilyUnit
    template_name = "families/unit_detail.html"
    context_object_name = "unit"

    def get_object(self, queryset=None):
        user = self.request.user
        obj = super().get_object(queryset)

        # Admin / Provincial / Staff → full access
        if user.is_authenticated and user.role in ["admin", "provincial", "staff"]:
            return obj

        # Unit President → only their unit
        if user.is_authenticated and user.role == "unit_president":
            if obj.pk == user.unit_president.id:
                return obj

            # ❌ Block access
            success_url = reverse_lazy("unit_list")
            raise PermissionDenied("You cannot access this unit")
        

        # Public → allow (or restrict if needed)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["families"] = self.object.families.all()
        return context