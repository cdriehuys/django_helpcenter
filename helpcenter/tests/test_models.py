from datetime import timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.utils import timezone
from django.utils.text import slugify

from helpcenter import models
from helpcenter.testing_utils import (
    create_article, create_category, instance_to_queryset_string)


class TestArticleModel(TestCase):
    """ Test cases for the Article model """

    def test_create(self):
        """ Test creating an article with all its fields.

        If arguments are passed to an article, it should be created with
        those parameters already set.
        """
        category = create_category()
        title = 'Test Article'
        body = 'This is a test article only for <em>testing</em>.'
        time = timezone.now()

        article = models.Article.objects.create(
            category=category,
            title=title,
            body=body,
            time_published=time,
            draft=True)

        self.assertEqual(1, models.Article.objects.count())
        self.assertEqual(category, article.category)
        self.assertEqual(title, article.title)
        self.assertEqual(body, article.body)
        self.assertEqual(time, article.time_published)
        self.assertIsNotNone(article.time_edited)
        self.assertTrue(article.draft)

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

        self.assertIsNone(article.category)
        self.assertTrue(start <= article.time_published <= end)
        self.assertTrue(start <= article.time_edited <= end)
        self.assertFalse(article.draft)

    def test_draft_publish(self):
        """Test publishing a draft.

        If an article is changed from a draft to published, it's
        `time_published` attribute should update to the current time.
        """
        prev_time = timezone.now() - timedelta(days=1)
        article = create_article(time_published=prev_time, draft=True)

        article.draft = False

        time_start = timezone.now()
        article.save()
        time_end = timezone.now()

        self.assertTrue(time_start <= article.time_published <= time_end)

    def test_draft_publish_no_update(self):
        """Test saving an article whose `draft` attr is already False.

        An article that is saved with `draft` already set to False
        should not update `time_published`.
        """
        prev_time = timezone.now() - timedelta(days=1)
        article = create_article(time_published=prev_time)

        # Do some unrelated save
        article.title = 'New Title'
        article.save()

        # `time_published` should not have changed
        self.assertEqual(prev_time, article.time_published)

    def test_get_absolute_url(self):
        """ Test getting an Article instance's url.

        This method should return the URL of the instance's detail view.
        """
        article = create_article()

        url = reverse('helpcenter:article-detail', kwargs={
            'article_pk': article.pk,
            'article_slug': article.slug,
        })

        self.assertEqual(url, article.get_absolute_url())

    def test_get_delete_url(self):
        """ Test getting the url of an Article instance's delete page.

        This method should return the url of the instance's delete view.
        """
        article = create_article()

        expected = reverse(
            'helpcenter:article-delete', kwargs={
                'article_pk': article.pk,
                'article_slug': article.slug,
            })

        self.assertEqual(expected, article.get_delete_url())

    def test_get_parent_url(self):
        """ Test getting the url of an Article's parent page.

        If an article has a Category, this method should return the url
        of the detail view for the parent Category.
        """
        category = create_category()
        article = create_article(category=category)

        expected = category.get_absolute_url()

        self.assertEqual(expected, article.get_parent_url())

    def test_get_parent_url_no_parent(self):
        """ Test getting the url of an Article's parent page.

        If an article does not have a Category, this method should
        return the url of the index view.
        """
        article = create_article()

        expected = reverse('helpcenter:index')

        self.assertEqual(expected, article.get_parent_url())

    def test_get_update_url(self):
        """ Test getting an Article instance's update url.

        This method should return the url of the instance's update view.
        """
        article = create_article()

        expected = reverse(
            'helpcenter:article-update', kwargs={
                'article_pk': article.pk,
                'article_slug': article.slug,
            })

        self.assertEqual(expected, article.get_update_url())

    def test_slug_generation(self):
        """Test the creation of the article's slug.

        When an article is first saved, it should generate a slug from
        its title.
        """
        article = create_article(title='Test Title')

        self.assertEqual(slugify('Test Title'), article.slug)

    def test_slug_title_change(self):
        """Test an article's slug when its title is changed.

        Changing the title after the initial save should not change the
        slug.
        """
        article = create_article(title='Test Title')

        article.title = 'New Title'
        article.save()

        self.assertEqual(slugify('Test Title'), article.slug)

    def test_string_conversion(self):
        """ Test converting an Article to a string.

        Converting an Article instance to a string should return a
        string with the article's title.
        """
        article = models.Article(title='Test Article', body='body')

        self.assertEqual(article.title, str(article))


