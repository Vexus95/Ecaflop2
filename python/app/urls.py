import hr.urls
from django.urls import include, path

urlpatterns = [
    path("", include(hr.urls)),
]
