from django.contrib import admin
from .models import FamilyUnit, Family, ParishGroup, FamilyMember


class FamilyMemberInline(admin.TabularInline):  # Inline members inside Family
    model = FamilyMember
    extra = 1


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ("house_name", "family_unit", "family_head")
    search_fields = ("house_name", "address")
    list_filter = ("family_unit",)
    inlines = [FamilyMemberInline]


@admin.register(FamilyUnit)
class FamilyUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "president")
    search_fields = ("name",)


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "family", "age", "is_family_head")
    search_fields = ("name", "family__house_name")
    list_filter = ("parish_groups", "is_family_head")
