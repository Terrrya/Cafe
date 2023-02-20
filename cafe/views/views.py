from cafe.forms import SearchForm
from django.views import generic
from django.db.models import QuerySet


class UniversalListView(generic.ListView):
    key_to_search = ""

    def get_context_data(self, **kwargs) -> dict:
        context = super(UniversalListView, self).get_context_data(**kwargs)
        context["search_form"] = SearchForm(
            initial={"field": self.request.GET.get("field", "")}
        )
        return context

    def get_queryset(self) -> QuerySet:
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                **{f"{self.key_to_search}__icontains": form.cleaned_data[
                    "field"
                ]}
            )
        return self.queryset
