from django.test import TestCase
from django.urls import reverse
from .models import User


class TestSignUpView(TestCase):
    url = reverse("accounts:signup")

    def test_success_get(self):
        self.url = reverse("accounts:signup")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/sign_up.html")

    def test_success_post(self):
        user_data = {
            "username": "testuser",
            "email": "testmail@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, user_data)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )

        self.assertTrue(
            User.objects.filter(
                username=user_data["username"],
                email=user_data["email"],
            ).exists()
        )

    def test_failure_post_with_empty_form(self):
        empty_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, empty_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "username",
            "このフィールドは必須です。",
        )
        self.assertFormError(
            response,
            "form",
            "email",
            "このフィールドは必須です。",
        )
        self.assertFormError(
            response,
            "form",
            "password1",
            "このフィールドは必須です。",
        )
        self.assertFormError(
            response,
            "form",
            "password2",
            "このフィールドは必須です。",
        )
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_empty_username(self):
        username_empty_data = {
            "username": "",
            "email": "testmail@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, username_empty_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "username",
            "このフィールドは必須です。",
        )
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_empty_email(self):
        email_empty_data = {
            "username": "testuser",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, email_empty_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "email",
            "このフィールドは必須です。",
        )
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_empty_password(self):
        password_empty_data = {
            "username": "testuser",
            "email": "testmail@email.com",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, password_empty_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "password1",
            "このフィールドは必須です。",
        )
        self.assertFormError(
            response,
            "form",
            "password2",
            "このフィールドは必須です。",
        )
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_duplicated_user(self):
        data = {
            "username": "testuser",
            "email": "testmail@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        duplicated_data = {
            "username": "testuser",
            "email": "testmail@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        self.client.post(self.url, data)
        response = self.client.post(self.url, duplicated_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "username",
            "同じユーザー名が既に登録済みです。",
        )
        self.assertTrue(User.objects.count(), 1)

    def test_failure_post_with_invalid_email(self):
        invalid_email_data = {
            "username": "testuser",
            "email": "test",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_email_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "email",
            "有効なメールアドレスを入力してください。",
        )
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_too_short_password(self):
        short_password_data = {
            "username": "testuser",
            "email": "testmail@email.com",
            "password1": "short",
            "password2": "short",
        }

        response = self.client.post(self.url, short_password_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "password2",
            "このパスワードは短すぎます。最低 8 文字以上必要です。",
        )
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_password_similar_to_username(self):
        password_similar_to_username_data = {
            "username": "testuser",
            "email": "testmail@email.com",
            "password1": "testuserr",
            "password2": "testuserr",
        }

        response = self.client.post(self.url, password_similar_to_username_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "password2",
            "このパスワードは ユーザー名 と似すぎています。",
        )
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_only_numbers_password(self):
        only_numbers_password_data = {
            "username": "testuser",
            "email": "testmail@email.com",
            "password1": "84927274",
            "password2": "84927274",
        }

        response = self.client.post(self.url, only_numbers_password_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "password2",
            "このパスワードは数字しか使われていません。",
        )
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_mismatch_password(self):
        mismatch_password_data = {
            "username": "testuser",
            "email": "testmail@email.com",
            "password1": "firstpassword",
            "password2": "secondpassword",
        }

        response = self.client.post(self.url, mismatch_password_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "password2",
            "確認用パスワードが一致しません。",
        )
        self.assertFalse(User.objects.exists())


class TestLoginView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
