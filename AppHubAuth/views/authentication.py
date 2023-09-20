from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from AppHubAuth.Serializers.CustomAuthTokenSerializers import CustomAuthTokenSerializer
from AppHubAuth.Serializers.UserSerializers import AppHubUserSerializer, AppHubUser
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
            'profile': AppHubUserSerializer(user).data,
        })


@api_view(['POST'])
def SingUp(request):
    data = request.data
    serializer = AppHubUserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return CustomJsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return CustomJsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
