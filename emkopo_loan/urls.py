from django.urls import path

from emkopo_loan.views import LoanOfferRequestView, PendingGotApprovalView, \
    LoanDisbursementRequestView
from emkopo_loan.views.loan_disbursement_request import add_disbursement_response
from emkopo_loan.views.loan_offer_request import add_offer_response

app_name = "emkopo_loan"

urlpatterns = [
    path("offer-request/", LoanOfferRequestView.as_view(), name="offer-request"),
    path("pending-got-approval/", PendingGotApprovalView.as_view(), name="pending-got-approval"),
    path("loan-disbursement-request/", LoanDisbursementRequestView.as_view(), name="loan-disbursement-request"),
    path('add-offer-response/', add_offer_response, name="add-offer-response"),
    path("add-disbursement_response/", add_disbursement_response, name="add-disbursement_response"),
]