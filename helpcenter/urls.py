from django.conf.urls import url

from helpcenter import views


urlpatterns = [
    url(r'articles/$', views.ArticleListView.as_view(), name='article-list'),
]
