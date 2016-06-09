from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from helpcenter import models
from helpcenter.api import serializers
from helpcenter.testing_utils import create_article


class TestArticleViewSet(APITestCase):
    """ Test cases for the article view set """

    def test_delete(self):
        """ Test deleting an article.

        A DELETE request to an article's detail page should delete that
        article.
        """
        article = create_article()

        url = reverse('api:article-detail', kwargs={'pk': article.pk})
        response = self.client.delete(url)

        self.assertEqual(204, response.status_code)
        self.assertEqual(0, models.Article.objects.count())

    def test_create(self):
        """ Test creating an article.

        A POST request to the article list view should create a new
        article with the given data.
        """
        data = {
            'title': 'Test Article',
            'body': 'Test body <em>text</em>.',
        }

        url = reverse('api:article-list')
        response = self.client.post(url, data)

        self.assertEqual(201, response.status_code)
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
        article = create_article()
        data = {
            'title': 'My Awesome Title'
        }

        url = reverse('api:article-detail', kwargs={'pk': article.pk})
        response = self.client.patch(url, data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(data['title'], models.Article.objects.get().title)

    def test_update(self):
        """ Test updating an article.

        An UPDATE request to an article's detail view should update the
        article's details.
        """
        article = create_article()
        data = serializers.ArticleSerializer(article).data
        data['title'] = 'My Awesome Title'

        url = reverse('api:article-detail', kwargs={'pk': article.pk})
        response = self.client.put(url, data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(data['title'], models.Article.objects.get().title)
