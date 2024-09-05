from django.views.generic.base import TemplateView

from emkopo_auth.mixins import LoginMixin


class WelcomeView(LoginMixin, TemplateView):
    template_name = f"emkopo_dashboard/bootstrap/welcome.html"

    def get_context_data(self, **kwargs):
        menu_category = ''
        context = super().get_context_data(**kwargs)
        context.update()
        return context
