from django.views import generic
from cafe.models import Position
from django.urls import reverse_lazy

from cafe.views.views import UniversalListView


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("cafe:position-list")


class PositionListView(UniversalListView):
    queryset = Position.objects.all()
    key_to_search = "name"


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("cafe:position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("cafe:position-list")
