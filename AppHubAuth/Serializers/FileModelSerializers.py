from rest_framework import serializers
from AppHubAuth.models import FileModel


class FileModelSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)


    class Meta:
        model = FileModel
        fields = '__all__'
