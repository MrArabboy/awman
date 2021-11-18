from ckeditor import fields
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin, TranslatableStackedInline
from .models import (
    Employee,
    Organization,
    OrganizationType,
    Position,
    Nationality,
    RewardType,
    Reward,
    RewardFile,
    SiteInfo,
)


class EmployeeAdmin(TranslatableAdmin):
    list_display = ["__str__", "gender", "birthday", "image_tag"]
    readonly_fields = ["image_tag"]
    search_fields = ["last_name", "first_name", "middle_name", "birthday"]
    list_filter = ["gender"]
    fieldsets = (
        (
            _("Translated Fields"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "biography",
                ),
            },
        ),
        (
            _("Nontranslated fields"),
            {
                "fields": (
                    "gender",
                    "nationality",
                    "organization",
                    "position",
                    "photo",
                    "birthday",
                ),
            },
        ),
    )


class OrganizationTypeAdmin(TranslatableAdmin):
    search_fields = ["translations__name"]
    fieldsets = (
        (
            _("Translated Fields"),
            {
                "fields": ("name",),
            },
        ),
    )


class OrganizationAdmin(TranslatableAdmin):
    list_display = ["name", "type"]
    search_fields = ["type", "name"]
    autocomplete_fields = ["type"]
    list_filter = ["type"]
    fieldsets = (
        (
            _("Nontranslated fields"),
            {
                "fields": ("type",),
            },
        ),
        (
            _("Translated Fields"),
            {
                "fields": ("name",),
            },
        ),
    )


class NationalityAdmin(TranslatableAdmin):
    fieldsets = (
        (
            _("Translated Fields"),
            {
                "fields": ("nation",),
            },
        ),
    )


class PositionAdmin(TranslatableAdmin):
    fieldsets = (
        (
            _("Nontranslated fields"),
            {
                "fields": ("organization",),
            },
        ),
        (
            _("Translated Fields"),
            {
                "fields": ("name",),
            },
        ),
    )


class RewardFileAdmin(TranslatableStackedInline):
    model = RewardFile


class RewardTypeAdmin(TranslatableAdmin):
    search_fields = ["translations__name"]
    fieldsets = (
        (
            _("Translated Fields"),
            {
                "fields": ("name",),
            },
        ),
        (
            _("Nontranslated fields"),
            {"fields": ("image",)},
        ),
    )


class RewardAdmin(TranslatableAdmin):
    list_display = ["employee", "name", "type", "issued_by", "date_of_issue"]
    search_fields = ["employee", "name", "description", "type", "issued_by"]
    autocomplete_fields = ["employee", "type", "issued_by"]
    inlines = [RewardFileAdmin]
    list_filter = ["type"]
    fieldsets = (
        (
            _("Nontranslated fields"),
            {
                "fields": ("employee", "type", "issued_by", "date_of_issue"),
            },
        ),
        (
            _("Translated Fields"),
            {
                "fields": ("name", "description"),
            },
        ),
    )


class RewardFileAdmin2(TranslatableAdmin):
    fieldsets = (
        (
            _("Nontranslated fields"),
            {
                "fields": (
                    "reward",
                    "document",
                ),
            },
        ),
        (
            _("Translated Fields"),
            {
                "fields": ("name",),
            },
        ),
    )


class SiteInfoAdmin(TranslatableAdmin):
    fieldsets = (
        (
            _("Translated Fields"),
            {
                "fields": ("info",),
            },
        ),
    )


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(OrganizationType, OrganizationTypeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(RewardType, RewardTypeAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Nationality, NationalityAdmin)
admin.site.register(SiteInfo, SiteInfoAdmin)
