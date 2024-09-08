from django.urls import path

from emkopo_product.views import FspView, ProductCatalogView
from emkopo_product.views.fsp_view import add_fsp, update_fsp, delete_fsp
from emkopo_product.views.product_catalog_view import add_product, add_currency

app_name = "emkopo_product"

urlpatterns = [
    path("fsp/", FspView.as_view(), name="fsp"),
    path("product-catalog/", ProductCatalogView.as_view(), name="product-catalog"),
    path("add-fsp/", add_fsp, name="add-fsp"),
    path("add-currency/", add_currency, name="add-currency"),
    path("add-product/", add_product, name="add-product"),
    path("update-fsp/", update_fsp, name="update-fsp"),
    path("delete-fsp/", delete_fsp, name="delete-fsp"),
    ]