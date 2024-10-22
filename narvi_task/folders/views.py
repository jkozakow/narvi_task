from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import ListView

from narvi_task.folders.models import Folder, Name


class FolderListView(SuccessMessageMixin, ListView):
    model = Folder
    fields = ["name"]


folder_list_view = FolderListView.as_view()

class FolderDetailView(DetailView):
    model = Folder
    slug_field = "group"
    slug_url_kwarg = "group"


folder_detail_view = FolderDetailView.as_view()


class NameMoveView(UpdateView):
    model = Name
    fields = ["folder"]


name_move_view = NameMoveView.as_view()
