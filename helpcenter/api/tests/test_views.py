import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory, APITestCase

from helpcenter import models
from helpcenter.api import serializers
from helpcenter.testing_utils import create_article, create_category


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
    factory = APIRequestFactory()

    @staticmethod
    def _get_request(viewname, kwargs=None):
        """ Create a request for the given view """
        return TestArticleViewSet.factory.get(reverse(viewname, kwargs=kwargs))

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

        url = reverse('helpcenter:helpcenter-api:article-list')
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

        url = reverse('helpcenter:helpcenter-api:article-list')
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

        url = reverse('helpcenter:helpcenter-api:article-detail',
                      kwargs={'pk': article.pk})
        response = self.client.delete(url)

        self.assertEqual(204, response.status_code)
        self.assertEqual(0, models.Article.objects.count())

    def test_delete_unauthenticated(self):
        """ Test deleting an article as an unauthenticated user.

        If a user is not authenticated, they should not be able to
        delete an article.
        """
        article = create_article()

        url = reverse('helpcenter:helpcenter-api:article-detail',
                      kwargs={'pk': article.pk})
        response = self.client.delete(url)

        self.assertEqual(403, response.status_code)
        self.assertEqual(1, models.Article.objects.count())

    def test_detail(self):
        """ Test getting the detail view of an article.

        A request to an article's detail view should return the
        serialized version of that article.
        """
        article = create_article()
        serializer = serializers.ArticleSerializer(
            article, context={'request': self._get_request(
                'helpcenter:helpcenter-api:article-detail',
                kwargs={'pk': article.pk})})

        url = reverse('helpcenter:helpcenter-api:article-detail',
                      kwargs={'pk': article.pk})
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
        context = {
            'request': self._get_request(
                'helpcenter:helpcenter-api:article-list')
        }
        serializer = serializers.ArticleSerializer(
            [article, article2], many=True, context=context)

        url = reverse('helpcenter:helpcenter-api:article-list')
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

        url = reverse('helpcenter:helpcenter-api:article-detail',
                      kwargs={'pk': article.pk})
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

        url = reverse('helpcenter:helpcenter-api:article-detail',
                      kwargs={'pk': article.pk})
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
        data = serializers.ArticleSerializer(
            article, context={'request': self._get_request(
                'helpcenter:helpcenter-api:article-detail',
                kwargs={'pk': article.pk})}).data
        data['category_id'] = ''
        data['title'] = 'My Awesome Title'

        url = reverse('helpcenter:helpcenter-api:article-detail',
                      kwargs={'pk': article.pk})
        response = self.client.put(url, data)

        self.assertEqual(200, response.status_code, msg=response.data)
        self.assertEqual(data['title'], models.Article.objects.get().title)

    def test_update_unauthenticated(self):
        """ Test updating an article while unauthenticated.

        An unauthenticated user should not be able to update an article.
        """
        article = create_article()
        data = serializers.ArticleSerializer(
            article, context={'request': self._get_request(
                'helpcenter:helpcenter-api:article-detail',
                kwargs={'pk': article.pk})}).data
        data['title'] = 'My Awesome Title'

        url = reverse('helpcenter:helpcenter-api:article-detail',
                      kwargs={'pk': article.pk})
        response = self.client.put(url, data)

        self.assertEqual(403, response.status_code)


