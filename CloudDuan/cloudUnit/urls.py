from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^duanPublish/$', views.duanPublish, name='duanPublish'),
    url(r'^duanView/(?P<duanID>\d+)/$', views.duanView, name='duanView'),
    url(r'^duanUp/$', views.duanUp, name='duanUp'),
    url(r'^duanDown/$', views.duanDown, name='duanDown'),
    url(r'^duanComment/$', views.duanComment, name='duanComment'),
    #TODO:前端页面的实现
    url(r'^duanCollect/$', views.duanCollect, name='duanCollect'),
    url(r'^duanList/$', views.duanList, name='duanList'),
    url(r'^hotList/$', views.hotList, name='hotList'),
    url(r'^newestList/$', views.newestList, name='newestList'),
    url(r'^rankList/$', views.rankList, name='rankList'),
    url(r'^hotView/(?P<duanID>\d+)/$', views.hotView, name='hotView'),
    url(r'^newestView/(?P<duanID>\d+)/$', views.newestView, name='newestView'),
    url(r'^rankView/(?P<duanID>\d+)/$', views.rankView, name='rankView'),
    url(r'^wanderView/$', views.wanderView, name='wanderView'),
    url(r'^addDuanLabel/$', views.addDuanLabel, name='addDuanLabel'),
    # url(r'^userRegister/$', views.userRegister, name='userRegister'),
    # url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    # url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
]