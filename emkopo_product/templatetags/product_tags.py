from django import template

from emkopo_product.models import Fsp, Currency, TermsCondition, ProductCatalog

register = template.Library()


@register.filter(name='format_received_time')
def format_received_time(value):
    formated_dt = value.strftime('%d %b, %Y') if value else None
    return formated_dt


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
def update_fsp(context, fsp_id, num):
    title = None
    fsp = Fsp.objects.get(id=fsp_id)
    return dict(
        num=num,
        fsp=fsp,
        title=title,
    )


@register.inclusion_tag(
    f"emkopo_product/bootstrap/button/del-fsp.html",
    takes_context=True,
)
def delete_fsp(context, fsp_id, num):
    title = None
    fsp = Fsp.objects.get(id=fsp_id)
    return dict(
        num=num,
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
    f"emkopo_product/bootstrap/button/edit-product.html",
    takes_context=True,
)
def update_product(context, product_id, num):
    title = None
    product = ProductCatalog.objects.get(id=product_id)
    return dict(
        num=num,
        title=title,
        product=product,
    )


@register.inclusion_tag(
    f"emkopo_product/bootstrap/button/del-product.html",
    takes_context=True,
)
def delete_product(context, product_id, num):
    title = None
    product = ProductCatalog.objects.get(id=product_id)
    return dict(
        num=num,
        title=title,
        product=product,
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


@register.inclusion_tag(
    f"emkopo_product/bootstrap/button/add-terms.html",
    takes_context=True,
)
def add_terms(context, product_id):
    title = None
    return dict(
        title=title,
        ProductCatalog=product_id
    )


@register.inclusion_tag(
    f"emkopo_product/bootstrap/button/edit-terms.html",
    takes_context=True,
)
def update_terms(context, terms_id, num):
    title = None
    terms = TermsCondition.objects.get(id=terms_id)
    return dict(
        num=num,
        terms=terms,
        title=title,
    )


@register.inclusion_tag(
    f"emkopo_product/bootstrap/button/del-terms.html",
    takes_context=True,
)
def delete_terms(context, terms_id, num):
    title = None
    terms = TermsCondition.objects.filter(id=terms_id)
    return dict(
        num=num,
        terms=terms,
        title=title,
    )
