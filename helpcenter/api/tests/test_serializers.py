import json

from django.test import TestCase

from helpcenter import models
from helpcenter.api import serializers
from helpcenter.testing_utils import create_article


class TestArticleSerializer(TestCase):
    """ Test cases for the Article serializer """

    def test_deserialize(self):
        """ Test deserializing an Article.

        Passing valid data to the serializer should allow the serializer
        to construct a new Article from the data.
        """
        data = {
            'title': 'Test Article',
            'body': '<p>Rich <strong>text</strong></p>',
            'category': None,
        }
        serializer = serializers.ArticleSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        article = serializer.save()

        self.assertEqual(data['title'], article.title)
        self.assertEqual(data['body'], article.body)

    def test_serialize(self):
        """ Test serializing an article """
        article = create_article()
        serializer = serializers.ArticleSerializer(article)

        expected_dict = {
            'body': article.body,
            'category': article.category,
            'id': article.id,
            'time_published': article.time_published.isoformat(),
            'title': article.title,
        }
        expected = json.dumps(expected_dict)

        self.assertJSONEqual(expected, serializer.data)

    def test_update(self):
        """ Test updating an existing Article.

        If data is passed to an already existing Article, it should
        update the existing Article.
        """
        article = create_article()
        data = {
            'title': 'New Awesome Title',
        }
        serializer = serializers.ArticleSerializer(
            article, data=data, partial=True)

        self.assertTrue(serializer.is_valid())

        updated = serializer.save()

        self.assertEqual(1, models.Article.objects.count())
        self.assertEqual(data['title'], updated.title)
