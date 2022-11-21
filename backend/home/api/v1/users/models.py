from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


def image_file(instance, filename):
    return '/'.join(['profile/images', str(instance.id), filename])


class User(AbstractUser):
    # WARNING!
    """
    Some officially supported features of Crowdbotics Dashboard depend on the initial
    state of this User model (Such as the creation of superusers using the CLI
    or password reset in the dashboard). Changing, extending, or modifying this model
    may lead to unexpected bugs and or behaviors in the automated flows provided
    by Crowdbotics. Change it at your own risk.

    This model represents the User instance of the system, login system and
    everything that relates with an `User` is represented by this model.
    """

    # First Name and Last Name do not cover name patterns around the globe.
    phone_number = models.CharField(_("Phone number of user"), unique=True, max_length=255)
    phone_number_verified = models.BooleanField(default=False)
    terms_condition_agree = models.BooleanField(_("Terms and condition agree"), default=False)
    profile_image = models.ImageField(upload_to=image_file, max_length=254, blank=True, null=True)
    verification_code = models.CharField(_("VERIFICATION CODE"), blank=True, null=True, max_length=64)

    REQUIRED_FIELDS = ["phone_number", "first_name", "last_name"]

    @property
    def full_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return reverse("users:crud-detail", kwargs={"phone_number": self.phone_number})
