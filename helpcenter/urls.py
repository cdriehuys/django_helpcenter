from django.conf.urls import include, url

from helpcenter import views


app_name = 'helpcenter'

urlpatterns = [
    url(r'^api/', include('helpcenter.api.urls', app_name='helpcenter-api',
        namespace='api')),
    url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(),
        name='article-detail'),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.CategoryDetailView.as_view(),
        name='category-detail'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]
