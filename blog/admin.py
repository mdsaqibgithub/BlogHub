from django.contrib import admin
from .models import Blog, Comment
admin.site.register(Blog)
# @admin.register(Blog)
# class BlogAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'total_likes')
admin.site.register(Comment)
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'blog', 'created_at', 'total_likes')
