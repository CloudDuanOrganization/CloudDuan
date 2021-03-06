from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^userLogin/$', views.userLogin, name='userLogin'),
    url(r'^userLogout/$', views.userLogout, name='userLogout'),
    url(r'^userRegister/$', views.userRegister, name='userRegister'),
    url(r'^userProfile/$', views.toUserProfile, name='toUserProfile'),
    url(r'^userProfile/userOwn/$', views.userProfileOwn, name='userProfileOwn'),
    url(r'^userProfile/history/$', views.userProfileHistory, name='userProfileHistory'),
    url(r'^userMessageCenter/$', views.userMessageCenter, name='userMessageCenter'),
    url(r'^userCollection/$', views.userCollection, name='userCollection'),
    #TODO:此网址仅供测试用，之后删除
    url(r'^uploadPortrait/$', views.uploadPortrait, name='uploadPortrait'),
    url(r'^changeSignature/$', views.changeSignature, name='changeSignature'),
    # url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    # url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
]