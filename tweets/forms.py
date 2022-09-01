from django import forms
from django.forms import ModelForm

from .models import Tweet


class TweetForm(ModelForm):
    content = forms.CharField(
        label="",
        max_length=140,
        widget=forms.Textarea(attrs={"rows": 4, "cols": 35, "placeholder": "いまどうしてる？"}),
    )

    class Meta:
        model = Tweet
        fields = ("content",)
