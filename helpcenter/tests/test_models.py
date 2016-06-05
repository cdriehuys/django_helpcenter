from django.test import TestCase
from django.utils import timezone

from helpcenter import models


class TestArticleModel(TestCase):
    """ Test cases for the Article model """

    def test_create(self):
        """ Test creating an article with all its fields.

        If arguments are passed to an article, it should be created with
        those parameters already set.
        """
        title = 'Test Article'
        body = 'This is a test article only for <em>testing</em>.'
        time = timezone.now()

        article = models.Article.objects.create(
            title=title,
            body=body,
            time_published=time)

        self.assertEqual(1, models.Article.objects.count())
        self.assertEqual(title, article.title)
        self.assertEqual(body, article.body)
        self.assertEqual(time, article.time_published)

    def test_defaults(self):
        """ Test the default values when creating an article.

        If an article is created with only the necessary values, certain
        defaults should automatically be filled in.
        """
        title = 'Test Article'
        body = 'Test body.'

        start = timezone.now()
        article = models.Article.objects.create(
            title=title,
            body=body)
        end = timezone.now()

        self.assertTrue(start <= article.time_published <= end)

    def test_string_conversion(self):
        """ Test converting an Article to a string.

        Converting an Article instance to a string should return a
        string with the article's title.
        """
        article = models.Article(title='Test Article', body='body')

        self.assertEqual(article.title, str(article))
