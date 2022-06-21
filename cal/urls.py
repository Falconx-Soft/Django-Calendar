from argparse import Namespace
from django.conf.urls import url
from . import views
from django.urls import path, include
from rest_framework import routers
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
# Serializers define the API representation.


router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet, basename='Event_')

app_name = 'cal'
urlpatterns = [
    path('events_api_view/', include(router.urls)),
    url(r'^index/$', views.index, name='index'),
    url(r'calendar', views.CalendarView.as_view(), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
	url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    url('register',views.register,name='register'),
    url('logout', views.logoutUser, name="logout"),
    url('', views.loginUser, name="login"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
