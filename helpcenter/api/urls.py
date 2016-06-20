from django.conf.urls import include, url

from rest_framework.routers import SimpleRouter

from helpcenter.api import views


router = SimpleRouter()
router.register(r'articles', views.ArticleViewSet)
router.register(r'categories', views.CategoryViewSet)


urlpatterns = [
    url(r'^permissions/$', views.PermissionsView.as_view(),
        name='permissions'),
    url(r'^', include(router.urls)),
]
