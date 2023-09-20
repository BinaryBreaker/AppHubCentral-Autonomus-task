from .BaseView import MetaBaseListView, BaseView,BaseListView
from AppHub.Serializers.AppSerializers import AppSerializer, App


class AppView(BaseView):
    serializer_class = AppSerializer
    Model = App
    model_name = "App"




class AppViewList(BaseListView):
    serializer_class = AppSerializer
    Model = App
    model_name = "App"




