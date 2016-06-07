from django.shortcuts import render
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


class CategoryDetailView(generic.DetailView):
    """ View for viewing a Category's details """
    model = models.Category

    def get_context_data(self, *args, **kwargs):
        """ Add custom context data """
        context = super(CategoryDetailView, self).get_context_data(
            *args, **kwargs)

        articles = models.Article.objects.filter(category=self.object)
        context['articles'] = articles

        child_categories = models.Category.objects.filter(parent=self.object)
        context['categories'] = child_categories

        return context


class IndexView(generic.View):
    """ View for the helpcenter index (home page) """
    template_name = 'helpcenter/index.html'

    def get(self, request, *args, **kwargs):
        """ Handle get requests """
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, *args, **kwargs):
        """ Get context data for a request """
        context = {}

        articles = models.Article.objects.filter(category=None)
        context['articles'] = articles

        categories = models.Category.objects.filter(parent=None)
        context['categories'] = categories

        return context