class TestCategoryViewSet(AuthMixin, APITestCase):
    """ Test cases for the category view set """
    factory = APIRequestFactory()

    @staticmethod
    def _get_request(viewname, kwargs=None):
        """ Create a request for the given view """
        return TestCategoryViewSet.factory.get(
            reverse(viewname, kwargs=kwargs))

    def test_create(self):
        """ Test creating a category.

        A POST request to the category list view should create a new
        category with the given data.
        """
        attach_permission(self.user, 'add_category')
        self.login()

        data = {
            'title': 'Test Category',
        }

        url = reverse('helpcenter:helpcenter-api:category-list')
        response = self.client.post(url, data)

        self.assertEqual(201, response.status_code)
        self.assertEqual(1, models.Category.objects.count())

    def test_create_unauthenticated(self):
        """ Test creating a category as an unauthenticated user.

        If a user is unauthenticated, they shouldn't be able to create
        a category.
        """
        data = {
            'title': 'Test Category',
        }

        url = reverse('helpcenter:helpcenter-api:category-list')
        response = self.client.post(url, data)

        self.assertEqual(403, response.status_code)

    def test_delete(self):
        """ Test deleting a category.

        A DELETE request to a category's detail page should delete that
        category.
        """
        attach_permission(self.user, 'delete_category')
        self.login()

        category = create_category()

        url = reverse('helpcenter:helpcenter-api:category-detail',
                      kwargs={'pk': category.pk})
        response = self.client.delete(url)

        self.assertEqual(204, response.status_code)
        self.assertEqual(0, models.Category.objects.count())

    def test_delete_unauthenticated(self):
        """ Test deleting a category as an unauthenticated user.

        If a user is not authenticated, they should not be able to
        delete a category.
        """
        category = create_category()

        url = reverse('helpcenter:helpcenter-api:category-detail',
                      kwargs={'pk': category.pk})
        response = self.client.delete(url)

        self.assertEqual(403, response.status_code)
        self.assertEqual(1, models.Category.objects.count())

    def test_detail(self):
        """ Test getting the detail view of a category.

        A request to a category's detail view should return the
        serialized version of that category.
        """
        category = create_category()
        serializer = serializers.CategorySerializer(
            category, context={'request': self._get_request(
                'helpcenter:helpcenter-api:category-detail',
                kwargs={'pk': category.pk})})

        url = reverse('helpcenter:helpcenter-api:category-detail',
                      kwargs={'pk': category.pk})
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_list(self):
        """ Test getting a list of categories.

        A GET request to the 'category-list' url should return a
        serialized list of categories.
        """
        category = create_category()
        category2 = create_category(title='Test Category 2')
        context = {
            'request': self._get_request(
                'helpcenter:helpcenter-api:category-list')
        }
        serializer = serializers.CategorySerializer(
            [category, category2], many=True, context=context)

        url = reverse('helpcenter:helpcenter-api:category-list')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_patch(self):
        """ Test partially updating a category.

        A PATCH request to a category's detail view should update its
        data with the provided data.
        """
        attach_permission(self.user, 'change_category')
        self.login()

        category = create_category()
        data = {
            'title': 'My Awesome Title'
        }

        url = reverse('helpcenter:helpcenter-api:category-detail',
                      kwargs={'pk': category.pk})
        response = self.client.patch(url, data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(data['title'], models.Category.objects.get().title)

    def test_patch_unauthenticated(self):
        """ Test partially updating a category while not authenticated.

        If an unauthenticated user tries to update a category, they
        should not be able to.
        """
        category = create_category()
        data = {
            'title': 'My Awesome Title'
        }

        url = reverse('helpcenter:helpcenter-api:category-detail',
                      kwargs={'pk': category.pk})
        response = self.client.patch(url, data)

        self.assertEqual(403, response.status_code)

    def test_update(self):
        """ Test updating a category.

        A PUT request to a category's detail view should update the
        category's details.
        """
        attach_permission(self.user, 'change_category')
        self.login()

        category = create_category()
        data = serializers.CategorySerializer(
            category, context={'request': self._get_request(
                'helpcenter:helpcenter-api:category-detail',
                kwargs={'pk': category.pk})}).data
        data['parent_id'] = ''
        data['title'] = 'My Awesome Title'

        url = reverse('helpcenter:helpcenter-api:category-detail',
                      kwargs={'pk': category.pk})
        response = self.client.put(url, data)

        self.assertEqual(200, response.status_code, response.data)
        self.assertEqual(data['title'], models.Category.objects.get().title)

    def test_update_unauthenticated(self):
        """ Test updating a category while unauthenticated.

        An unauthenticated user should not be able to update a category.
        """
        category = create_category()
        data = serializers.CategorySerializer(
            category, context={'request': self._get_request(
                'helpcenter:helpcenter-api:category-detail',
                kwargs={'pk': category.pk})}).data
        data['title'] = 'My Awesome Title'

        url = reverse('helpcenter:helpcenter-api:category-detail',
                      kwargs={'pk': category.pk})
        response = self.client.put(url, data)

        self.assertEqual(403, response.status_code)


class TestPermissionsView(AuthMixin, APITestCase):
    """ Test cases for the permissions view """
    url = reverse('helpcenter:helpcenter-api:permissions')

    def setUp(self, *args, **kwargs):
        """ Create a dict containing the default permissions """
        super(TestPermissionsView, self).setUp(*args, **kwargs)

        self.default_permissions = {
            'add_article': False,
            'add_category': False,
            'change_article': False,
            'change_category': False,
            'delete_article': False,
            'delete_category': False,
        }

    def test_all_permissions(self):
        """ Test the view as a user with all permissions.

        If a user has all permissions, the response should return true
        for each permission.
        """
        self.user.is_superuser = True
        self.user.save()
        self.login()

        response = self.client.get(self.url)

        expected_dict = {k: True for k in self.default_permissions}
        expected = json.dumps(expected_dict)

        self.assertJSONEqual(expected, response.data)

    def test_no_permissions(self):
        """ Test the view as a user with no permissions.

        If the user has no permissions, the response should return false
        for each permission.
        """
        self.login()

        response = self.client.get(self.url)

        expected_dict = self.default_permissions.copy()
        expected = json.dumps(expected_dict)

        self.assertJSONEqual(expected, response.data)

    def test_unauthenticated(self):
        """ Test the view as an unauthenticated user.

        If an unauthenticated user tries to access the view, they should
        receive a 403 response.
        """
        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)
