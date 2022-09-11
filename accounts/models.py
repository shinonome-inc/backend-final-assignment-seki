from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    def __str__(self):
        return str(self.user)


# class FriendShip(models.Model):
#     pass
