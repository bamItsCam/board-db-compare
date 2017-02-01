from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^', views.index, name='index') # The Home page shows up at the default URL (currently http:\\127.0.0.1:8000)
]
