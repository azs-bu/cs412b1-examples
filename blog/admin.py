# blog/admin.py
# tell the admin we want to administer these models
from django.contrib import admin

from .models import * 
# Register your models here.

admin.site.register(Article)
admin.site.register(Comment) ## NEW
