from django.urls import path
from .views import (
    register, user_login, user_logout, profile, edit_profile, user_locations, map_view,
    notifications_list, mark_notification_read, like_profile, send_friend_request,
    accept_friend_request, reject_friend_request, search_users,
    inbox, message_thread, send_message, view_message, delete_message, sent_messages,
    blog_post_detail, blog_list, blog_detail, blog_create, delete_comment, notifications, blog_list, blog_detail, blog_create, blog_edit, blog_delete
)
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('profile/edit/', views.edit_profile, name='edit_profile'),  # ✅ Fix: Place this before <str:username>
    path('profile/', views.my_profile, name='my_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('like/<int:user_id>/', like_profile, name='like_profile'),
    path('friend-request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('reject-request/<int:request_id>/', reject_friend_request, name='reject_friend_request'),

    # Map & Geolocation
    path('map/', map_view, name='map'),
    path('locations/', user_locations, name='user_locations'),

    # Search
    path('search/', search_users, name='search_users'),

    # Blog system
    path("blogs/", blog_list, name="blog_list"),
    path("blogs/<int:blog_id>/", blog_detail, name="blog_detail"),
    path("blogs/new/", blog_create, name="blog_create"),
    path("blogs/<int:blog_id>/edit/", blog_edit, name="blog_edit"),  # ✅ Fix this
    path("blogs/<int:blog_id>/delete/", blog_delete, name="blog_delete"),

    # Messaging system
    path('inbox/', inbox, name='inbox'),
    path('messages/<str:username>/', message_thread, name='message_thread'),
    path('send_message/<str:username>/', views.send_message, name='send_message'),
    path('sent_messages/', sent_messages, name='sent_messages'),
    path('message/<int:message_id>/', view_message, name='view_message'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),

    # Notifications
    path('notifications/', views.notifications_list, name='notifications_list'),

    path('notifications/read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),

    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
