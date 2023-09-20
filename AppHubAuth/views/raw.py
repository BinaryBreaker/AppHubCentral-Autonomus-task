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
    file = data.get('file')
    File = FileModel.objects.create(file=file, uploaded_by=request.user)
    serializer = FileModelSerializer(File)
    return CustomJsonResponse(serializer.data, status=status.HTTP_200_OK)
