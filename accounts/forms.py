from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        label="Eメール",
        help_text="この項目は必須です。有効なメールアドレスを入力してください",
        required=True,
    )

    class Meta:
        model = User
        fields = ("username", "email",)
