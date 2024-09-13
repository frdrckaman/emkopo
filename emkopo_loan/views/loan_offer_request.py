from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

from emkopo_auth.mixins import LoginMixin
from emkopo_loan.models import LoanOfferRequest, UserResponse


class LoanOfferRequestView(LoginMixin, TemplateView):
    template_name = f"emkopo_loan/bootstrap/loan-offer-request.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loans = LoanOfferRequest.objects.filter(status=1)
        context.update(
            staff=self.get_user,
            loans=loans,
        )
        return context


def add_response(request, url=None):
    if request.method == 'POST':
        created = UserResponse.objects.update_or_create(
            Staff=request.POST.get('staff_id'),
            LoanOfferRequest=request.POST.get('LoanOfferRequest'),
            FspComplies=request.POST.get('FspComplies'),
            FspResponse=request.POST.get('FspResponse'),
        )

        if created:
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
