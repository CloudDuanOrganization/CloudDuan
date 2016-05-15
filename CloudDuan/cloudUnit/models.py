from django.db import models
from userUnit.models import CdUser
# Create your models here.

# def duanDirectoryPath(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     print(instance.title,instance,instance.numb)
#     return 'uploadFiles/Duan/duan_{0}/{1}'.format(instance.numb, filename)

class Duan(models.Model):
    title = models.CharField(max_length=50, null=True)
    content = models.TextField(null=False)
    publishTime = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CdUser, related_name='duanOwner',null=False)
    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploadFiles/Duan/%Y/%m/%d', null=True)
    def __str__(self):
        return self.title


class Comment(models.Model):
    ofDuan = models.ForeignKey(Duan,related_name='ofDuan',null=False)
    content = models.CharField(max_length=200, null=False)
    owner = models.ForeignKey(CdUser, related_name='commentOwner',null=False)
    publishTime = models.DateTimeField(auto_now_add=True)