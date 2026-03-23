from django.utils.timezone import now
from notices.models import Notice
from events.models import Event

def notification_counts(request):
    user = request.user

    if not user.is_authenticated:
        return {}

    last_seen_notices = user.last_seen_notices or user.date_joined
    last_seen_events = user.last_seen_events or user.date_joined

    return {
        "new_notices_count": Notice.objects.filter(
            created_at__gt=last_seen_notices
        ).count(),

        "new_events_count": Event.objects.filter(
            created_at__gt=last_seen_events
        ).count(),
    }