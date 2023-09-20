from django.urls import path
from django.conf.urls.static import static
from AppHubCentral import settings
from .views import *

urlpatterns = [
                  path('api-token-auth/', CustomAuthToken.as_view(), name="api-token-auth"),
                  path('upload-file', uploadFile, name="upload-file"),
                  path('change-password', ChangePassword, name="change-password"),
                  path('reset-password', resetPasswordView, name="reset-password"),
                  path('validate-otp', validateOtp, name="validate-otp"),
                  path('set-new-password', newPasswordView, name="set-new-password"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
