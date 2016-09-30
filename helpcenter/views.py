from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views import generic

from helpcenter import models
from helpcenter.mixins import OptionalFormMixin, PermissionsMixin


class ArticleCreateView(OptionalFormMixin, PermissionsMixin,
                        generic.edit.CreateView):
    """View for creating new Article instances."""
    fields = ('title', 'body', 'category', 'draft')
    form_class_setting = 'HELPCENTER_ARTICLE_CREATE_FORM'
    model = models.Article
    permissions = ('helpcenter.add_article',)
    pk_url_kwarg = 'article_pk'
    template_name_suffix = '_create'


class ArticleDeleteView(PermissionsMixin, generic.edit.DeleteView):
    """ View for deleting an Article instance """
    model = models.Article
    permissions = ('helpcenter.delete_article',)
    pk_url_kwarg = 'article_pk'

    def get_success_url(self):
        """ Redirect to the instance's parent """
        return self.object.get_parent_url()


class ArticleDetailView(generic.DetailView):
    """ View for viewing an article's details """
    model = models.Article
    pk_url_kwarg = 'article_pk'


class ArticleUpdateView(OptionalFormMixin, PermissionsMixin,
                        generic.edit.UpdateView):
    """ View for updating Article instances """
    fields = ('title', 'body', 'category', 'draft')
    form_class_setting = 'HELPCENTER_ARTICLE_UPDATE_FORM'
    model = models.Article
    permissions = ('helpcenter.change_article',)
    pk_url_kwarg = 'article_pk'
    template_name_suffix = '_update'


class CategoryCreateView(OptionalFormMixin, PermissionsMixin,
                         generic.edit.CreateView):
    """View for creating new Category instances."""
    fields = ('title', 'parent')
    form_class_setting = 'HELPCENTER_CATEGORY_CREATE_FORM'
    model = models.Category
    permissions = ('helpcenter.add_category',)
    pk_url_kwarg = 'category_pk'
    template_name_suffix = '_create'


class CategoryDeleteView(PermissionsMixin, generic.edit.DeleteView):
    """ View for deleting Category instances """
    model = models.Category
    permissions = ('helpcenter.delete_category',)
    pk_url_kwarg = 'category_pk'

    def get_success_url(self):
        """ Return the url of the instances parent """
        return self.object.get_parent_url()


class CategoryDetailView(generic.DetailView):
    """ View for viewing a Category's details """
    model = models.Category
    pk_url_kwarg = 'category_pk'

    def get_context_data(self, *args, **kwargs):
        """ Add custom context data """
        context = super(CategoryDetailView, self).get_context_data(
            *args, **kwargs)

        articles = self.object.article_list

        if not self.request.user.has_perm('helpcenter.change_article'):
            articles = articles.exclude(draft=True)

        context['articles'] = self._paginate_query(articles)

        child_categories = models.Category.objects.filter(parent=self.object)
        context['categories'] = child_categories

        return context

    def _paginate_query(self, query):
        """Paginate the given query."""
        per_page = getattr(settings, 'HELPCENTER_ARTICLES_PER_PAGE', 10)
        paginator = Paginator(query, per_page)

        page = self.request.GET.get('page')
        try:
            return paginator.page(page)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)


class CategoryUpdateView(OptionalFormMixin, PermissionsMixin,
                         generic.edit.UpdateView):
    """ View for updating existing Category instances """
    fields = ('title', 'parent')
    form_class_setting = 'HELPCENTER_CATEGORY_UPDATE_FORM'
    model = models.Category
    permissions = ('helpcenter.change_category',)
    pk_url_kwarg = 'category_pk'
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
