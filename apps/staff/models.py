from django.db import models
from django.utils import translation
from parler.models import TranslatableModel, TranslatedFields
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _


class Employee(TranslatableModel):
    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employee")

    GENDER_CHOICES = (("male", _("Male")), ("female", _("Female")))
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    middle_name = models.CharField(_("Middle Name"), max_length=50)
    photo = models.ImageField(_("Photo"), upload_to="employee_images/")
    birthday = models.DateField(_("Birthday"))
    gender = models.CharField(_("Gender"), choices=GENDER_CHOICES, max_length=20)
    translations = TranslatedFields(biography=RichTextUploadingField(_("Biography")))

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"


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

    type = models.ForeignKey(OrganizationType, on_delete=models.SET_NULL, null=True)
    translations = TranslatedFields(
        name=models.CharField(_("Organization Name"), max_length=100)
    )

    def __str__(self):
        return self.name


class RewardType(TranslatableModel):
    class Meta:
        verbose_name = _("Reward Type")
        verbose_name_plural = _("Reward Types")

    translations = TranslatedFields(name=models.CharField(_("Name"), max_length=100))

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
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type = models.ForeignKey(RewardType, on_delete=models.SET_NULL, null=True)
    issued_by = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    date_of_issue = models.DateField()

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
