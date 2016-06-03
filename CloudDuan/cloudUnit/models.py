from django.db import models
from userUnit.models import CdUser
from CloudDuan.settings import MEDIA_ROOT
import os, base64
# Create your models here.


# 段子模型
class Duan(models.Model):
    title = models.CharField(max_length=50, null=True) # 标题
    content = models.TextField(null=False) # 内容
    pureContent = models.TextField(null=True) # 内容的纯文本
    publishTime = models.DateTimeField(auto_now_add=True) # 发布时间
    owner = models.ForeignKey(CdUser, related_name='duanOwner',null=False) # 发布人
    up = models.IntegerField(default=0) # 点赞数
    down = models.IntegerField(default=0) # 踩数
    hasCover = models.BooleanField(null=False, default=False) # 是否有封面的标识位
    image = models.TextField(null=True) # 封面图片
    liker = models.ManyToManyField(CdUser, related_name='like') # 记录点赞的用户，和CdUser是多对多的关系
    disliker = models.ManyToManyField(CdUser, related_name='dislike')# 记录踩的用户，和CdUser是多对多的关系
    collector = models.ManyToManyField(CdUser, related_name='collect')# 记录收藏的用户，和CdUser是多对多的关系
    viewCount = models.IntegerField(default=0) # 记录浏览数

    def __str__(self):
        return str(self.id) + str(self.title)

    class Meta:
        ordering = ['-publishTime'] # 在数据库中采用时间为序存放

# 段子评论
class Comment(models.Model):
    # 采用外键的方式将评论与段子联系起来，并采用CASCADE方式
    ofDuan = models.ForeignKey(Duan,related_name='comment',null=False,on_delete=models.CASCADE)
    content = models.TextField(null=False) # 评论的内容
    owner = models.ForeignKey(CdUser, related_name='commentOwner',null=False) # 评论人，使用外键的方式与CdUser关联
    publishTime = models.DateTimeField(auto_now_add=True)# 评论发布时间

    def __str__(self):
        return str(self.ofDuan) + str(self.id)


class DuanLabel(models.Model):
    text = models.TextField(max_length=10, null=False)
    ofDuan = models.ForeignKey(Duan,related_name="label",null=False)
    colour = models.IntegerField(null=False,default=0)

    def __str__(self):
        return self.text


class DuanHistory(models.Model):
    owner = models.ForeignKey(CdUser, null=False)
    duan = models.ForeignKey(Duan, null=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner) + str(self.duan) + str(self.time)

    class Meta:
        ordering = ['-time']


class DuanMessage(models.Model):
    fromUser = models.ForeignKey(CdUser, null=False, related_name='fromUser')
    toUser = models.ForeignKey(CdUser, null=False, related_name='toUser')
    duan = models.ForeignKey(Duan, null=False, related_name='duanMessage')
    content = models.CharField(max_length=20, null=False)
    time = models.DateTimeField(auto_now_add=True)
    isNew = models.BooleanField(default=True,null=False)

    def __str__(self):
        return str(self.fromUser) + '-->' + str(self.toUser) + ' ' + str(self.time)

    class Meta:
        ordering = ['-time']
