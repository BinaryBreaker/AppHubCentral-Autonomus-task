from rest_framework import serializers
from AppHub.models import App, UserSubScription, SubscriptionPlan


class AppSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)
    subscription = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.all(),
                                                      required=False,
                                                      allow_null=True)

    def validate_subscription_plan(self, value, user):
        if value is None:
            try:
                value = UserSubScription.get_or_create_free_subscription(user)
            except UserSubScription.DoesNotExist:
                raise serializers.ValidationError("You are not subscribed to any plan.")
        try:
            user_subscription = UserSubScription.objects.get(user=user, is_active=True, subscription_plan=value)
        except UserSubScription.DoesNotExist:
            raise serializers.ValidationError("You are not subscribed to this plan.")
        return user_subscription

    def validate(self, attrs):
        attrs["subscription"] = self.validate_subscription_plan(attrs.get("subscription", None),
                                                                attrs.get("user", None)
                                                                )
        return attrs

    class Meta:
        model = App
        fields = "__all__"
