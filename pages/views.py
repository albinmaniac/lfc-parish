from django.views.generic import TemplateView
from notices.models import Notice
from events.models import Event
from .models import CarouselImage
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta

class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Active carousel images
        context["carousel_images"] = (
            CarouselImage.objects
            .filter(is_active=True)
            .order_by("-id")
        )

        # Latest active notice
        context["latest_notice"] = (
            Notice.objects
            .filter(is_active=True)
            .select_related("created_by")
            .order_by("-created_at")
            .first()
        )

        # Upcoming active events (future only)
        

        context["events"] = Event.objects.filter(
            is_active=True,
            date__gte=timezone.localdate()
        ).order_by("date")[:3]

        today = timezone.localdate()

        for event in context["events"]:
            if event.date == today:
                event.tag = "today"
            elif event.date == today + timedelta(days=1):
                event.tag = "tomorrow"
            else:
                event.tag = "upcoming"

        return context