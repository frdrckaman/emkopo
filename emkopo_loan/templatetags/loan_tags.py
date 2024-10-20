from django import template

from emkopo_loan.models import LoanOfferRequest, UserResponse
from emkopo_mixins.list_mixins import ListboardView

register = template.Library()


@register.inclusion_tag(
    f"emkopo_loan/bootstrap/button/offer-details.html",
    takes_context=True,
)
def loan_offer_details(context, loan_id, num):
    title = None
    loans = LoanOfferRequest.objects.filter(id=loan_id)
    loan = ListboardView().get_wrapped_queryset(loans)
    return dict(
        num=num,
        loan=loan[0],
        title=title,
        got_approval=True,
    )


@register.inclusion_tag(
    f"emkopo_loan/bootstrap/button/offer-response.html",
    takes_context=True,
)
def loan_offer_response(context, loan_id, num):
    title = None
    loan = LoanOfferRequest.objects.get(id=loan_id)
    return dict(
        num=num,
        loan=loan,
        title=title,
    )


@register.inclusion_tag(
    f"emkopo_loan/bootstrap/button/offer-response.html",
    takes_context=True,
)
def loan_offer_response(context, loan_id, num):
    title = None
    loan = LoanOfferRequest.objects.get(id=loan_id)
    if loan.status > 1:
        usr_response = True
        offer_responses = UserResponse.objects.get(
            LoanOfferRequest__ApplicationNumber=loan.ApplicationNumber)
    else:
        usr_response = False
        offer_responses = None
    offer_response = offer_responses if offer_responses else None
    return dict(
        num=num,
        loan=loan,
        title=title,
        usr_response=usr_response,
        offer_response=offer_response,
    )


@register.inclusion_tag(
    f"emkopo_loan/bootstrap/button/loan-disbursement.html",
    takes_context=True,
)
def loan_disbursement_response(context, loan_id, num):
    title = None
    loan = LoanOfferRequest.objects.get(id=loan_id)
    if loan.status > 1:
        usr_response = True
        offer_responses = UserResponse.objects.get(
            LoanOfferRequest__ApplicationNumber=loan.ApplicationNumber)
    else:
        usr_response = False
        offer_responses = None
    offer_response = offer_responses if offer_responses else None
    return dict(
        num=num,
        loan=loan,
        title=title,
        usr_response=usr_response,
        offer_response=offer_response,
    )
