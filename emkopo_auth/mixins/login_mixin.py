from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginMixin:
    @method_decorator(login_required(login_url='emkopo_auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)