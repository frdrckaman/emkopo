from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

from emkopo_api.views.disbursement_notification import loan_disbursement_notification
from emkopo_auth.mixins import LoginMixin
from emkopo_loan.models import LoanOfferRequest, UserResponse
from emkopo_mixins.date_mixins import convert_datetime_format
from emkopo_mixins.list_mixins import ListboardView
from emkopo_product.models import Fsp


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


def add_disbursement_response(request, url=None):
    if request.method == 'POST':
        try:
            UserResponse.objects.filter(id=request.POST.get('id')).update(
                FspResponse=request.POST.get('FspResponse'),
                DisbursementDate=convert_datetime_format(request.POST.get('DisbursementDate')),
                TotalAmountToPay=request.POST.get('TotalAmountToPay'),
                Reason=request.POST.get('Reason'),
            )
            loan_offer_request = LoanOfferRequest.objects.get(pk=request.POST.get(
                'LoanOfferRequest'))
            loan_offer_request.LoanNumber = request.POST.get('LoanNumber')
            loan_offer_request.FSPReferenceNumber = request.POST.get('FSPReferenceNumber')
            loan_offer_request.TotalAmountToPay = request.POST.get('TotalAmountToPay')
            loan_offer_request.DisbursementDate = convert_datetime_format(request.POST.get(
                'DisbursementDate'))
            loan_offer_request.status = request.POST.get('FspResponse')
            if request.POST.get('FspResponse') == '4':
                loan_offer_request.Reason = request.POST.get('Reason')
            else:
                loan_offer_request.FailureReason = request.POST.get('Reason')
            loan_offer_request.save()

            fsp = Fsp.objects.all().first()
            offer_request = LoanOfferRequest.objects.get(pk=request.POST.get('LoanOfferRequest'))
            loan_disbursement_notification(offer_request, fsp)

            res = 'success'
            message = 'Request submitted successful'
        except Exception as e:
            res = 'error'
            message = ('Error occurred while processing the request,please check your inputs '
                       'and try gain')

        notification = res + '&message=' + message
        url = "?response=".join(
            [reverse(f'emkopo_loan:{request.POST.get("next_url_name")}'), notification])
    return redirect(url)
