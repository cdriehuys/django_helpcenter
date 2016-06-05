from django.conf.urls import url

from helpcenter import views


urlpatterns = [
    url(r'articles/$', views.ArticleListView.as_view(), name='article-list'),
    url(r'articles/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(),
        name='article-detail'),
]
