from django.urls import path

from emkopo_loan.views import LoanOfferRequestView

app_name = "emkopo_loan"

urlpatterns = [
    path("offer-request/", LoanOfferRequestView.as_view(), name="offer-request"),
]