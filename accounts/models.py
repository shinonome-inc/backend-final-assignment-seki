from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254)
    birth_date = models.DateField(
        verbose_name="誕生日",
        null=True,
        blank=True,
    )
    self_introduction = models.TextField(
        verbose_name="自己紹介",
        max_length=160,
        null=True,
        blank=True,
        default="未設定",
    )


class FriendShip(models.Model):
    followee = models.ForeignKey(
        User,
        related_name="followee",
        on_delete=models.CASCADE,
    )
    follower = models.ForeignKey(
        User,
        related_name="follower",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["followee", "follower"], name="unique_friendship"
            )
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.followee.username}"
