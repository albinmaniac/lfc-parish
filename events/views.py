from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import HttpResponseForbidden
from accounts.mixins import RoleRequiredMixin
from .models import Event
from .forms import EventForm


# 🔹 LIST (Public)
class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    ordering = ["date"]

    def get_queryset(self):
        return Event.objects.filter(is_active=True)


# 🔹 DETAIL (Public)
class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"


# 🔹 CREATE (Admin + Provincial)
class EventCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial"]

    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy("event_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# 🔹 UPDATE
class EventUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial"]

    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy("event_list")

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()

        # Admin → full control
        if request.user.role == "admin":
            return super().dispatch(request, *args, **kwargs)

        # Provincial → only their own events
        if request.user.role == "provincial" and event.created_by == request.user:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You cannot edit this event.")


# 🔹 DELETE (Admin only)
class EventDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin"]

    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("event_list")