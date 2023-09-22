from datetime import timedelta

from django.utils.datetime_safe import datetime
from rest_framework import serializers
from AppHub.models import UserSubScription


class UserSubscriptionPlanSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)
    last_payment_date = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)
    expiry_date = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)

    def create(self, validated_data):
        user = UserSubScription(**validated_data)
        user.last_payment_date = datetime.now()
        user.expiry_date = datetime.now() + timedelta(days=30)
        user.is_active = True
        user.save()
        return user

    class Meta:
        model = UserSubScription
        fields = "__all__"
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=UserSubScription.objects.all(),
                fields=('subscription_plan', 'user'),
                message="User already subscribed to this plan."
            )
        ]
