from django import template

from emkopo_loan.models import LoanOfferRequest

register = template.Library()


@register.inclusion_tag(
    f"emkopo_loan/bootstrap/button/offer-details.html",
    takes_context=True,
)
def loan_offer_details(context, loan_id, num):
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
    return dict(
        num=num,
        loan=loan,
        title=title,
    )
