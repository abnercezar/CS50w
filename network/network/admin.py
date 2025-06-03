from django.contrib import admin
from .models import Post, User, Like, Follow

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Follow)