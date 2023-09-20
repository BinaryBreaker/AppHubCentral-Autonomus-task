from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from AppHubAuth.EmailHandler.HTMLMessageMixinEmail import HTMLMessageMixin
from AppHubAuth.Serializers.CustomAuthTokenSerializers import CustomAuthTokenSerializer
from AppHubAuth.other.CommonFunctions import genOtp
from AppHubAuth.models import Otp, OTP_EXPIRATION_TIME_IN_MIN
from AppHubAuth.other.ModelHelpingData import validate_password
from AppHubCentral.settings import OTP_LENGTH
from AppHubAuth.Serializers.UserSerializers import PortfolioUserSerializer, AppHubUser
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from AppHubAuth.CustomTokens.GenericTokens import BaseGenericToken
from AppHubAuth.other.CustomJsonResponse import CustomJsonResponse


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'profile': PortfolioUserSerializer(user).data,
        })


@api_view(['POST'])
@authentication_classes([BaseGenericToken])
@permission_classes([IsAuthenticated])
def ChangePassword(request):
    old_password = request.data.get('old_password', None)
    new_password = request.data.get('new_password', None)
    if old_password is None:
        return CustomJsonResponse({"old_password": "Old password is required"}, status=400)
    if new_password is None:
        return CustomJsonResponse({"new_password": "New password is required"}, status=400)
    if not request.user.check_password(old_password):
        return CustomJsonResponse({"old_password": "Incorrect password"}, status=400)
    if len(new_password) < 8:
        return CustomJsonResponse({"new_password": "Password must be at least 8 characters"}, status=400)
    request.user.set_password(new_password)
    request.user.save()
    return CustomJsonResponse({"message": "Password changed successfully"}, status=200)


@api_view(['POST'])
def resetPasswordView(request):
    email = request.data.get('email', None)
    if email is None:
        return CustomJsonResponse({"email": "Email is required"}, status=400)
    try:
        name = AppHubUser.objects.get(email=email).full_name
        subject = "Reset Password"
        template_name = "Email/otpEmailTemplate.html"
        otp = Otp.create(genOtp(OTP_LENGTH), email)
        context = {
            "otp": otp.code,
            "subject": subject,
            "name": name,
            "expirationTime": OTP_EXPIRATION_TIME_IN_MIN
        }
        recipient_list = [email]
        email_mixin = HTMLMessageMixin()
        email_mixin.send_html_email(subject, template_name, context, recipient_list)

        return CustomJsonResponse({"message": "OTP sent successfully"}, status=200)

    except AppHubUser.DoesNotExist:
        return CustomJsonResponse({"email": "account does not exist"}, status=400)


@api_view(['POST'])
def validateOtp(request):
    email = request.data.get('email', None)
    otp = request.data.get('otp', None)
    error = {
        'email': 'email is required' if email is None else None,
        'otp': 'otp is required' if otp is None else None,
    }
    if error['email'] is not None or error['otp'] is not None:
        return CustomJsonResponse(error, status=400)
    try:
        otp = Otp.objects.get(email=email, code=otp)
        if otp.is_expired():
            return CustomJsonResponse({"otp": "Invalid otp"}, status=400)

        return CustomJsonResponse({
            "message": "Otp is valid"
        }, status=200)

    except Otp.DoesNotExist:
        return CustomJsonResponse({"otp": "Invalid OTP"}, status=400)


@api_view(['POST'])
def newPasswordView(request):
    email = request.data.get('email', None)
    otp = request.data.get('otp', None)
    password = request.data.get('password', None)
    errors = {
        'email': 'email is required' if email is None else None,
        'otp': 'otp is required' if otp is None else None,
        'password': 'password is required' if password is None else "Password must be a minimum of 8 characters and contain a combination of letters and numbers." if validate_password(
            password) is False else None
    }
    for key in list(errors.keys()):
        if errors[key] is None:
            del errors[key]
    if len(errors) > 0:
        return CustomJsonResponse(errors, status=400)

    try:
        otp = Otp.objects.get(email=email, code=otp)
        if otp.is_expired():
            return CustomJsonResponse({"otp": "Invalid otp"}, status=400)
        user = AppHubUser.objects.get(email=email)
        user.set_password(password)
        user.save()
        otp.delete()
        return CustomJsonResponse({
            "message": "Password changed successfully"
        }, status=200)

    except Otp.DoesNotExist:
        return CustomJsonResponse({"otp": "Invalid OTP"}, status=400)
    except AppHubUser.DoesNotExist:
        return CustomJsonResponse({"email": "account does not exist"}, status=400)
