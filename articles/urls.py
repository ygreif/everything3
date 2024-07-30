from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^edit/stub/(.*)/$', views.complete_stub),
    re_path(r'^new/something/$', views.new_something),
    re_path(r'^new/article/(.*)/$', views.new_article),
    re_path(r'^view/article/(.*)/$', views.view_article),
    re_path(r'^new/topic/(.*)/$', views.new_topic),
    re_path(r'^search/$', views.search),
]
