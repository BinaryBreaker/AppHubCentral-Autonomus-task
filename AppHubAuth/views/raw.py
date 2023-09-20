from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from AppHubAuth.CustomTokens.GenericTokens import BaseGenericToken
from AppHubAuth.Serializers.FileModelSerializers import FileModelSerializer, FileModel
from AppHubAuth.other.CustomJsonResponse import CustomJsonResponse


@api_view(['POST'])
@authentication_classes([BaseGenericToken])
@permission_classes([IsAuthenticated])
def uploadFile(request):
    data = request.data
    data._mutable = True
    data['uploaded_by'] = request.user.id
    serializerFile = FileModelSerializer(data=data)
    if serializerFile.is_valid():
        serializerFile.save()
        return CustomJsonResponse(serializerFile.data, status=status.HTTP_201_CREATED)
    return CustomJsonResponse(serializerFile.errors, status=status.HTTP_400_BAD_REQUEST)
