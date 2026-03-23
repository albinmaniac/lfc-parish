from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.role in self.allowed_roles

    def handle_no_permission(self):
        user = self.request.user

        # 🔐 Not logged in → go to login
        if not user.is_authenticated:
            messages.warning(self.request, "Please login to continue.")
            return redirect("login")   # make sure this URL exists

        # 🚫 Logged in but no permission
        messages.warning(self.request, "You don't have permission to access this page.")
        return redirect("home")