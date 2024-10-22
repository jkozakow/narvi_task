from rest_framework import serializers

from narvi_task.folders.models import Folder, Name


class FolderSerializer(serializers.ModelSerializer[Folder]):
    names = serializers.StringRelatedField(many=True)

    class Meta:
        model = Folder
        fields = ["prefix", "names"]

        extra_kwargs = {
            "url": {"view_name": "api:folder-detail", "lookup_field": "prefix"},
        }


class NameSerializer(serializers.ModelSerializer[Name]):
    folder_name = serializers.CharField(read_only=True, source="folder.prefix")

    class Meta:
        model = Name
        fields = ["name", "folder_name"]

        extra_kwargs = {
            "url": {"view_name": "api:name-detail", "lookup_field": "name"},
        }


class FolderResetSerializer(serializers.ModelSerializer[Folder]):
    class Meta:
        model = Folder
        fields = ["prefix"]


class InputMoveNameSerializer(serializers.Serializer):
    folder_name = serializers.CharField()
