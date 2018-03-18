from django.conf.urls import url
import views

urlpatterns = [
    # url(r'^/', views.index, name='index'),
    url(r'^fetch/short-url/', views.short_url, name='short-url'),

]
