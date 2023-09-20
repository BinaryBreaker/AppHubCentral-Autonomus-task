from .BaseView import MetaBaseListView
from AppHub.Serializers.SubscriptionPlanSerializers import SubscriptionPlanSerializer, SubscriptionPlan


class MetaSubscriptionView(MetaBaseListView):
    serializer_class = SubscriptionPlanSerializer
    Model = SubscriptionPlan

    def get_queryset(self):
        return self.Model.objects.all().order_by('-id')
