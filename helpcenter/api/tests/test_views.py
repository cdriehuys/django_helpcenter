from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from helpcenter import models
from helpcenter.api import serializers
from helpcenter.testing_utils import create_article


def attach_permission(user, permission_name):
    """ Attach a permission to a user """
    permission = Permission.objects.get(codename=permission_name)
    user.user_permissions.add(permission)


class AuthMixin:
    """ Mixin for handling authentication in test cases """
    password = 'test'
    username = 'test'

    def setUp(self):
        """ Create a test user """
        if get_user_model().objects.filter(username=self.username).exists():
            self.user = get_user_model().objects.get(username=self.username)
        else:
            self.user = get_user_model().objects.create_user(
                username=self.username, password=self.password)

    def login(self, username=None, password=None):
        """ Log in the current client """
        u = username or self.username
        p = password or self.password

        self.client.login(username=u, password=p)


class TestArticleViewSet(AuthMixin, APITestCase):
    """ Test cases for the article view set """

    def test_create(self):
        """ Test creating an article.

        A POST request to the article list view should create a new
        article with the given data.
        """
        attach_permission(self.user, 'add_article')
        self.login()

        data = {
            'title': 'Test Article',
            'body': 'Test body <em>text</em>.',
        }

        url = reverse('api:article-list')
        response = self.client.post(url, data)

        self.assertEqual(201, response.status_code)
        self.assertEqual(1, models.Article.objects.count())

    def test_create_unauthenticated(self):
        """ Test creating an article as an unauthenticated user.

        If a user is unauthenticated, they shouldn't be able to create
        an article.
        """
        data = {
            'title': 'Test Article',
            'body': 'Test body <em>text</em>.',
        }

        url = reverse('api:article-list')
        response = self.client.post(url, data)

        self.assertEqual(403, response.status_code)

    def test_delete(self):
        """ Test deleting an article.

        A DELETE request to an article's detail page should delete that
        article.
        """
        attach_permission(self.user, 'delete_article')
        self.login()

        article = create_article()

        url = reverse('api:article-detail', kwargs={'pk': article.pk})
        response = self.client.delete(url)

        self.assertEqual(204, response.status_code)
        self.assertEqual(0, models.Article.objects.count())

    def test_delete_unauthenticated(self):
        """ Test deleting an article as an unauthenticated user.

        If a user is not authenticated, they should not be able to
        delete an article.
        """
        article = create_article()

        url = reverse('api:article-detail', kwargs={'pk': article.pk})
        response = self.client.delete(url)

        self.assertEqual(403, response.status_code)
        self.assertEqual(1, models.Article.objects.count())

    def test_detail(self):
        """ Test getting the detail view of an article.

        A request to an article's detail view should return the
        serialized version of that article.
        """
        article = create_article()
        serializer = serializers.ArticleSerializer(article)

        url = reverse('api:article-detail', kwargs={'pk': article.pk})
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_list(self):
        """ Test getting a list of articles.

        A GET request to the 'article-list' url should return a
        serialized list of articles.
        """
        article = create_article()
        article2 = create_article(title='Test Article 2')
        serializer = serializers.ArticleSerializer(
            [article, article2], many=True)

        url = reverse('api:article-list')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_patch(self):
        """ Test partially updating an article.

        A PATCH request to an article's detail view should update its
        data with the provided data.
        """
        attach_permission(self.user, 'change_article')
        self.login()

        article = create_article()
        data = {
            'title': 'My Awesome Title'
        }

        url = reverse('api:article-detail', kwargs={'pk': article.pk})
        response = self.client.patch(url, data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(data['title'], models.Article.objects.get().title)

    def test_patch_unauthenticated(self):
        """ Test partially updating an article while not authenticated.

        If an unauthenticated user tries to update an article, they
        should not be able to.
        """
        article = create_article()
        data = {
            'title': 'My Awesome Title'
        }

        url = reverse('api:article-detail', kwargs={'pk': article.pk})
        response = self.client.patch(url, data)

        self.assertEqual(403, response.status_code)

    def test_update(self):
        """ Test updating an article.

        A PUT request to an article's detail view should update the
        article's details.
        """
        attach_permission(self.user, 'change_article')
        self.login()

        article = create_article()
        data = serializers.ArticleSerializer(article).data
        data['category'] = ''
        data['title'] = 'My Awesome Title'

        url = reverse('api:article-detail', kwargs={'pk': article.pk})
        response = self.client.put(url, data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(data['title'], models.Article.objects.get().title)

    def test_update_unauthenticated(self):
        """ Test updating an article while unauthenticated.

        An unauthenticated user should not be able to update an article.
        """
        article = create_article()
        data = serializers.ArticleSerializer(article).data
        data['title'] = 'My Awesome Title'

        url = reverse('api:article-detail', kwargs={'pk': article.pk})
        response = self.client.put(url, data)

        self.assertEqual(403, response.status_code)
