from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^userLogin/$', views.userLogin, name='userLogin'),
    # url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    # url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
]