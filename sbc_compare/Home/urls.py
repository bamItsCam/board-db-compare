from django.conf.urls import url, include
from . import views

urlpatterns = [
  # NOTE: the root url (r'^') HAS TO BE LAST in this list or else there is an error where the root url overrides other urls
  # NOTE2: $ is necessary if two routes start with a similar string
    url(r'^about', views.about, name='about'),
    url(r'^compare',views.compare,name='compare'),
    url(r'^search$', views.search_boards, name='search_boards'),
    url(r'^search_post$',views.search_post,name='search_post'),
    url(r'^add_post$',views.add_post,name='add_post'),
    url(r'^', views.select_boards, name="select_boards"),
]
