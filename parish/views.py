from django.views.generic import (
    ListView, TemplateView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from accounts.mixins import RoleRequiredMixin
from .models import GalleryImage, Parish


# 🔹 PUBLIC GALLERY
class GalleryListView(ListView):
    model = GalleryImage
    template_name = "parish/gallery.html"
    context_object_name = "images"
    ordering = ["-uploaded_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context["can_manage_gallery"] = (
            user.is_authenticated and
            user.role in ["admin", "provincial", "group_leader"]
        )

        return context


# 🔹 CREATE (Admin + Provincial + Group Leader)
class GalleryCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial", "group_leader"]

    model = GalleryImage
    fields = ["title", "image", "is_active"]
    template_name = "parish/gallery_form.html"
    success_url = reverse_lazy("gallery")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# 🔹 UPDATE (Admin + Provincial + Group Leader)
class GalleryUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial", "group_leader"]

    model = GalleryImage
    fields = ["title", "image", "is_active"]
    template_name = "parish/gallery_form.html"
    success_url = reverse_lazy("gallery")

    def dispatch(self, request, *args, **kwargs):
        image = self.get_object()

        # Admin → full control
        if request.user.role == "admin":
            return super().dispatch(request, *args, **kwargs)

        # Others → only their own uploads
        if image.created_by == request.user:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You cannot edit this image.")


# 🔹 DELETE (Admin only)
class GalleryDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin"]

    model = GalleryImage
    template_name = "parish/gallery_confirm_delete.html"
    success_url = reverse_lazy("gallery")


# 🔹 ABOUT (Public)
class AboutView(TemplateView):
    template_name = "parish/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        parish = Parish.objects.first()
        context["parish"] = parish

        user = self.request.user
        context["can_edit_parish"] = (
            user.is_authenticated and
            user.role in ["admin", "provincial"]
        )

        return context

# 🔹 CONTACT (Public)
from django.views.generic import TemplateView
from .models import Parish, ParishLeader

class ContactView(TemplateView):
    template_name = "parish/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        parish = Parish.objects.first()
        context["global_parish"] = parish

        # ✅ THIS IS IMPORTANT
        context["leaders"] = ParishLeader.objects.filter(is_active=True)

        return context
    

from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from accounts.mixins import RoleRequiredMixin
from .models import Parish
from django.contrib.auth.mixins import LoginRequiredMixin

class ParishUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial"]

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
    success_url = reverse_lazy("home")

    def get_object(self):
        # Always edit the first parish record
        parish = Parish.objects.first()
        if not parish:
            parish = Parish.objects.create(name="My Parish")
        return parish
    


class ParishLeaderCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial"]
    model = ParishLeader
    fields = ["name", "role", "phone", "photo", "term_start", "term_end", "is_active"]
    template_name = "parish/leader_form.html"
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        parish = Parish.objects.first()
        form.instance.parish = parish
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("contact")
    

class ParishLeaderUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial"]
    model = ParishLeader
    fields = ["name", "role", "phone", "photo", "term_start", "term_end", "is_active"]
    template_name = "parish/leader_form.html"
    success_url = reverse_lazy("contact")  
    def get_success_url(self):
        return reverse_lazy("contact") # ✅ Redirect here


class ParishLeaderDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin"]

    model = ParishLeader
    template_name = "parish/leader_confirm_delete.html"
    success_url = reverse_lazy("contact")