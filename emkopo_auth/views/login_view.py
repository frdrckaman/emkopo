from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView


class LoginView(BaseLoginView):
    template_name = f"emkopo_auth/bootstrap/login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['username'] = self.request.user.username
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session.set_test_cookie()
        if not self.request.session.test_cookie_worked():
            messages.add_message(self.request, messages.ERROR, "Please enable cookies.")
        self.request.session.delete_test_cookie()
        errors = str(context)
        error = errors.split(',')[0].split(' ')[2].split('=')[1]
        context.update(
            error=error,
        )
        return context
