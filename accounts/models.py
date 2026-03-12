from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Father'),
        ('staff', 'Parish Staff'),   
        ('family_head', 'Family Head'),
        ('unit_president', 'Family Unit President'),
        ('group_leader', 'Group Leader'),
        ('provincial', 'Provincial'),
        ('user', 'User'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    

from django.contrib.auth.mixins import UserPassesTestMixin

class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == "admin"

class IsFamilyHeadMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ["admin", "family_head"]