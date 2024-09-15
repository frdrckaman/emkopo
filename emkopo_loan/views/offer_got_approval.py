from django.views.generic.base import TemplateView
from emkopo_auth.mixins import LoginMixin
from emkopo_loan.models import LoanOfferRequest
from emkopo_mixins.list_mixins import ListboardView


class LoanOfferRequestView(LoginMixin, ListboardView, TemplateView):
    template_name = f"emkopo_loan/bootstrap/offer-got-approval.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loan = LoanOfferRequest.objects.filter(status=2)
        loans = self.get_wrapped_queryset(loan)
        context.update(
            loans=loans,
        )
        return context
