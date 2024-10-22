from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from narvi_task.users.api.views import UserViewSet
from narvi_task.folders.api.views import FolderViewSet, NameViewSet, ResetFoldersViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("folders", FolderViewSet)
router.register("", ResetFoldersViewSet, basename="reset_folders")
router.register("names", NameViewSet)

app_name = "api"
urlpatterns = router.urls
