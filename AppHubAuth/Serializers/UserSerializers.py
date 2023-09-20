from django.contrib.auth.models import Permission
from rest_framework import serializers
from AppHubAuth.models import AppHubUser
from .FileModelSerializers import FileModelSerializer


class PortfolioUserSerializer(serializers.ModelSerializer):
    dp = FileModelSerializer(allow_null=True, required=False)
    date_joined = serializers.DateTimeField(format="%d %b %Y", read_only=True)

    class Meta:
        model = AppHubUser
        fields = (
            "id",
            "full_name",
            "email",
            "dp",
            "date_joined",

        )
