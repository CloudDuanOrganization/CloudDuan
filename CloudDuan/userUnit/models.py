from django.db import models
from  django.contrib.auth.models import User
# Create your models here.

def userDirectoryPath(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'User/user_{0}/{1}'.format(instance.user.username, filename)


class CdUser(models.Model):
    user = models.OneToOneField(User)
    signature = models.CharField(max_length=200, null=True)
    portrait = models.ImageField(upload_to=userDirectoryPath,default='User/defaultImage/1.jpg')

    def __str__(self):
        return self.user.username
