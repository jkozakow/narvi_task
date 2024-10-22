import csv
import os

from django.conf import settings
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.http import Http404

from narvi_task.folders.models import Folder, Name
from narvi_task.folders.group_names import group_by_prefix
from .serializers import (
    FolderSerializer,
    NameSerializer,
    FolderResetSerializer,
    InputMoveNameSerializer,
)


class ResetFoldersViewSet(GenericViewSet):
    serializer_class = FolderResetSerializer
    queryset = Folder.objects.all()

    @action(detail=False, methods=["GET"])
    def reset_folders(self, request, pk=None):
        self.queryset.delete()
        with open(os.path.join(settings.BASE_DIR, "narvi_task/data/names.csv"), "r") as file:
            data = []
            reader = csv.reader(file)
            for line in reader:
                if line:
                    data.append(*line)
            folders = group_by_prefix(data)

        for folder, names in folders.items():
            folder_serializer = self.get_serializer(data={"prefix": folder})
            folder_serializer.is_valid(raise_exception=True)
            folder_serializer.save()
            for name in names:
                Name(name=name, folder_id=folder_serializer.instance.id).save()
        return Response({"status": "Folders reset done"})


class NameViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = NameSerializer
    queryset = Name.objects.all()
    lookup_field = "name"

    @extend_schema(request=InputMoveNameSerializer)
    @action(detail=True, methods=["PATCH"])
    def move_name_into_folder(self, request, pk=None, **kwargs):
        folder_name = request.data["folder_name"]
        try:
            folder = Folder.objects.get(prefix=folder_name)
        except Folder.DoesNotExist:
            raise Http404(f"Folder with name={folder_name} not found")
        instance = self.get_object()
        instance.folder_id = folder.id
        instance.save()
        return Response(self.get_serializer(instance).data)


class FolderViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()
    lookup_field = "prefix"

