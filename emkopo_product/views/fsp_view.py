from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

from emkopo_auth.mixins import LoginMixin
from emkopo_product.models import Fsp


class FspView(LoginMixin, TemplateView):
    template_name = f"emkopo_product/bootstrap/fsp.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fsps = Fsp.objects.filter(status=1)
        context.update(
            fsps=fsps
        )
        return context


def add_fsp(request):
    if request.method == 'POST':
        created = Fsp.objects.get_or_create(
            name=request.POST['name'],
            code=request.POST['code'],
            sysName=request.POST.get("sysName"),
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


def update_fsp(request):
    if request.method == 'POST':
        try:
            Fsp.objects.filter(pk=request.POST.get("id")).update(
                name=request.POST.get("name"),
                code=request.POST.get("code"),
                sysName=request.POST.get("sysName"))

            res = 'success'
            message = 'Request Approved successful'
        except Exception as e:
            res = 'error'
            message = ('Error occurred while processing the request,please check your inputs '
                       'and try again')

    notification = res + '&message=' + message
    url = "?response=".join(
        [reverse(f'emkopo_product:{request.POST.get("next_url_name")}'), notification])

    return redirect(url)


def delete_fsp(request):
    if request.method == 'POST':
        try:
            Fsp.objects.filter(pk=request.POST.get("id")).update(status=0)

            res = 'success'
            message = 'Request Approved successful'
        except Exception as e:
            res = 'error'
            message = ('Error occurred while processing the request,please check your inputs '
                       'and try again')

    notification = res + '&message=' + message
    url = "?response=".join(
        [reverse(f'emkopo_product:{request.POST.get("next_url_name")}'), notification])

    return redirect(url)
