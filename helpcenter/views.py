from django.shortcuts import render
from django.views import generic

from helpcenter import models
from helpcenter.backends.search import SimpleSearch
from helpcenter.mixins import PermissionsMixin


class ArticleCreateView(PermissionsMixin, generic.edit.CreateView):
    """ View for creating new Article instances """
    fields = ('title', 'body', 'category')
    model = models.Article
    permissions = ('helpcenter.add_article',)
    template_name_suffix = '_create'


class ArticleDeleteView(PermissionsMixin, generic.edit.DeleteView):
    """ View for deleting an Article instance """
    model = models.Article
    permissions = ('helpcenter.delete_article',)

    def get_success_url(self):
        """ Redirect to the instance's parent """
        return self.object.get_parent_url()


class ArticleDetailView(generic.DetailView):
    """ View for viewing an article's details """
    model = models.Article


class ArticleUpdateView(PermissionsMixin, generic.edit.UpdateView):
    """ View for updating Article instances """
    fields = ('title', 'body', 'category')
    model = models.Article
    permissions = ('helpcenter.change_article',)
    template_name_suffix = '_update'


class CategoryCreateView(PermissionsMixin, generic.edit.CreateView):
    """ View for creating new Category instances """
    fields = ('title', 'parent')
    model = models.Category
    permissions = ('helpcenter.add_category',)
    template_name_suffix = '_create'


class CategoryDeleteView(PermissionsMixin, generic.edit.DeleteView):
    """ View for deleting Category instances """
    model = models.Category
    permissions = ('helpcenter.delete_category',)

    def get_success_url(self):
        """ Return the url of the instances parent """
        return self.object.get_parent_url()


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


class CategoryUpdateView(PermissionsMixin, generic.edit.UpdateView):
    """ View for updating existing Category instances """
    fields = ('title', 'parent')
    model = models.Category
    permissions = ('helpcenter.change_category',)
    template_name_suffix = '_update'


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


class SearchView(generic.View):
    """ View for searching article database """
    template_name = 'helpcenter/search.html'
    query_parameter = 'q'
    search_backend = SimpleSearch()

    def get(self, request, *args, **kwargs):
        """ Handle GET requests """
        self.request = request

        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, *args, **kwargs):
        """ Get context data for a request """
        context = {}

        query = self.request.GET.get(self.query_parameter, None)

        articles = self.get_search_results(query)
        context['articles'] = articles

        context['query'] = query

        return context

    def get_search_results(self, query):
        """ Return the results of a given query """
        if not query:
            return models.Article.objects.none()

        return self.search_backend.search(query)
