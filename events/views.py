from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from accounts.mixins import RoleRequiredMixin
from .models import Event
from .forms import EventForm
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now

# ============================
# 🔹 LIST (PUBLIC)
# ============================



class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.filter(is_active=True).order_by("date")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_seen_events = now()  # ✅ FIXED
            request.user.save(update_fields=["last_seen_events"])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        events = context["events"]

        for event in events:
            if event.date == today:
                event.tag = "today"
            elif event.date == tomorrow:
                event.tag = "tomorrow"
            elif event.date < today:
                event.tag = "past"
            else:
                event.tag = "upcoming"

        context["today"] = today
        context["can_manage_events"] = (
            self.request.user.is_authenticated and
            self.request.user.role in ["admin", "provincial", "staff"]
        )

        return context


# ============================
# 🔹 DETAIL (PUBLIC)
# ============================
class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["can_manage_events"] = (
            user.is_authenticated and user.role in ["admin", "provincial", "staff"]
        )
        return context


# ============================
# 🔹 CREATE
# ============================
class EventCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy("event_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # ✅ keep for tracking
        return super().form_valid(form)


# ============================
# 🔹 UPDATE (FIXED ✅)
# ============================
class EventUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ["admin", "provincial", "staff"]

    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy("event_list")


# ============================
# 🔹 DELETE
# ============================
class EventDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ["admin"]   # 🔒 keep strict OR change to include provincial

    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("event_list")