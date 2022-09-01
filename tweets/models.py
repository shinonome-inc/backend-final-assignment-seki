from django.db import models
from django.urls import reverse

from accounts.models import User


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="内容", max_length=140)
    created_at = models.DateTimeField(verbose_name="作成日", auto_now_add=True)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("tweets:detail", kwargs={"pk": self.pk})
