from django.conf import settings
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from emkopo_api.views import ProductCatalogXMLView, LoanChargesRequestAPIView, \
    LoanOfferRequestAPIView, LoanOfferResponseAPIView, LoanFinalApprovalNotificationAPIView, \
    LoanDisbursementNotificationAPIView, LoanDisbursementFailureNotificationAPIView, \
    LoanOfferCancellationNotificationAPIView, LoanPayOffBalanceRequestAPIView, \
    LoanSettlementBalanceResponseAPIView, LoanRestructuringRequestAPIView, \
    LoanTakeOverDetailsAPIView, LoanLiquidationRequestAPIView, \
    LoanNotificationToEmployerAPIView, LoanLiquidationNotificationAPIView, \
    LoanTakeoverDisbursementNotificationAPIView, LoanRepaymentRequestAPIView, \
    LoanRepaymentOffBalanceRequestAPIView, LoanPayoffPaymentResponseAPIView, \
    FullLoanRepaymentNotificationAPIView, FullLoanRepaymentRequestAPIView, \
    LoanRepaymentNotificationAPIView, LoanDefaulterDetailEmployerAPIView, \
    LoanDefaulterDetailAPIView
from emkopo_api.views.account_validation_request import AccountValidationRequestAPIView
from emkopo_api.views.partial_loan_repayment_request import PartialLoanRepaymentRequestAPIView
from emkopo_api.views.partial_loan_repayment_response import \
    PartialLoanRepaymentResponseAPIView
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
    path('loan-offer-response/', LoanOfferResponseAPIView.as_view(), name='loan-offer-response'),
    path('offer-final-approval/', LoanFinalApprovalNotificationAPIView.as_view(), name='offer-final-approval'),
    path('loan-disbursement-notification/', LoanDisbursementNotificationAPIView.as_view(),
         name='loan-disbursement-notification'),
    path('fail-disbursement-notification/', LoanDisbursementFailureNotificationAPIView.as_view(),
         name='fail-disbursement-notification'),
    path('loan-cancellation-notification/', LoanOfferCancellationNotificationAPIView.as_view(), name='loan-cancellation-notification'),
    path('loan-payoff-balance-request/', LoanPayOffBalanceRequestAPIView.as_view(), name='loan-payoff-balance-request'),
    path('loan-restructuring-request/', LoanRestructuringRequestAPIView.as_view(), name='loan-restructuring-request'),
    path('loan-settlement-balance-response/', LoanSettlementBalanceResponseAPIView.as_view(), name='loan-settlement-balance-response'),
    path('loan-takeover-details/', LoanTakeOverDetailsAPIView.as_view(), name='loan-takeover-details'),
    path('loan-liquidation-request/', LoanLiquidationRequestAPIView.as_view(),
         name='loan-liquidation-request'),
    path('loan-notification-employer/', LoanNotificationToEmployerAPIView.as_view(),
         name='loan-notification-employer'),
    path('loan-liquidation-notification/', LoanLiquidationNotificationAPIView.as_view(), name='loan-liquidation-notification'),
    path('takeover-disbursement-notification/', LoanTakeoverDisbursementNotificationAPIView.as_view(),
         name='takeover-disbursement-notification'),
    path('loan-repayment-request/', LoanRepaymentRequestAPIView.as_view(),
         name='loan-repayment-request'),
    path('loan-repayment-off-balance-request/', LoanRepaymentOffBalanceRequestAPIView.as_view(), name='loan-repayment-off-balance-request'),
    path('loan-payoff-payment-response/', LoanPayoffPaymentResponseAPIView.as_view(),
         name='loan-payoff-payment-response'),
    path('full-loan-repayment-notification/', FullLoanRepaymentNotificationAPIView.as_view(),
         name='full-loan-repayment-notification'),
    path('full-loan-repayment-request/', FullLoanRepaymentRequestAPIView.as_view(),
         name='full-loan-repayment-request'),
    path('partial-loan-repayment-request/', PartialLoanRepaymentRequestAPIView.as_view(),
         name='partial-loan-repayment-request'),
    path('partial-loan-repayment-response/', PartialLoanRepaymentResponseAPIView.as_view(),
         name='partial-loan-repayment-response'),
    path('loan-repayment-notification/', LoanRepaymentNotificationAPIView.as_view(),
         name='loan-repayment-notification'),
    path('loan-defaulter-detail-employer/', LoanDefaulterDetailEmployerAPIView.as_view(),
         name='loan-defaulter-detail-employer'),
    path('loan-defaulter-detail/', LoanDefaulterDetailAPIView.as_view(),
         name='loan-defaulter-detail'),
    path('account-validation-request/', AccountValidationRequestAPIView.as_view(),
         name='account-validation-request'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]