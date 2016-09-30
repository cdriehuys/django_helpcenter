from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Article(models.Model):
    """ Model to represent a help article """
    body = models.TextField(
        help_text="The body of an article can contain HTML as well as text.",
        verbose_name="Article Body Content")

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The parent category for the article.",
        verbose_name="Article Category")

    draft = models.BooleanField(
        default=False,
        help_text="Marking an article as a draft will hide it from users.",
        verbose_name="article is a draft")

    slug = models.SlugField(
        verbose_name='Article URL Slug')

    time_edited = models.DateTimeField(
        auto_now=True,
        verbose_name="time last modifed")

    time_published = models.DateTimeField(
        default=timezone.now,
        help_text=("Please use the following format: ",
                   "<em>YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]</em>"),
        verbose_name="Time Published")

    title = models.CharField(
        max_length=200,
        db_index=True,
        help_text="An article title is restricted to 200 characters.",
        verbose_name="Article Title")

    def __str__(self):
        """ Return the Article's title """
        return self.title

    def get_absolute_url(self):
        """ Get the url of the instance's detail view """
        kwargs = {
            'article_pk': self.pk,
            'article_slug': self.slug,
        }

        return reverse('helpcenter:article-detail', kwargs=kwargs)

    def get_delete_url(self):
        """ Get the url of the instance's delete view """
        kwargs = {
            'article_pk': self.pk,
            'article_slug': self.slug,
        }

        return reverse('helpcenter:article-delete', kwargs=kwargs)

    def get_parent_url(self):
        """ Get the url of the instance's parent """
        if self.category:
            return self.category.get_absolute_url()

        return reverse('helpcenter:index')

    def get_update_url(self):
        """ Get the url of the instance's update view """
        kwargs = {
            'article_pk': self.pk,
            'article_slug': self.slug,
        }

        return reverse('helpcenter:article-update', kwargs=kwargs)

    def save(self, *args, **kwargs):
        """Save the article instance to the database.

        This overrides Django's default save method in order to update
        the instance's `time_published` attribute if the instance is
        being converted from a draft to a normal article.

        It also generates the article's slug if it is being created for
        the first time.

        Args:
            *args: Passed to the default implementation.
            **kwargs: Passed to the default implementation.

        Returns:
            Article: The new saved instance.
        """
        if self.pk and not self.draft:
            old_obj = Article.objects.get(pk=self.pk)

            if old_obj.draft:
                self.time_published = timezone.now()

        if not self.id:
            self.slug = slugify(self.title)[:50]

        return super(Article, self).save(*args, **kwargs)


class Category(models.Model):
    """ Model to represent a category to contain articles """
    title = models.CharField(
        max_length=200,
        db_index=True,
        help_text="A category's title is restricted to 200 characters.",
        verbose_name="Category Title")

    parent = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Categories can be nested as deep as you would like.",
        verbose_name="Parent Category")

    slug = models.SlugField(
        verbose_name="Category URL Slug")

    class Meta:
        """ Meta options for the Category model """
        verbose_name_plural = 'categories'

    def __str__(self):
        """ Return the Category's hierarchy in string form """
        if self.parent:
            return "{} > {}".format(self.parent, self.title)

        return self.title

    @property
    def article_list(self):
        """List of articles in this category.

        If the setting `HELPCENTER_EXPANDED_ARTICLE_LIST` is true, this
        list will include all the articles in this instance's child
        categories as well.
        """
        if getattr(settings, 'HELPCENTER_EXPANDED_ARTICLE_LIST', False):
            articles = self.article_set.all()

            for category in self.category_set.all():
                articles |= category.article_list

            return articles

        return self.article_set.all()

    def get_absolute_url(self):
        """ Get the url of the instance's detail view """
        kwargs = {
            'category_pk': self.pk,
            'category_slug': self.slug
        }

        return reverse('helpcenter:category-detail', kwargs=kwargs)

    def get_delete_url(self):
        """ Get the url of the instance's delete view """
        kwargs = {
            'category_pk': self.pk,
            'category_slug': self.slug
        }

        return reverse('helpcenter:category-delete', kwargs=kwargs)

    def get_parent_url(self):
        """ Get the url of the instance's parent container """
        if self.parent:
            return self.parent.get_absolute_url()

        return reverse('helpcenter:index')

    def get_update_url(self):
        """ Get the url of the instance's update view """
        kwargs = {
            'category_pk': self.pk,
            'category_slug': self.slug
        }

        return reverse('helpcenter:category-update', kwargs=kwargs)

    @property
    def num_articles(self):
        """int: Return the number of articles in the category."""
        articles = self.article_set.exclude(draft=True).count()

        for category in self.category_set.all():
            articles += category.num_articles

        return articles

    def save(self, *args, **kwargs):
        """Save the category to the database.

        If the category is being created, its slug is generated.
        """
        if not self.id:
            self.slug = slugify(self.title)[:50]

        return super(Category, self).save(*args, **kwargs)
