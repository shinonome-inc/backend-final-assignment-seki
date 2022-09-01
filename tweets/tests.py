from django.test import TestCase
from django.urls import reverse

from .models import Tweet
from accounts.models import User


class TestHomeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
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

    def test_success_get(self):
        response = self.client.get(reverse("tweets:home"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/home.html")
        self.assertQuerysetEqual(
            response.context["tweets"], Tweet.objects.order_by("-created_at")
        )


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")
        self.url = reverse("tweets:create")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_create.html")

    def test_success_post(self):
        data = {"content": "test_tweet"}
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(Tweet.objects.filter(content=data["content"]).exists())

    def test_failure_post_with_empty_content(self):
        empty_content_data = {"content": ""}
        response = self.client.post(self.url, empty_content_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "content",
            "このフィールドは必須です。",
        )
        self.assertFalse(Tweet.objects.exists())

    def test_failure_post_with_too_long_content(self):
        too_long_content_data = {"content": "a" * 141}
        response = self.client.post(self.url, too_long_content_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "content",
            "この値は 140 文字以下でなければなりません( "
            + str(len(too_long_content_data["content"]))
            + " 文字になっています)。",
        )
        self.assertFalse(Tweet.objects.exists())


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")
        self.tweet = Tweet.objects.create(user=self.user, content="test_tweet")

    def test_success_get(self):
        response = self.client.get(
            reverse("tweets:detail", kwargs={"pk": self.tweet.pk})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_detail.html")
        self.assertEquals(self.tweet, response.context["tweet"])


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="first_user",
            email="firstemail@email.com",
            password="first_password",
        )
        self.user2 = User.objects.create_user(
            username="second_user",
            email="secondemail@email.com",
            password="second_password",
        )
        self.client.login(username="first_user", password="first_password")
        self.tweet1 = Tweet.objects.create(user=self.user1, content="test_tweet")
        self.tweet2 = Tweet.objects.create(user=self.user2, content="test_tweet2")

    def test_success_post(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet1.pk})
        )
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(Tweet.objects.filter(content="test_tweet").exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": 10}))
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Tweet.objects.count(), 2)

    def test_failure_post_with_incorrect_user(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet2.pk})
        )
        self.assertEquals(response.status_code, 403)
        self.assertEquals(Tweet.objects.count(), 2)


class TestFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
