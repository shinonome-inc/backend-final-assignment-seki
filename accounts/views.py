from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from tweets.models import Tweet
from .forms import SignUpForm


# Create your views here.


class SignUpView(CreateView):
    template_name = "accounts/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        result = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return result


class UserProfileView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "accounts/profile.html"
    context_object_name = "my_tweets"

    def get_queryset(self):
        return Tweet.objects.filter(user=self.request.user)
