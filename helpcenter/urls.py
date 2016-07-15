from django.conf.urls import include, url

from helpcenter import views


app_name = 'helpcenter'

urlpatterns = [
    url(r'^api/', include('helpcenter.api.urls', app_name='helpcenter-api',
        namespace='api')),
    url(r'^articles/create/$', views.ArticleCreateView.as_view(),
        name='article-create'),
    url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(),
        name='article-detail'),
    url(r'^articles/(?P<pk>[0-9]+)/delete/$',
        views.ArticleDeleteView.as_view(), name='article-delete'),
    url(r'^articles/(?P<pk>[0-9]+)/update/$',
        views.ArticleUpdateView.as_view(), name='article-update'),
    url(r'^categories/create/$', views.CategoryCreateView.as_view(),
        name='category-create'),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.CategoryDetailView.as_view(),
        name='category-detail'),
    url(r'^categories/(?P<pk>[0-9]+)/delete/$',
        views.CategoryDeleteView.as_view(), name='category-delete'),
    url(r'^categories/(?P<pk>[0-9]+)/update/$',
        views.CategoryUpdateView.as_view(), name='category-update'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]
