from django.conf.urls import include, url

from helpcenter import views


app_name = 'helpcenter'

article_urls = [
    url(r'^create/$', views.ArticleCreateView.as_view(),
        name='article-create'),
    url(r'^(?P<article_pk>[0-9]+)/(?P<article_slug>[-\w]+)/', include([
        url(r'^$', views.ArticleDetailView.as_view(), name='article-detail'),
        url(r'^delete/$', views.ArticleDeleteView.as_view(),
            name='article-delete'),
        url(r'^update/$', views.ArticleUpdateView.as_view(),
            name='article-update'),
    ])),
]

category_urls = [
    url(r'^create/$', views.CategoryCreateView.as_view(),
        name='category-create'),
    url(r'^(?P<category_pk>[0-9]+)/(?P<category_slug>[-\w]+)/', include([
        url(r'^$', views.CategoryDetailView.as_view(),
            name='category-detail'),
        url(r'^delete/$', views.CategoryDeleteView.as_view(),
            name='category-delete'),
        url(r'^update/$', views.CategoryUpdateView.as_view(),
            name='category-update'),
    ])),
]

urlpatterns = [
    url(r'^api/', include('helpcenter.api.urls', app_name='helpcenter-api',
        namespace='api')),
    url(r'^articles/', include(article_urls)),
    url(r'^categories/', include(category_urls)),
    url(r'^$', views.IndexView.as_view(), name='index'),
]
