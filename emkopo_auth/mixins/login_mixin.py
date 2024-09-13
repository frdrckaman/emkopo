from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from emkopo_auth.models import UserProfile


class LoginMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(

        )
        return context

    @method_decorator(login_required(login_url='emkopo_auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @property
    def get_user(self):
        user_id = User.objects.filter(username=self.request.session['username'], is_active=True).first().id
        return user_id

    @property
    def get_user_details(self):
        user = User.objects.filter(username=self.request.session['username'], is_active=True).first()
        return user

    @property
    def user_profiles(self):
        user_profile = UserProfile.objects.get(user_id=self.get_user)
        return user_profile

    @property
    def user_roles(self):
        roles = []
        user_profile = self.user_profiles
        rl = user_profile.roles.all()
        for r in rl:
            roles.append(r.name)
        return roles
