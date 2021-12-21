from django.urls import include, path

import hr.urls

urlpatterns = [
    path("", include(hr.urls)),
]
