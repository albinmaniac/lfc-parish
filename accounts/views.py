from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from families.models import Family, FamilyMember, FamilyUnit
from groups.models import ParishGroup
from notices.models import Notice
from events.models import Event


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context["role"] = user.role

        # Global statistics (visible mostly to admin/provincial)
        context["family_count"] = Family.objects.count()
        context["member_count"] = FamilyMember.objects.count()
        context["unit_count"] = FamilyUnit.objects.count()
        context["group_count"] = ParishGroup.objects.count()
        context["notice_count"] = Notice.objects.filter(is_active=True).count()
        context["event_count"] = Event.objects.filter(is_active=True).count()

        # Unit-specific data
        if user.role == "unit_president":
            if hasattr(user, "unit_president"):
                unit = user.unit_president
                context["my_unit"] = unit
                context["unit_families"] = unit.families.all()

        # Group-specific data
        if user.role == "group_leader":
            if hasattr(user, "led_groups"):
                context["my_groups"] = user.led_groups.all()

        return context