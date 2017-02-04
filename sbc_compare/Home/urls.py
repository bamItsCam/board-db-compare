from django.conf.urls import url, include
from . import views

urlpatterns = [
  # NOTE: the root url (r'^') HAS TO BE LAST in this list or else there is an error where the root url overrides other urls
    url(r'^about/', views.about, name='about'),
    url(r'^compare/',views.compare,name='compare'),
    url(r'^', views.select_boards, name='select_boards')
]
