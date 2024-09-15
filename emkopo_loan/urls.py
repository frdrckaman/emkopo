from django.urls import path

from emkopo_loan.views import LoanOfferRequestView, PendingGotApprovalView
from emkopo_loan.views.loan_offer_request import add_offer_response

app_name = "emkopo_loan"

urlpatterns = [
    path("offer-request/", LoanOfferRequestView.as_view(), name="offer-request"),
    path("pending-got-approval/", PendingGotApprovalView.as_view(), name="pending-got-approval"),
    path('add-offer-response/', add_offer_response, name="add-offer-response"),
]