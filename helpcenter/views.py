from django.views import generic

from helpcenter import models


class ArticleDetailView(generic.DetailView):
    """ View for viewing an article's details """
    model = models.Article


class ArticleListView(generic.ListView):
    """ View for listing articles """
    context_object_name = 'articles'
    model = models.Article
    ordering = ['title']
