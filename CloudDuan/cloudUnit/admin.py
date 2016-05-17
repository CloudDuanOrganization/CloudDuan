from django.contrib import admin
from .models import Duan,Comment, DuanHistory

# Register your models here.
admin.site.register(Duan)
admin.site.register(Comment)
admin.site.register(DuanHistory)