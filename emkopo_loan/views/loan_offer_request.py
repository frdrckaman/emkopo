from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

from emkopo_auth.mixins import LoginMixin
from emkopo_loan.models import LoanOfferRequest


class LoanOfferRequestView(LoginMixin, TemplateView):
    template_name = f"emkopo_loan/bootstrap/loan-offer-request.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loans = LoanOfferRequest.objects.filter(status=1)
        context.update(
            loans=loans,
        )
        return context
