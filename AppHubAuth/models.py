import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils import timezone
from AppHubAuth.manager.CustomUserManager import CustomUserManager
from AppHubCentral.settings import OTP_EXPIRATION_TIME_IN_MIN


# Create your models here.


# Create your models here.
class FileModel(models.Model):
    file = models.FileField(upload_to='media/files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey("AppHubUser", on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager()

    def filename(self):
        return os.path.basename(self.file.name)

    def size(self):
        return self.file.size

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        super().delete()

    def __str__(self):
        return self.file.name


class AppHubUser(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(_("email address"), unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=100, null=False, blank=False)
    dp = models.ForeignKey(FileModel, null=True, blank=True, on_delete=models.CASCADE)
    REQUIRED_FIELDS = ["full_name", "email",]
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Otp(models.Model):
    code = models.CharField(null=False, max_length=30)
    send_at = models.DateTimeField(null=False, auto_now_add=True)
    expire_at = models.DateTimeField(null=False)
    email = models.EmailField(null=False, unique=True)
    is_used = models.BooleanField(default=False)

    @staticmethod
    def create(code, email):
        Otp.objects.filter(email=email).delete()
        self = Otp()
        self.code = code
        self.email = email
        self.expire_at = timezone.now() + timedelta(minutes=OTP_EXPIRATION_TIME_IN_MIN)
        self.save()
        return self

    def setAsUsed(self):
        self.is_used = True
        self.save()

    def is_expired(self):
        return self.expire_at < timezone.now() or self.is_used

    def __str__(self):
        return self.code + " " + self.email
