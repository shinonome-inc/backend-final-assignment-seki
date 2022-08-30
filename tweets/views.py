from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import TweetForm
from .models import Tweet

# Create your views here.


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "tweets/home.html"
    context_object_name = "tweets"
    ordering = ["-created_at"]

    def get_queryset(self):
        return Tweet.objects.select_related("user")


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/tweet_create.html"
    form_class = TweetForm
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
