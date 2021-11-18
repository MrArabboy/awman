from django.db import models
from django.utils import translation
from django.utils.safestring import mark_safe
from parler.models import TranslatableModel, TranslatedFields
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from django.core.exceptions import ValidationError

GENDER_CHOICES = (("male", _("Male")), ("female", _("Female")))


class SiteInfo(TranslatableModel):
    class Meta:
        verbose_name = _("SiteInfo")
        verbose_name_plural = _("SiteInfo")

    translations = TranslatedFields(
        info=RichTextUploadingField(_("About Site")),
    )

    def __str__(self):
        return f"{self.info[:20]}..."


class OrganizationType(TranslatableModel):
    class Meta:
        verbose_name = _("Organization Type")
        verbose_name_plural = _("Organization Types")

    translations = TranslatedFields(name=models.CharField(_("Name"), max_length=100))

    def __str__(self):
        return self.name


class Organization(TranslatableModel):
    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    type = models.ForeignKey(
        OrganizationType, verbose_name=_("Type"), on_delete=models.SET_NULL, null=True
    )
    translations = TranslatedFields(
        name=models.CharField(_("Organization Name"), max_length=100)
    )

    def __str__(self):
        return self.name


class Position(TranslatableModel):
    class Meta:
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")

    organization = models.ForeignKey(
        Organization,
        verbose_name=_("Organization"),
        on_delete=models.SET_NULL,
        null=True,
    )
    translations = TranslatedFields(
        name=models.CharField(_("Position"), max_length=100)
    )

    def __str__(self):
        return self.name + " in " + self.organization.name


class Nationality(TranslatableModel):
    class Meta:
        verbose_name = _("Nationality")
        verbose_name_plural = _("Nationalities")

    translations = TranslatedFields(
        nation=models.CharField(_("Nationality"), max_length=30)
    )

    def __str__(self):
        return self.nation


class Employee(TranslatableModel):
    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    translations = TranslatedFields(
        first_name=models.CharField(_("First Name"), max_length=50, null=True),
        last_name=models.CharField(_("Last Name"), max_length=50, null=True),
        middle_name=models.CharField(_("Middle Name"), max_length=50, null=True),
        biography=RichTextUploadingField(_("Biography")),
    )

    nationality = models.ForeignKey(
        Nationality, verbose_name=_("Nationality"), on_delete=models.SET_NULL, null=True
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name=_("Organization"),
        on_delete=models.SET_NULL,
        null=True,
    )
    position = ChainedForeignKey(
        Position,
        chained_field="organization",
        chained_model_field="organization",
        auto_choose=True,
        sort=True,
        verbose_name=_("Position"),
        null=True,
    )
    photo = models.ImageField(_("Photo"), upload_to="employee_images/")
    birthday = models.DateField(_("Birthday"))
    gender = models.CharField(_("Gender"), choices=GENDER_CHOICES, max_length=20)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.photo.url))

    image_tag.short_description = "Image"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"


class RewardType(TranslatableModel):
    class Meta:
        verbose_name = _("Reward Type")
        verbose_name_plural = _("Reward Types")

    translations = TranslatedFields(name=models.CharField(_("Name"), max_length=100))
    image = models.ImageField(_("Image"), upload_to="reward_images/", null=True)

    def __str__(self):
        return self.name


class Reward(TranslatableModel):
    class Meta:
        verbose_name = _("Reward")
        verbose_name_plural = _("Rewards")

    translations = TranslatedFields(
        name=models.CharField(_("Reward Name"), max_length=100),
        description=models.TextField(_("Description"), null=True, blank=True),
    )
    employee = models.ForeignKey(
        Employee, verbose_name=_("Employee"), on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        RewardType, verbose_name=_("Type"), on_delete=models.SET_NULL, null=True
    )

    issued_by = models.ForeignKey(
        Organization, verbose_name=_("Issued By"), on_delete=models.SET_NULL, null=True
    )
    date_of_issue = models.DateField(_("Date Of Issue"))

    @property
    def imageUrl(self):
        if self.type.image:
            return self.type.image.url
        else:
            return ""

    def __str__(self):
        return f"{self.type} of {self.employee}"


class RewardFile(TranslatableModel):
    class Meta:
        verbose_name = _("Reward File")
        verbose_name_plural = _("Reward Files")

    translations = TranslatedFields(
        name=models.CharField(_("File Name"), max_length=100),
    )
    reward = models.ForeignKey(
        Reward,
        verbose_name=_("Reward"),
        related_name="files",
        on_delete=models.SET_NULL,
        null=True,
    )
    document = models.FileField(_("File"), upload_to="reward_files/")
