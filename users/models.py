from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

### ✅ User Likes ###
class UserLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_given")
    liked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_received")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'liked_user')

    def __str__(self):
        return f"{self.user.username} ➝ {self.liked_user.username}"

### ✅ Friend Requests ###
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        status = "Accepted" if self.is_accepted else "Pending"
        return f"{self.sender.username} ➝ {self.receiver.username} ({status})"

### ✅ Notifications ###
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"📢 {self.user.username} - {'Read' if self.is_read else 'Unread'}"

### ✅ Messages (Fixed Duplicate) ###
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=255, default="No Subject")
    body = models.TextField()
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"📩 {self.sender.username} ➝ {self.receiver.username} ({'Read' if self.is_read else 'Unread'})"

### ✅ Blog Posts ###
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="blog_images/", null=True, blank=True)  # ✅ Image support

    def __str__(self):
        return self.title

### ✅ Comments ###
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"💬 {self.user.username} on {self.post.title}"

### ✅ User Profile ###
class UserProfile(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('friends', 'Friends Only')
    ]

    MESSAGE_CHOICES = [
        ('everyone', 'Everyone'),
        ('friends', 'Friends Only'),
        ('none', 'No One')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True, default=None)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)
    height = models.FloatField(null=True, blank=True, default=None)
    career = models.CharField(max_length=100, null=True, blank=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    contact_info = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True, default=0.0)
    longitude = models.FloatField(null=True, blank=True, default=0.0)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg', null=True, blank=True)

    # ✅ Privacy Settings
    profile_visibility = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    message_privacy = models.CharField(max_length=10, choices=MESSAGE_CHOICES, default='everyone')
    allow_in_search = models.BooleanField(default=True)

    def __str__(self):
        return f"👤 {self.user.username}"
