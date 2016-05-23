from django.db import models
from userUnit.models import CdUser
from CloudDuan.settings import MEDIA_ROOT
import os, base64
# Create your models here.

# def duanDirectoryPath(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     print(instance.title,instance,instance.numb)
#     return 'uploadFiles/Duan/duan_{0}/{1}'.format(instance.numb, filename)


class Duan(models.Model):
    title = models.CharField(max_length=50, null=True)
    content = models.TextField(null=False)
    pureContent = models.TextField(null=True)
    publishTime = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CdUser, related_name='duanOwner',null=False)
    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    hasCover = models.BooleanField(null=False, default=False)
    image = models.TextField(null=True)
    liker = models.ManyToManyField(CdUser, related_name='like')
    disliker = models.ManyToManyField(CdUser, related_name='dislike')
    collector = models.ManyToManyField(CdUser, related_name='collect')
    viewCount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + str(self.title)

    class Meta:
        ordering = ['-publishTime']


class Comment(models.Model):
    ofDuan = models.ForeignKey(Duan,related_name='comment',null=False,on_delete=models.CASCADE)
    content = models.CharField(max_length=200, null=False)
    owner = models.ForeignKey(CdUser, related_name='commentOwner',null=False)
    publishTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ofDuan) + str(self.id)


class DuanLabel(models.Model):
    text = models.TextField(max_length=10, null=False)
    ofDuan = models.ForeignKey(Duan,related_name="label",null=False)

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
