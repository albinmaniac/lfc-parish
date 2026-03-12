from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        return (
            self.request.user.is_authenticated and
            self.request.user.role in self.allowed_roles
        )

    def handle_no_permission(self):
        messages.warning(self.request, "You don't have permission to access this page.")
        return redirect("dashboard")