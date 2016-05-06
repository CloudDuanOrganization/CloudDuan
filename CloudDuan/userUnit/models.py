from django.db import models
from  django.contrib.auth.models import User
# Create your models here.

class CdUser(models.Model):
    user = models.OneToOneField(User)
    signature = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.user.username