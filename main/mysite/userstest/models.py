import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(_("Username"), blank=True, max_length=150, unique=True)
    email = models.EmailField(_("email address"), blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_reset_token(self, length=32):
        """Generates a secure, URL-safe random token."""
        token = secrets.token_urlsafe(length)
        self.resetPasswordTokens.create(value=token)
        return token


class TodoItem(models.Model):
    name = models.CharField(_("Name"), max_length=256, null=False, blank=False)
    is_checked = models.BooleanField(_("Is checked"), default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)


class ResetPasswordToken(models.Model):
    user = models.ForeignKey(CustomUser, related_name='resetPasswordTokens', on_delete=models.CASCADE, null=False, blank=False)
    value = models.CharField(_("Value"), max_length=256, null=False, blank=False)