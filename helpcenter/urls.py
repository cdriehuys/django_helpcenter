from django.conf.urls import url

from helpcenter import views


urlpatterns = [
    url(r'^articles/$', views.ArticleListView.as_view(), name='article-list'),
    url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(),
        name='article-detail'),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.CategoryDetailView.as_view(),
        name='category-detail'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]
