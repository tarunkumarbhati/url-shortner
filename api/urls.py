from django.conf.urls import url
import views

urlpatterns = [
    url(r'^fetch/short-url', views.short_url, name='short-url'),
    url(r'^fetch/long-url', views.long_url, name='long-url'),
    url(r'^fetch/short-urls', views.short_urls, name='short-urls'),
    url(r'^fetch/long-urls', views.long_urls, name='long-urls'),
    url(r'^fetch/count', views.count, name='count'),
    url(r'^clean-urls', views.clean_urls, name='clean-urls'),
    url(r'^(?P<unique_hash>.*)', views.url_redirect, name='url-redirect'),
]
