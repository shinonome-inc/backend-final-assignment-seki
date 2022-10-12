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


class Like(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tweet", "user"],
                name="like_unique",
            )
        ]

    def __str__(self):
        return f"{self.user} likes {self.tweet}"
