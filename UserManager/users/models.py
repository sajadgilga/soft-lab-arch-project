from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your views here.

phone_number_validator = RegexValidator(r'^[0-9]*$', 'Only phone_numbers are allowed.')


class User(AbstractUser):
    class Roles(models.IntegerChoices):
        ADMIN = 0, _('admin')
        CLIENT = 1, _('client')

    phone = models.CharField(validators=[phone_number_validator], max_length=11)
    role = models.IntegerField(choices=Roles.choices, default=Roles.CLIENT)
