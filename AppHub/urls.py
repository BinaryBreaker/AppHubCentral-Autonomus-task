from django.urls import path
from AppHubAuth.urls import urlpatterns as AppHubAuthUrls
from AppHub.views import *

urlpatterns = [
                  path('subscription-plans/', MetaSubscriptionView.as_view(), name="subscription-plans"),

              ] + AppHubAuthUrls
