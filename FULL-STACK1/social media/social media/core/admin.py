from django.contrib import admin

from .models import Profile, Post, Comment, Like, Follow


# Register all models so we can manage them
# from Django Admin Panel

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)