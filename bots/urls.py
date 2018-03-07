from django.conf.urls import url, include
from bots import views

urlpatterns = [
    url(r'^profile/(?P<profile_name>[\w\-]+)/$', views.show_profile, name ='show_profile'),]
]