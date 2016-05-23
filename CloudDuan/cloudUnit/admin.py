from django.contrib import admin
from .models import Duan,Comment, DuanHistory, DuanMessage, DuanLabel

# Register your models here.
admin.site.register(Duan)
admin.site.register(Comment)
admin.site.register(DuanHistory)
admin.site.register(DuanLabel)
admin.site.register(DuanMessage)