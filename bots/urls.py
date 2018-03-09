from django.conf.urls import url, include
from bots import views

urlpatterns = [
    url(r'^profile/(?P<profile_name>[\w\-]+)/$', views.show_profile, name ='show_profile'),
    url(r'^upgrade/$', views.upgrade, name='upgrade'),
    url(r'^leaderboards/$', views.leaderboards, name='leaderboards'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signup/$', views.signup, name='signup'),
]
