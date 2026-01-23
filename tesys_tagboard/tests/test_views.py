from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from tesys_tagboard.users.models import User


@pytest.mark.django_db
class TestHomeView:
    def test_home(self, client):
        response = client.get(reverse("home"))
        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, "pages/home.html")

    def test_max_query_count(self, client):
        client.get(reverse("home"))


@pytest.mark.django_db
class TestTagsView:
    def test_tags(self, client):
        response = client.get(reverse("tags"))
        assert response.status_code == HTTPStatus.OK

    def test_max_query_count(self, client, django_assert_max_num_queries):
        with django_assert_max_num_queries(15):
            client.get(reverse("home"))


@pytest.mark.django_db
class TestPostsView:
    def test_posts(self, client):
        response = client.get(reverse("posts"))
        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, "pages/posts.html")

    def test_max_query_count(self, client, django_assert_max_num_queries):
        with django_assert_max_num_queries(20):
            client.get(reverse("posts"))

    def test_max_logged_in_query_count(self, client, django_assert_max_num_queries):
        user = User.objects.get(username="user1")
        client.force_login(user)
        with django_assert_max_num_queries(25):
            client.get(reverse("posts"))


@pytest.mark.django_db
class TestUploadView:
    def test_upload(self, client):
        response = client.get(reverse("upload"), follow=True)
        assert response.redirect_chain[0][0] == "/accounts/login/?next=/upload/"
        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, "account/login.html")

    def test_max_query_count(self, client, django_assert_max_num_queries):
        with django_assert_max_num_queries(20):
            client.get(reverse("upload"))


@pytest.mark.django_db
class TestCollectionsView:
    def test_collections(self, client):
        response = client.get(reverse("collections"))
        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, "pages/collections.html")

    def test_max_query_count(self, client, django_assert_max_num_queries):
        with django_assert_max_num_queries(20):
            client.get(reverse("collections"))


@pytest.mark.django_db
class TestHelpView:
    def test_help(self, client):
        response = client.get(reverse("help"))
        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, "pages/help.html")

    def test_max_query_count(self, client, django_assert_max_num_queries):
        with django_assert_max_num_queries(20):
            client.get(reverse("help"))
