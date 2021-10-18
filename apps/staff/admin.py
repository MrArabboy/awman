from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin, TranslatableStackedInline
from .models import (
    Employee,
    Organization,
    OrganizationType,
    RewardType,
    Reward,
    RewardFile,
)


class EmployeeAdmin(TranslatableAdmin):
    fieldsets = (
        (
            _("Nontranslated fields"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "gender",
                    "photo",
                    "birthday",
                ),
            },
        ),
        (
            _("Translated Fields"),
            {
                "fields": ("biography",),
            },
        ),
    )


class OrganizationTypeAdmin(TranslatableAdmin):
    fieldsets = (
        (
            _("Translated Fields"),
            {
                "fields": ("name",),
            },
        ),
    )


class OrganizationAdmin(TranslatableAdmin):
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


class RewardFileAdmin(TranslatableStackedInline):
    model = RewardFile


class RewardAdmin(TranslatableAdmin):
    inlines = [RewardFileAdmin]
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


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(OrganizationType, OrganizationTypeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(RewardType)
admin.site.register(Reward, RewardAdmin)
admin.site.register(RewardFile, RewardFileAdmin2)
