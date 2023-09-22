from django.contrib import admin
from .models import App, SubscriptionPlan, UserSubScription

# Register your models here.


admin.site.register(App)
admin.site.register(SubscriptionPlan)
admin.site.register(UserSubScription)
