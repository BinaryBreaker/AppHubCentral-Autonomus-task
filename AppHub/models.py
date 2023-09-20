from django.db import models
from AppHubAuth.models import AppHubUser, FileModel


# Create your models here.


class SubscriptionPlan(models.Model):
    price = models.FloatField(null=False)
    name = models.CharField(max_length=200, null=False, unique=True)
    description = models.TextField(null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class App(models.Model):
    image = models.ForeignKey(FileModel, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    subScriptionPlan = models.ForeignKey(SubscriptionPlan, null=False, blank=False, on_delete=models.CASCADE)
    description = models.TextField(null=False)
    metaDescription = models.CharField(max_length=300)
    user = models.ForeignKey(AppHubUser, on_delete=models.CASCADE, related_name='apps')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
