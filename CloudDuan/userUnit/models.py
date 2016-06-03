from django.db import models
from  django.contrib.auth.models import User
# Create your models here.

# 用户文件的路径生成函数
def userDirectoryPath(instance, filename):
    # 文件将会被上传到 MEDIA_ROOT/user_<id>/<filename>
    return 'User/user_{0}/{1}'.format(instance.user.username, filename)

# 用户模型，使用ORM技术，将类与表单进行映射。而类的每一个实体则是数据库表中的一行。
class CdUser(models.Model): # 继承django自带的model
    user = models.OneToOneField(User) # 使用django的用户验证功能
    signature = models.CharField(max_length=200, null=True) # 用户的个性签名
    newsCount = models.IntegerField(null=False,default=0) # 用户的新消息数
    # 用户的头像，并规定了默认图片
    portrait = models.ImageField(upload_to=userDirectoryPath,default='User/defaultImage/1.jpg')

    def __str__(self):
        return self.user.username
