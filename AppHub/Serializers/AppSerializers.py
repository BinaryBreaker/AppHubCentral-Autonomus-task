from rest_framework import serializers
from AppHub.models import App, SubscriptionPlan


class AppSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)
    subscription_plan = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.all(),

                                                           required=False,
                                                           allow_null=True)

    def validate_subscription_plan(self, value):
        if value is None:
            try:
                value = SubscriptionPlan.objects.get(name="Free")
            except SubscriptionPlan.DoesNotExist:
                raise serializers.ValidationError("Subscription Plan does not exist.")

        return value

    def validate(self, attrs):
        attrs["subscription_plan"] = self.validate_subscription_plan(attrs.get("subscription_plan", None))
        return attrs

    class Meta:
        model = App
        fields = "__all__"
