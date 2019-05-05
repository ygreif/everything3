from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit/stub/(.*)/$', views.complete_stub),
    url(r'^new/something/(.*)/$', views.new_something),
    url(r'^new/article/(.*)/$', views.new_article),
    url(r'^new/topic/(.*)/$', views.new_topic),
    url(r'^search/$', views.search),
]
