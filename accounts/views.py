from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm

# Create your views here.


class SignUpView(CreateView):
    template_name = "accounts/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return result


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
