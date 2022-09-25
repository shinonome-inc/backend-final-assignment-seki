from django.contrib import messages
from django.views.generic import (
    CreateView,
    DetailView,
    View,
    ListView,
)
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from .models import User, FriendShip
from .forms import SignUpForm
from tweets.models import Tweet


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


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context["tweets"] = (
            Tweet.objects.select_related("user")
            .filter(user=user)
            .order_by("-created_at")
        )
        context["following_count"] = FriendShip.objects.filter(follower=user).count()
        context["follower_count"] = FriendShip.objects.filter(followee=user).count()
        context["connection_exists"] = FriendShip.objects.filter(
            follower=self.request.user, followee=user
        ).exists()
        return context


class FollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        follower = self.request.user
        try:
            followee = User.objects.get(username=self.kwargs["username"])
        except User.DoesNotExist:
            messages.warning(request, "指定されたユーザーは存在しません。")
            raise Http404

        if follower == followee:
            messages.warning(request, "自分自身はフォローできません。")
            return render(request, "tweets/home.html")
        elif FriendShip.objects.filter(follower=follower, followee=followee).exists():
            messages.warning(request, f"あなたは{ followee.username }をすでにフォローしています。")
            return render(request, "tweets/home.html")
        else:
            FriendShip.objects.create(follower=follower, followee=followee)
            messages.success(request, f"{ followee.username }をフォローしました。")
            return HttpResponseRedirect(reverse("tweets:home"))


class UnFollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        follower = self.request.user
        try:
            followee = User.objects.get(username=self.kwargs["username"])
        except User.DoesNotExist:
            messages.warning(request, "指定されたユーザーは存在しません。")
            raise Http404

        if follower == followee:
            messages.warning(request, "自分自身のフォローを外すことはできません。")
            return render(request, "tweets/home.html")
        elif FriendShip.objects.filter(follower=follower, followee=followee).exists():
            FriendShip.objects.filter(follower=follower, followee=followee).delete()
            messages.success(request, f"{ followee.username }のフォローを解除しました。")
            return HttpResponseRedirect(reverse("tweets:home"))
        else:
            messages.warning(request, f"{followee.username}はフォローしていません")
            return render(request, "tweets/home.html")


class FollowingListView(LoginRequiredMixin, ListView):
    template_name = "accounts/following_list.html"
    model = FriendShip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs["username"]
        follower = User.objects.get(username=username)
        context["username"] = username
        context["following_list"] = (
            FriendShip.objects.select_related("follower")
            .filter(follower=follower)
            .order_by("-created_at")
        )
        return context


class FollowerListView(LoginRequiredMixin, ListView):
    template_name = "accounts/follower_list.html"
    model = FriendShip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs["username"]
        followee = User.objects.get(username=username)
        context["username"] = username
        context["follower_list"] = (
            FriendShip.objects.select_related("followee")
            .filter(followee=followee)
            .order_by("-created_at")
        )
        return context
