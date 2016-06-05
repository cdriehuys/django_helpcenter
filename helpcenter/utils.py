from django.core.urlresolvers import reverse


def article_detail(article=None, pk=None):
    """ Get the detail url of an article """
    if article is None and pk is None:
        raise ValueError("Either 'article' or 'pk' must not be None.")

    if pk is None and article is not None:
        pk = article.pk

    reverse_kwargs = {
        'pk': pk,
    }

    return reverse('article-detail', kwargs=reverse_kwargs)
