from rest_framework import serializers
from AppHub.models import SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)

    class Meta:
        model = SubscriptionPlan
        fields = "__all__"
