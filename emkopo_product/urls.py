from django.urls import path

from emkopo_product.views import FspView, ProductCatalogView
from emkopo_product.views.fsp_view import add_fsp, update_fsp, delete_fsp
from emkopo_product.views.product_catalog_view import add_product, add_currency, \
    update_product, delete_product, add_terms, update_terms, delete_terms

app_name = "emkopo_product"

urlpatterns = [
    path("fsp/", FspView.as_view(), name="fsp"),
    path("product-catalog/", ProductCatalogView.as_view(), name="product-catalog"),
    path("add-fsp/", add_fsp, name="add-fsp"),
    path("add-currency/", add_currency, name="add-currency"),
    path("add-product/", add_product, name="add-product"),
    path("add-terms/", add_terms, name="add-terms"),
    path("update-fsp/", update_fsp, name="update-fsp"),
    path("update-terms/", update_terms, name="update-terms"),
    path("update-product/", update_product, name="update-product"),
    path("delete-fsp/", delete_fsp, name="delete-fsp"),
    path("delete-product/", delete_product, name="delete-product"),
    path("delete-terms/", delete_terms, name="delete-terms"),
    ]
