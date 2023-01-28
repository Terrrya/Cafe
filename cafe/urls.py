from django.urls import path
from cafe.views import index


app_name = "cafe"

urlpatterns = [
    path("", index, name="index")
]
