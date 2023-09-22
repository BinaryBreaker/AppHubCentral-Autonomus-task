from django.urls import path
from AppHubAuth.urls import urlpatterns as AppHubAuthUrls
from AppHub.views import *

urlpatterns = [
                  path('subscription-plans/', MetaSubscriptionView.as_view(), name="subscription-plans"),

                  path('user-subscription/', UserSubscriptionView.as_view(), name="user-subscription"),
                  path('app-view/', AppView.as_view(), name="app-view"),
                  path('app-view-list', AppViewList.as_view(), name="app-view-list"),
                  path("app-view/<str:id>", AppView.as_view(), name="app-view-get"),

              ] + AppHubAuthUrls
