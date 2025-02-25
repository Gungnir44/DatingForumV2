from django.contrib import admin
from .models import UserProfile, Message, BlogPost, Comment, UserLike, FriendRequest, Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'career', 'income', 'profile_visibility', 'allow_in_search')
    list_filter = ('gender', 'career', 'profile_visibility', 'allow_in_search')
    search_fields = ('user__username', 'user__email', 'career')
    readonly_fields = ('latitude', 'longitude')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('sender__username', 'receiver__username', 'content')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'timestamp')
    search_fields = ('user__username', 'post__title', 'content')

@admin.register(UserLike)
class UserLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'liked_user')
    search_fields = ('user__username', 'liked_user__username')

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'is_accepted')
    list_filter = ('is_accepted',)
    search_fields = ('sender__username', 'receiver__username')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'message')
