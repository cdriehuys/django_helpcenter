from django.test import TestCase

from helpcenter.backends.search import SimpleSearch
from helpcenter.testing_utils import create_article


class TestSimpleSearch(TestCase):
    """ Test cases for SimpleSearch backend """

    def setUp(self):
        """ Create backend for each test """
        self.backend = SimpleSearch()

    def test_non_existent_keywords(self):
        """ Test searching for non-existent keywords.

        If the search term doesn't exist in any articles, the method
        should return an empty queryset.
        """
        results = self.backend.search('does not exist')

        self.assertQuerysetEqual(results, [])

    def test_search(self):
        """ Test searching for a term.

        If there is an article with the search term in its title or body
        it should be returned in the results list.
        """
        in_title = create_article(title='Look at the cat')
        in_body = create_article(body='<p>Cat on the loose!</p>')

        results = list(self.backend.search('cat'))

        self.assertTrue(in_title in results)
        self.assertTrue(in_body in results)

    def test_search_multiple_words(self):
        """ Test searching for multiple words.

        If the query string is multiple words then the search backend
        should search for them individually.
        """
        in_title = create_article(title='Cats found fighting')
        in_body = create_article(
            body='<p>Did you see the cats? They were fighting.</p>')

        results = list(self.backend.search('cat fight'))

        self.assertTrue(in_title in results)
        self.assertTrue(in_body in results)
