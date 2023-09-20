from django.contrib.auth.models import Permission
from rest_framework import serializers
from AppHubAuth.models import AppHubUser
from .FileModelSerializers import FileModelSerializer
from ..other.ModelHelpingData import validate_password


class AppHubUserSerializer(serializers.ModelSerializer):
    dp_uri = FileModelSerializer(source="dp",allow_null=True, required=False)
    date_joined = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, write_only=True)
    dp = serializers.PrimaryKeyRelatedField(queryset=FileModelSerializer.Meta.model.objects.all(), required=False,
                                             allow_null=True,write_only=True)
    # validate password
    def validate_password(self, value):
        print(value)
        if not validate_password(value):
            raise serializers.ValidationError(
                "Password must be a minimum of 8 characters and contain a combination of letters and numbers.")
        return value

    def validate_username(self, value):
        if AppHubUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        user = AppHubUser.objects.create_user(**validated_data)
        user.is_staff = False
        user.is_superuser = False
        return user

    class Meta:
        model = AppHubUser
        fields = (
            "id",
            "full_name",
            "username",
            "email",
            "dp",
            "dp_uri",
            "date_joined",
            "password",
        )
