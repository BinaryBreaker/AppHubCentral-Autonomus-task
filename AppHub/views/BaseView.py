from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, generics
from AppHubAuth.CustomTokens.GenericTokens import BaseGenericToken
from AppHubAuth.other.CustomJsonResponse import CustomJsonResponse


# creating a put update Get and Delete for the store

class BaseView(APIView):
    authentication_classes = [BaseGenericToken]
    permission_classes = [IsAuthenticated]
    serializer_class = None
    Model = None
    model_name = None
    primarySearchField = "id"
    putPrimaryKey = "id"
    userFiled = "user"
    allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']

    def delete(self, request, *args, **kwargs):
        if "DELETE" not in self.allowed_methods:
            return self.http_method_not_allowed()

        pk = request.data.get(self.primarySearchField, None)
        print(pk)
        if pk is None:
            return CustomJsonResponse({
                "error": f"{self.primarySearchField} is required",
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            record = self.Model.objects.get(**{self.primarySearchField: pk, self.userFiled: request.user.id})
            record.delete()
            return CustomJsonResponse({
                'message': f'{self.model_name} Deleted',
            }, status=status.HTTP_200_OK)
        except self.Model.DoesNotExist:
            return CustomJsonResponse({
                "error": f"{self.model_name} Does Not Exist",
            }, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        if "GET" not in self.allowed_methods:
            return self.http_method_not_allowed()
        pk = kwargs.get(self.primarySearchField, None)
        if pk is None:
            return CustomJsonResponse({
                "error": f"{self.primarySearchField} is required",
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            record = self.Model.objects.get(**{self.primarySearchField: pk, self.userFiled: request.user.id})
            serializer = self.serializer_class(record)
            return CustomJsonResponse({
                'message': f'{self.model_name}',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        except self.Model.DoesNotExist:
            return CustomJsonResponse({
                "error": f"{self.model_name} Does Not Exist",
            }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        if "POST" not in self.allowed_methods:
            return self.http_method_not_allowed()
        data = request.data
        data["user"] = request.user.id
        newRecord = self.serializer_class(data=data)
        if newRecord.is_valid():
            newRecord.save()
            return CustomJsonResponse({
                'message': f'{self.model_name} Added',
                'data': newRecord.data,
            }, status=status.HTTP_200_OK)
        return CustomJsonResponse({
            'message': 'Invalid Data',
            "error": newRecord.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        if "PUT" not in self.allowed_methods:
            return self.http_method_not_allowed()
        data = request.data
        print(data)

        if self.putPrimaryKey not in data:
            return CustomJsonResponse({
                "non_field_errors": [f"{self.model_name} {self.putPrimaryKey} is required"],
            }, status=status.HTTP_400_BAD_REQUEST)

        pk = data[self.putPrimaryKey]

        try:
            record = self.Model.objects.get(**{self.putPrimaryKey: pk, self.userFiled: request.user.id})
            data["user"] = request.user.id
            serializer = self.serializer_class(record, data=data)
            if serializer.is_valid():
                serializer.save()
                return CustomJsonResponse({
                    'message': f'{self.model_name} Updated',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK)
            return CustomJsonResponse({
                'message': 'Invalid Data',
                "error": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        except self.Model.DoesNotExist:
            return CustomJsonResponse({
                "error": f"{self.model_name} Does Not Exist",
            }, status=status.HTTP_404_NOT_FOUND)

    def http_method_not_allowed(self):
        return CustomJsonResponse({
            "error": f"Method Not Allowed",
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BaseListView(generics.ListAPIView):
    authentication_classes = [BaseGenericToken]
    permission_classes = [IsAuthenticated]
    serializer_class = None
    Model = None
    primarySearchField = "name__icontains"
    query_field = "name"
    userField = "user"

    # search by name
    def get_queryset(self):
        user = self.request.user
        name = self.request.query_params.get(self.query_field, None)
        print(name)
        if name is not None:
            return self.Model.objects.filter(**{self.userField: user, self.primarySearchField: name}).order_by('-id')
        return self.Model.objects.filter(**{self.userField: user}).order_by('-id')


class MetaBaseListView(BaseListView):
    serializer_class = None
    paginator = None
