from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

from emkopo_api.views import LoanOfferResponseAPIView
from emkopo_auth.mixins import LoginMixin
from emkopo_constants.constants import TAKE_OVER_LOAN
from emkopo_loan.mixins import generate_reference_number, generate_loan_id
from emkopo_loan.models import LoanOfferRequest, UserResponse


class LoanOfferRequestView(LoginMixin, TemplateView):
    template_name = f"emkopo_loan/bootstrap/loan-offer-request.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loans = LoanOfferRequest.objects.filter(status=0)
        context.update(
            Staff=self.get_user,
            loans=loans,
        )
        return context


def add_offer_response(request, url=None):
    if request.method == 'POST':

        reference_number = generate_reference_number()
        loan_number = generate_loan_id()

        instance, created = UserResponse.objects.update_or_create(
            Staff_id=request.user.id,
            LoanOfferRequest_id=request.POST.get('LoanOfferRequest'),
            FspComplies=request.POST.get('FspComplies'),
            FspResponse=request.POST.get('FspResponse'),
            FSPReferenceNumber=reference_number,
            LoanNumber=loan_number,
            TotalAmountToPay=request.POST.get('TotalAmountToPay'),
            OtherCharges=request.POST.get('OtherCharges'),
            Reason=request.POST.get('Reason'),
        )

        if created:
            loan_offer_type = 'LOAN_TAKEOVER_APPROVAL_NOTIFICATION_FSP2' if (
                    request.POST.get('LoanOfferType') == TAKE_OVER_LOAN) else None
            LoanOfferResponseAPIView().offer_request_response(instance, loan_offer_type)
            res = 'success'
            message = 'Request submitted successful'
        else:
            res = 'error'
            message = ('Error occurred while processing the request,please check your inputs '
                       'and try gain')

        notification = res + '&message=' + message
        url = "?response=".join(
            [reverse(f'emkopo_loan:{request.POST.get("next_url_name")}'), notification])
    return redirect(url)
