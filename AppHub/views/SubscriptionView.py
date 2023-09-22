from rest_framework import status

from AppHubAuth.other.CustomJsonResponse import CustomJsonResponse
from .BaseView import MetaBaseListView, BaseView
from AppHub.Serializers.SubscriptionPlanSerializers import SubscriptionPlanSerializer, SubscriptionPlan
from AppHub.Serializers.UserSubscriptionSearilizer import UserSubScription, UserSubscriptionPlanSerializer
from AppHub.models import App


class MetaSubscriptionView(MetaBaseListView):
    serializer_class = SubscriptionPlanSerializer
    Model = SubscriptionPlan

    def get_queryset(self):
        return self.Model.objects.all().order_by('-id')


class UserSubscriptionView(BaseView):
    Model = UserSubScription
    model_name = "User Subscription"
    serializer_class = UserSubscriptionPlanSerializer
    allowed_methods = ["post", "delete"]

    def delete(self, request, *args, **kwargs):
        data = request.data
        subscription_plan_id = data.get("subscription_plan_id", None)
        if subscription_plan_id is None:
            return CustomJsonResponse({
                'message': 'Invalid Data',
                "error": "subscription_plan_id is required",
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan_id)
            UserSubScriptionData = UserSubScription.objects.get(user=request.user, subscription_plan=subscription_plan)
            UserSubScriptionData.is_active = False
            App.objects.filter(user=request.user, subscription=UserSubScriptionData).update(is_active=False)
            UserSubScriptionData.save()
            return CustomJsonResponse({
                'message': f'{self.model_name} unsubscribed',
                'data': self.serializer_class(UserSubScriptionData).data,
            }, status=status.HTTP_200_OK)
        except SubscriptionPlan.DoesNotExist:
            return CustomJsonResponse({
                'message': 'Invalid Data',
                "error": "subscription_plan_id is not valid",
            }, status=status.HTTP_400_BAD_REQUEST)
        except UserSubScription.DoesNotExist:
            return CustomJsonResponse({
                'message': 'Invalid Data',
                "error": "User is not subscribed to this plan",
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        newRecord = self.serializer_class(data=data)
        if newRecord.is_valid():
            newRecord.save()
            return CustomJsonResponse({
                'message': f'{self.model_name} Added',
                'data': newRecord.data,
            }, status=status.HTTP_200_OK)
        return CustomJsonResponse({
            'message': 'Invalid Data',
            "error": newRecord.errors,
        }, status=status.HTTP_400_BAD_REQUEST)