class TestCategoryModel(TestCase):
    """ Test cases for the Category model """

    @override_settings(HELPCENTER_EXPANDED_ARTICLE_LIST=False)
    def test_article_list_default(self):
        """Test the default article list.

        By default, this property should return articles who's category
        is that single category instance.
        """
        top_category = create_category()
        top_article = create_article(category=top_category)

        child_category = create_category(parent=top_category)
        create_article(category=child_category)

        self.assertQuerysetEqual(
            top_category.article_list,
            [instance_to_queryset_string(top_article)])

    @override_settings(HELPCENTER_EXPANDED_ARTICLE_LIST=True)
    def test_article_list_expanded(self):
        """Test the expanded article list.

        If the `HELPCENTER_EXPANDED_ARTICLE_LIST` setting is true, all
        articles in the Category instance's child categories should be
        included in the list.
        """
        top_category = create_category()
        top_article = create_article(category=top_category)

        child_category = create_category(parent=top_category)
        child_article = create_article(category=child_category)

        deep_child_category = create_category(parent=child_category)
        deep_child_article = create_article(category=deep_child_category)

        results = top_category.article_list

        self.assertTrue(top_article in results)
        self.assertTrue(child_article in results)
        self.assertTrue(deep_child_article in results)

    def test_create(self):
        """ Test creating a Category with all its fields.

        Any arguments passed to a Category should affect the created
        instance's attributes.
        """
        title = 'Test Category'
        parent = create_category(title='Parent Category')

        category = models.Category.objects.create(title=title, parent=parent)

        self.assertEqual(title, category.title)
        self.assertEqual(parent, category.parent)

    def test_delete_parent(self):
        """ Test deleting a parent category.

        If a parent category is deleted, its child categories should
        have their parent set to NULL rather than being deleted.
        """
        parent = create_category(title='parent')
        create_category(title='child', parent=parent)

        parent.delete()

        self.assertEqual(1, models.Category.objects.count())
        self.assertEqual('child', models.Category.objects.get().title)

    def test_get_absolute_url(self):
        """ Test getting a Category instance's absolute url.

        This method should return the url of the instance's detail view.
        """
        category = create_category()

        url = reverse(
            'helpcenter:category-detail',
            kwargs={
                'category_pk': category.pk,
                'category_slug': category.slug
            })

        self.assertEqual(url, category.get_absolute_url())

    def test_get_delete_url(self):
        """ Test getting a Category instance's delete url.

        This method should return the url of the instance's delete view.
        """
        category = create_category()

        expected = reverse(
            'helpcenter:category-delete', kwargs={
                'category_pk': category.pk,
                'category_slug': category.slug
            })

        self.assertEqual(expected, category.get_delete_url())

    def test_get_parent_url(self):
        """ Test getting the url of a Category's parent container.

        If the Category has a parent Category, the url of the parent
        Category's detail view should be returned.
        """
        parent = create_category()
        category = create_category(parent=parent)

        expected = parent.get_absolute_url()

        self.assertEqual(expected, category.get_parent_url())

    def test_get_parent_url_no_parent(self):
        """ Test getting the url of a Category's parent container.

        If a Category has no parent Category, this method should return
        the url of the index view.
        """
        category = create_category()

        expected = reverse('helpcenter:index')

        self.assertEqual(expected, category.get_parent_url())

    def test_get_update_url(self):
        """ Test getting the url of a Category instance's update view.

        The method should return the url of the instance's update view.
        """
        category = create_category()

        expected = reverse(
            'helpcenter:category-update', kwargs={
                'category_pk': category.pk,
                'category_slug': category.slug
            })

        self.assertEqual(expected, category.get_update_url())

    def test_num_articles(self):
        """ Test num_articles property with articles in category.

        This property should return the number of articles in a
        Category.
        """
        category = create_category()
        create_article(category=category)

        self.assertEqual(1, category.num_articles)

    def test_num_articles_draft(self):
        """Test `num_articles` property with draft articles.

        Articles marked as drafts should not be included in the count.
        """
        category = create_category()
        create_article(category=category, draft=True)

        self.assertEqual(0, category.num_articles)

    def test_num_articles_nested(self):
        """ Test num_articles property with nested categories.

        The property should loop through all the instance's child
        categories and include the number of articles in each of them.
        """
        category = create_category()
        child = create_category(title='child', parent=category)
        create_article(category=child)

        self.assertEqual(1, category.num_articles)

    def test_slug_generation(self):
        """Test the creation of the category's slug.

        When a category is first saved, it should generate a slug from
        its title.
        """
        category = create_category(title='Test Title')

        self.assertEqual(slugify('Test Title'), category.slug)

    def test_slug_title_change(self):
        """Test a category's slug when its title is changed.

        Changing the title after the initial save should not change the
        slug.
        """
        category = create_category(title='Test Title')

        category.title = 'New Title'
        category.save()

        self.assertEqual(slugify('Test Title'), category.slug)

    def test_string_conversion(self):
        """ Test converting a Category instance to a string.

        Converting a Category instance to a string should return the
        instance's title.
        """
        category = models.Category(title='Test Category')

        self.assertEqual(category.title, str(category))

    def test_string_conversion_nested(self):
        """Test converting a nested Category instance to a string.

        If a category has a parent category, it's string representation
        should show that.
        """
        parent = create_category(title='parent')
        category = create_category(parent=parent, title='child')

        expected = "{} > {}".format(parent.title, category.title)

        self.assertEqual(expected, str(category))
