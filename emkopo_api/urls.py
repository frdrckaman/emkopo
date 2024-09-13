from django.conf import settings
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from emkopo_api.views import ProductCatalogXMLView, LoanChargesRequestAPIView, \
    LoanOfferRequestAPIView
from emkopo_api.views.product_decommission import GenerateXMLForDecommissionView

schema_view = get_schema_view(
    openapi.Info(
        title="e-MKOPO API",
        default_version='v1',
        description="API documentation for handling product details and terms & conditions",
        terms_of_service=settings.EMKOPO_TERMS_SERVICE_URL,
        contact=openapi.Contact(email="fredrick.amani@stanbic.co.tz"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)
urlpatterns = [
    path('product-catalog/', ProductCatalogXMLView.as_view(), name='product-catalog'),
    path('product-decommission/', GenerateXMLForDecommissionView.as_view(), name='product-decommission'),
    path('loan-charges-request/', LoanChargesRequestAPIView.as_view(), name='loan-charges-request'),
    path('loan-offer-request/', LoanOfferRequestAPIView.as_view(), name='loan-offer-request'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]