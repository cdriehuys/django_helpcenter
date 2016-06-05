from django.db import models
from django.utils import timezone


class Article(models.Model):
    """ Model to represent a help article """
    title = models.CharField(
        max_length=200,
        db_index=True,
        help_text="An article title is restricted to 200 characters.",
        verbose_name="Article")

    body = models.TextField(
        help_text="The body of an article can contain HTML as well as text.",
        verbose_name="Article Body Content")

    time_published = models.DateTimeField(
        default=timezone.now,
        help_text=("Please use the following format: ",
                   "<em>YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]</em>"),
        verbose_name="Time Published")

    def __str__(self):
        """ Return the Article's title """
        return self.title
