from django.urls import path

from emkopo_product.views import FspView
from emkopo_product.views.fsp_view import add_fsp, update_fsp, delete_fsp

app_name = "emkopo_product"

urlpatterns = [
    path("fsp/", FspView.as_view(), name="fsp"),
    path("add-fsp/", add_fsp, name="add-fsp"),
    path("update-fsp/", update_fsp, name="update-fsp"),
    path("delete-fsp/", delete_fsp, name="delete-fsp"),
    ]