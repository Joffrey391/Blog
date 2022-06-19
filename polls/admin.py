from django.contrib import admin

from .models import Post, Comment
from .admin_filters import PostTitleFilter

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "limit", "id")
    list_filter = ('user', 'limit')
    search_fields = ('title', 'user__nick', 'id', )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'user', 'id')
    list_filter = (PostTitleFilter, 'user')
    search_fields = ('post__title', 'user__nick', 'id')
    def post_title(self, obj):
        return obj.post.title