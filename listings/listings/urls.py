from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # versioned API root
    path("api/<str:version>/", include("api.urls")),
]
