from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from bots import views

app_name= 'bots'

urlpatterns = [
    url(r'^profile/(?P<profile_name>[\w\-]+)/$', views.show_profile, name ='show_profile'),
    url(r'^upgrade/$', views.upgrade, name='upgrade'),
    url(r'^leaderboards/$', views.leaderboards, name='leaderboards'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^get_bot/$', views.display_bot, name='display_bot'),
    url(r'^matchmake/$', views.validate, name = 'validate'),
    url(r'^initialize/$',views.initialize, name = 'initialize'),
    url('^update_team/$',views.resetTeam, name = 'resetTeam'),
    url(r'^create_bot/$',csrf_exempt(views.create_bot), name = 'create_bot'),
    url(r'^validate_new_bot/$',views.validate_name,name = 'validate_name'),
    url(r'^fight/$',views.fight,name = 'fight'),
]

