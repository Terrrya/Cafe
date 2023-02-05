from django.views import generic
from cafe.models import Position
from django.urls import reverse_lazy


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("cafe:position-list")


class PositionListView(generic.ListView):
    model = Position


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("cafe:position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("cafe:position-list")
