from datetime import timedelta

from django.db import models
from django.utils.datetime_safe import datetime

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


class UserSubScription(models.Model):
    user = models.ForeignKey(AppHubUser, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_plan = models.ForeignKey(SubscriptionPlan, null=False, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_payment_date = models.DateTimeField(null=False, blank=False)
    expiry_date = models.DateTimeField(null=False, blank=False)
    is_active = models.BooleanField(default=False)

    @staticmethod
    def get_or_create_free_subscription(user):
        subscription_plan = SubscriptionPlan.objects.get(name="Free")
        try:
            subscription = UserSubScription.objects.get(user=user, subscription_plan=subscription_plan)
        except UserSubScription.DoesNotExist:
            subscription = UserSubScription(user=user, subscription_plan=subscription_plan)
            subscription.last_payment_date = datetime.now()
            subscription.expiry_date = datetime.now() + timedelta(days=30)
            subscription.is_active = True
            subscription.save()
        return subscription

    def __str__(self):
        return self.user.email + " - " + self.subscription_plan.name

    class Meta:
        unique_together = ('user', 'subscription_plan',)


class App(models.Model):
    image = models.ForeignKey(FileModel, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    subscription = models.ForeignKey(UserSubScription, null=False, blank=False, on_delete=models.CASCADE)
    description = models.TextField(null=False)
    metaDescription = models.CharField(max_length=300)
    user = models.ForeignKey(AppHubUser, on_delete=models.CASCADE, related_name='apps')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
