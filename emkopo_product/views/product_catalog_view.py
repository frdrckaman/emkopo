from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

from emkopo_auth.mixins import LoginMixin
from emkopo_product.models import ProductCatalog, Currency


class ProductCatalogView(LoginMixin, TemplateView):
    template_name = f"emkopo_product/bootstrap/product-catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = ProductCatalog.objects.filter(status=1)
        context.update(
            products=products
        )
        return context


def add_product(request):
    if request.method == 'POST':
        created = ProductCatalog.objects.get_or_create(
            ProductCode=request.POST['ProductCode'],
            ProductName=request.POST['ProductName'],
            ProductDescription=request.POST['ProductDescription'],
            ForExecutive=request.POST['ForExecutive'],
            MinimumTenure=request.POST['MinimumTenure'],
            MaximumTenure=request.POST['MaximumTenure'],
            InterestRate=request.POST['InterestRate'],
            ProcessFee=request.POST['ProcessFee'],
            Insurance=request.POST['Insurance'],
            MaxAmount=request.POST['MaxAmount'],
            MinAmount=request.POST['MinAmount'],
            RepaymentType=request.POST['RepaymentType'],
            Currency=request.POST['Currency']
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
            [reverse(f'emkopo_product:{request.POST.get("next_url_name")}'), notification])
    return redirect(url)


def add_currency(request):
    if request.method == 'POST':
        created = Currency.objects.get_or_create(
            name=request.POST['name'],
            code=request.POST['code'],
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
            [reverse(f'emkopo_product:{request.POST.get("next_url_name")}'), notification])
    return redirect(url)
