from django import template

from emkopo_product.models import Fsp, Currency, TermsCondition

register = template.Library()


@register.inclusion_tag(
    f"emkopo_product/bootstrap/button/add-fsp.html",
    takes_context=True,
)
def add_fsp(context):
    title = None
    return dict(
        title=title,
    )


@register.inclusion_tag(
    f"emkopo_product/bootstrap/button/edit-fsp.html",
    takes_context=True,
)
def update_fsp(context, fsp_id):
    title = None
    fsp = Fsp.objects.get(id=fsp_id)
    return dict(
        fsp=fsp,
        title=title,
    )


@register.inclusion_tag(
    f"emkopo_product/bootstrap/button/del-fsp.html",
    takes_context=True,
)
def delete_fsp(context, fsp_id):
    title = None
    fsp = Fsp.objects.get(id=fsp_id)
    return dict(
        fsp=fsp,
        title=title,
    )


@register.inclusion_tag(
    f"emkopo_product/bootstrap/button/add-product.html",
    takes_context=True,
)
def add_product(context):
    title = None
    currencies = Currency.objects.filter(status=True)
    return dict(
        currencies=currencies,
    )


@register.inclusion_tag(
    f"emkopo_product/bootstrap/button/add-currency.html",
    takes_context=True,
)
def add_currency(context):
    title = None
    return dict(
        title=title,
    )


@register.inclusion_tag(
    f"emkopo_product/bootstrap/button/terms-conditions.html",
    takes_context=True,
)
def terms_conditions(context, product_id):
    title = None
    terms = TermsCondition.objects.filter(ProductCatalog_id=product_id)
    return dict(
        title=title,
        terms=terms,
    )
