from django.views.generic.base import TemplateView
from emkopo_auth.mixins import LoginMixin
from emkopo_loan.models import LoanOfferRequest
from emkopo_mixins.list_mixins import ListboardView


class LoanDisbursementRequestView(LoginMixin, ListboardView, TemplateView):
    template_name = f"emkopo_loan/bootstrap/loan-disbursement-request.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loan = LoanOfferRequest.objects.filter(status=3)
        loans = self.get_wrapped_queryset(loan)
        context.update(
            loans=loans,
            got_approval=True,
        )
        return context
