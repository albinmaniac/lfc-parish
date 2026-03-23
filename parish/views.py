from django.views.generic import (
    ListView, TemplateView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from accounts.mixins import RoleRequiredMixin
from .models import GalleryImage, Parish, ParishLeader
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms


# ============================
# 🔹 PUBLIC GALLERY
# ============================
class GalleryListView(ListView):
    model = GalleryImage
    template_name = "parish/gallery.html"
    context_object_name = "images"
    ordering = ["-uploaded_at"]

    def get_queryset(self):
        return GalleryImage.objects.filter(is_active=True).order_by("-uploaded_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context["can_manage_gallery"] = (
            user.is_authenticated and
            user.role in ["admin", "provincial", "staff", "group_leader"]
        )

        return context


# ============================
# 🔹 CREATE
# ============================
class GalleryCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial", "staff", "group_leader"]

    model = GalleryImage
    fields = ["title", "image", "is_active"]
    template_name = "parish/gallery_form.html"
    success_url = reverse_lazy("gallery")

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # ✅ tracking only
        return super().form_valid(form)


# ============================
# 🔹 UPDATE (FIXED 🔥)
# ============================
class GalleryUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial", "staff", "group_leader"]

    model = GalleryImage
    fields = ["title", "image", "is_active"]
    template_name = "parish/gallery_form.html"
    success_url = reverse_lazy("gallery")

    # ❌ REMOVED created_by restriction completely


# ============================
# 🔹 DELETE
# ============================
class GalleryDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin"]  # 🔒 or extend if needed

    model = GalleryImage
    template_name = "parish/gallery_confirm_delete.html"
    success_url = reverse_lazy("gallery")


# ============================
# 🔹 ABOUT
# ============================
class AboutView(TemplateView):
    template_name = "parish/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        parish = Parish.objects.first()
        context["parish"] = parish

        user = self.request.user
        context["can_edit_parish"] = (
            user.is_authenticated and
            user.role in ["admin", "provincial", "staff"]
        )

        return context


# ============================
# 🔹 CONTACT
# ============================
class ContactView(TemplateView):
    template_name = "parish/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        parish = Parish.objects.first()
        context["global_parish"] = parish

        context["leaders"] = ParishLeader.objects.filter(is_active=True)

        user = self.request.user
        context["can_manage_leaders"] = (
            user.is_authenticated and
            user.role in ["admin", "provincial","staff"]
        )

        return context


# ============================
# 🔹 PARISH UPDATE
# ============================
class ParishUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = Parish
    fields = [
        "name",
        "about",
        "address",
        "phone",
        "email",
        "mass_timings",
        "logo",
    ]
    template_name = "parish/parish_form.html"
    success_url = reverse_lazy("about")

    def get_object(self):
        parish = Parish.objects.first()
        if not parish:
            parish = Parish.objects.create(name="My Parish")
        return parish


# ============================
# 🔹 LEADER CREATE
# ============================
class ParishLeaderCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = ParishLeader
    fields = ["name", "role", "phone", "photo", "term_start", "term_end", "is_active"]
    template_name = "parish/leader_form.html"
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        parish = Parish.objects.first()
        form.instance.parish = parish
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["term_start"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["term_end"].widget = forms.DateInput(attrs={"type": "date"})

        return form


# ============================
# 🔹 LEADER UPDATE
# ============================
class ParishLeaderUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = ParishLeader
    fields = ["name", "role", "phone", "photo", "term_start", "term_end", "is_active"]
    template_name = "parish/leader_form.html"
    success_url = reverse_lazy("contact")

    # ✅ ADD THIS
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["term_start"].widget.attrs.update({"type": "date"})
        form.fields["term_end"].widget.attrs.update({"type": "date"})
        return form


# ============================
# 🔹 LEADER DELETE
# ============================
class ParishLeaderDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin"]

    model = ParishLeader
    template_name = "parish/leader_confirm_delete.html"
    success_url = reverse_lazy("contact")