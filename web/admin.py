from django.contrib import admin
from web.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Article)
admin.site.register(ArticleTag)
admin.site.register(Comment)
