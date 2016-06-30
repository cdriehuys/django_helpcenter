from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('helpcenter.urls', app_name='helpcenter',
        namespace='help')),
]
