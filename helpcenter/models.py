from django.db import models
from django.utils import timezone


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

    time_published = models.DateTimeField(
        default=timezone.now,
        help_text=("Please use the following format: ",
                   "<em>YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]</em>"),
        verbose_name="Time Published")

    title = models.CharField(
        max_length=200,
        db_index=True,
        help_text="An article title is restricted to 200 characters.",
        verbose_name="Article")

    def __str__(self):
        """ Return the Article's title """
        return self.title


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

    def __str__(self):
        """ Return the Category's title """
        return self.title
