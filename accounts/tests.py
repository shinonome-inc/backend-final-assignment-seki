from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import SESSION_KEY

from mysite import settings
from tweets.models import Tweet
from .models import User, FriendShip


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
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
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )

        self.assertTrue(
            User.objects.filter(
                username=user_data["username"],
                email=user_data["email"],
            ).exists()
        )

        self.assertIn(SESSION_KEY, self.client.session)

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
        duplicated_data = {
            "username": "testuser",
            "email": "testmail@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
        )
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
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
        )
        self.url = reverse("accounts:login")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_success_post(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )

        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        not_exist_user_data = {
            "username": "hoge",
            "password": "hogefugapiyo",
        }
        response = self.client.post(self.url, not_exist_user_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            None,
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        empty_password_user_data = {
            "username": "testuser",
            "password": "",
        }
        response = self.client.post(self.url, empty_password_user_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "password",
            "このフィールドは必須です。",
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")

    def test_success_get(self):
        response = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(
            response,
            reverse(settings.LOGOUT_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="testemail2@email.com",
            password="testpassword2",
        )
        self.user3 = User.objects.create_user(
            username="testuser3",
            email="testemail3@email.com",
            password="testpassword3",
        )
        self.client.login(username="testuser", password="testpassword")
        Tweet.objects.create(
            user=self.user,
            content="test_tweet1",
        )
        Tweet.objects.create(
            user=self.user,
            content="test_tweet2",
        )
        FriendShip.objects.create(followee=self.user2, follower=self.user)
        FriendShip.objects.create(followee=self.user3, follower=self.user)
        FriendShip.objects.create(followee=self.user, follower=self.user2)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:user_profile", kwargs={"pk": self.user.pk})
        )
        self.assertTemplateUsed(response, "accounts/profile.html")
        self.assertQuerysetEqual(
            response.context["tweets"],
            Tweet.objects.filter(user=self.user).order_by("-created_at"),
        )
        self.assertEquals(
            response.context["following_count"],
            FriendShip.objects.select_related("followee", "follower")
            .filter(follower=self.user)
            .count(),
        )
        self.assertEquals(
            response.context["follower_count"],
            FriendShip.objects.select_related("followee", "follower")
            .filter(followee=self.user)
            .count(),
        )


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
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="testemail2@email.com",
            password="testpassword2",
        )
        self.client.login(username="testuser", password="testpassword")

    def test_success_post(self):
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": self.user2.username})
        )
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(FriendShip.objects.filter(followee=self.user2).exists())

    def test_failure_post_with_not_exist_user(self):
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "hoge"})
        )
        self.assertEquals(response.status_code, 404)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEquals(message, "指定されたユーザーは存在しません。")
        self.assertFalse(FriendShip.objects.filter(followee__username="hoge").exists())

    def test_failure_post_with_self(self):
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": self.user.username})
        )
        self.assertEquals(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEquals(message, "自分自身はフォローできません。")
        self.assertFalse(FriendShip.objects.filter(followee=self.user).exists())


class TestUnfollowView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="testemail2@email.com",
            password="testpassword2",
        )
        self.client.login(username="testuser", password="testpassword")
        FriendShip.objects.create(followee=self.user2, follower=self.user)

    def test_success_post(self):
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": self.user2.username})
        )
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(FriendShip.objects.filter(followee=self.user2).exists())

    def test_failure_post_with_not_exist_user(self):
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "hoge"})
        )
        self.assertEquals(response.status_code, 404)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEquals(message, "指定されたユーザーは存在しません。")
        self.assertTrue(FriendShip.objects.filter(followee=self.user2).exists())

    def test_failure_post_with_incorrect_user(self):
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": self.user.username})
        )
        self.assertEquals(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEquals(message, "自分自身のフォローを外すことはできません。")
        self.assertTrue(FriendShip.objects.filter(followee=self.user2).exists())


class TestFollowingListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="testemail2@email.com",
            password="testpassword2",
        )
        self.user3 = User.objects.create_user(
            username="testuser3",
            email="testemail3@email.com",
            password="testpassword3",
        )
        self.client.login(username="testuser", password="testpassword")
        Tweet.objects.create(
            user=self.user,
            content="test_tweet1",
        )
        Tweet.objects.create(
            user=self.user,
            content="test_tweet2",
        )
        FriendShip.objects.create(followee=self.user2, follower=self.user)
        FriendShip.objects.create(followee=self.user3, follower=self.user)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:following_list", kwargs={"username": self.user.username})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/following_list.html")


class TestFollowerListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="testemail2@email.com",
            password="testpassword2",
        )
        self.user3 = User.objects.create_user(
            username="testuser3",
            email="testemail3@email.com",
            password="testpassword3",
        )
        self.client.login(username="testuser", password="testpassword")
        Tweet.objects.create(
            user=self.user,
            content="test_tweet1",
        )
        Tweet.objects.create(
            user=self.user,
            content="test_tweet2",
        )
        FriendShip.objects.create(followee=self.user2, follower=self.user)
        FriendShip.objects.create(followee=self.user3, follower=self.user)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:follower_list", kwargs={"username": self.user.username})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/follower_list.html")
