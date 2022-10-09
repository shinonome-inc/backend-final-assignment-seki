from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, View

from .forms import TweetForm
from .models import Like, Tweet

# Create your views here.


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "tweets/home.html"
    context_object_name = "tweets"

    def get_queryset(self):
        return Tweet.objects.select_related("user").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liked_list"] = Like.objects.filter(user=self.request.user).values_list(
            "tweet", flat=True
        )
        return context


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/tweet_create.html"
    form_class = TweetForm
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    template_name = "tweets/tweet_detail.html"


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = "tweets/tweet_delete.html"
    success_url = reverse_lazy("tweets:home")

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.user


class LikeView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        pk = self.kwargs["pk"]
        tweet = get_object_or_404(Tweet, pk=pk)
        user = self.request.user
        Like.objects.get_or_create(tweet=tweet, user=user)
        context = {
            "tweet_pk": tweet.pk,
            "like_counter": tweet.like_set.count(),
        }
        return JsonResponse(context)


class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        pk = self.kwargs["pk"]
        tweet = get_object_or_404(Tweet, pk=pk)
        user = self.request.user
        like = Like.objects.filter(tweet=tweet, user=user)
        like.delete()
        context = {
            "tweet_pk": tweet.pk,
            "like_counter": tweet.like_set.count(),
        }
        return JsonResponse(context)
