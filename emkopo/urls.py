from django.conf import settings
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = settings.APP_NAME

urlpatterns = [
    path('admin/', admin.site.urls),
    path("dashboard/", include("emkopo_dashboard.urls")),
    path("", include("emkopo_auth.urls"))
]
