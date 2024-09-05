from django.contrib import admin
from django.urls import path

from emkopo_dashboard.views.theme_view import change_theme
from emkopo_dashboard.views.welcome_views import WelcomeView

app_name = "emkopo_dashboard"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("change-theme", change_theme, name="change-theme"),
    path("", WelcomeView.as_view(), name="welcome"),
    ]