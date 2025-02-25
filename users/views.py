from users.forms import UserRegistrationForm
from .forms import UserProfileForm
from .models import BlogPost, Comment, Message, User, UserLike, FriendRequest, Notification
from .forms import BlogPostForm, UserSearchForm, MessageForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import UserProfile
from django.conf import settings
from math import radians, sin, cos, sqrt, atan2
from .models import BlogPost
from .forms import BlogForm

@login_required
def blog_delete(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)

    # ✅ Ensure only the author can delete
    if request.user != blog.author:
        return redirect("blog_detail", blog_id=blog.id)

    if request.method == "POST":
        blog.delete()
        return redirect("blog_list")

    return render(request, "users/blog_confirm_delete.html", {"blog": blog})

@login_required
def blog_edit(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)

    # ✅ Ensure only the blog author can edit
    if request.user != blog.author:
        return redirect("blog_detail", blog_id=blog.id)

    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)

    return render(request, "users/blog_edit.html", {"form": form, "blog": blog})


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure only the comment's author or an admin can delete it
    if request.user == comment.user or request.user.is_staff:
        comment.delete()
        return redirect('blog_post_detail', post_id=comment.post.id)  # Redirect to the post

    return redirect('blog_post_detail', post_id=comment.post.id)  # Prevent unauthorized deletion

def blog_post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.order_by('-timestamp')  # Show newest comments first

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('blog_post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'users/blog_post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.sender or request.user == message.receiver:
        message.delete()
        messages.success(request, "Message deleted successfully!")
        return redirect("inbox")
    else:
        messages.error(request, "You don't have permission to delete this message.")
        return redirect("inbox")

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.receiver:
        message.is_read = True
        message.save()
    return render(request, "users/view_message.html", {"message": message})


def search_users(request):
    user_lat = request.GET.get("latitude")
    user_lon = request.GET.get("longitude")
    max_distance = float(request.GET.get("distance", 50))  # Default to 50 miles

    if not user_lat or not user_lon:
        return render(request, "users/search.html", {"error": "Location data is required."})

    user_lat = float(user_lat)
    user_lon = float(user_lon)

    users = UserProfile.objects.exclude(latitude=None).exclude(longitude=None)

    filtered_users = []
    for user in users:
        if user.latitude is not None and user.longitude is not None:
            # Calculate distance (use a function or library like geopy)
            distance = haversine(user_lat, user_lon, user.latitude, user.longitude)
            if distance <= max_distance:
                filtered_users.append(user)

    context = {
        "users": filtered_users,
        "google_api_key": settings.GOOGLE_MAPS_API_KEY,  # Pass API key for the map
    }

    return render(request, "users/search.html", context)

def map_view(request):
    return render(request, 'users/map.html', {'google_api_key': settings.GOOGLE_MAPS_API_KEY})

def user_locations(request):
    users = UserProfile.objects.exclude(latitude=None).exclude(longitude=None)
    user_data = [
        {
            "username": user.user.username,
            "latitude": user.latitude,
            "longitude": user.longitude,
            "career": user.career,
            "income": float(user.income) if user.income else "N/A",
        }
        for user in users
    ]
    return JsonResponse({"users": user_data})

def user_logout(request):
    logout(request)
    return redirect('login')  # ✅ Redirect to login page after logout

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # ✅ Redirect to dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def notifications(request):
    return render(request, "users/notifications.html")


@login_required
def dashboard(request):
    blogs = BlogPost.objects.order_by('-created_at')[:5]  # ✅ Fetch latest 5 blogs
    return render(request, 'users/dashboard.html', {'blogs': blogs})


@login_required
def like_profile(request, user_id):
    liked_user = get_object_or_404(User, id=user_id)

    existing_like = UserLike.objects.filter(user=request.user, liked_user=liked_user).first()
    if existing_like:
        existing_like.delete()
        return JsonResponse({'status': 'unliked'})
    else:
        UserLike.objects.create(user=request.user, liked_user=liked_user)
        if UserLike.objects.filter(user=liked_user, liked_user=request.user).exists():
            return JsonResponse({'status': 'match'})
        return JsonResponse({'status': 'liked'})


@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    if not FriendRequest.objects.filter(sender=request.user, receiver=receiver).exists():
        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        return JsonResponse({'status': 'sent'})
    else:
        return JsonResponse({'status': 'already_sent'})


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    friend_request.is_accepted = True
    friend_request.save()
    return JsonResponse({'status': 'accepted'})


@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    friend_request.delete()
    return JsonResponse({'status': 'rejected'})


@login_required
def notifications_list(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'users/notifications.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications_list')


@login_required
def inbox(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, "users/inbox.html", {"messages_received": messages_received})


@login_required
def sent_messages(request):
    messages_sent = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, "users/sent_messages.html", {"messages_sent": messages_sent})


@login_required
def message_thread(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(sender=request.user, receiver=other_user) | Message.objects.filter(sender=other_user, receiver=request.user)
    messages = messages.order_by('timestamp')

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()
            return redirect('message_thread', username=username)
    else:
        form = MessageForm()

    return render(request, 'users/message_thread.html', {'messages': messages, 'form': form, 'other_user': other_user})


@login_required
def send_message(request, username):
    receiver = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('message_thread', username=username)
    else:
        form = MessageForm()

    return render(request, 'users/send_message.html', {'form': form, 'receiver': receiver})


def blog_list(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'users/blog_list.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    return render(request, 'users/blog_detail.html', {'blog': blog})


@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'users/blog_create.html', {'form': form})

@login_required
def my_profile(request):
    return redirect("profile", username=request.user.username)

@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=profile_user)
    blogs = BlogPost.objects.filter(author=profile_user).order_by('-created_at')  # ✅ Get user's blogs

    if user_profile.profile_visibility == 'private' and request.user != profile_user:
        return render(request, 'users/private_profile.html')

    if user_profile.profile_visibility == 'friends' and request.user not in profile_user.friends.all():
        return render(request, 'users/private_profile.html')

    return render(request, 'users/profile.html', {'user_profile': user_profile, 'blogs': blogs})



@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)

            # ✅ Save geolocation if enabled
            if "latitude" in request.POST and "longitude" in request.POST:
                profile.latitude = request.POST.get("latitude", 0.0)
                profile.longitude = request.POST.get("longitude", 0.0)

            profile.save()
            return redirect("profile", username=request.user.username)

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, "users/edit_profile.html", {"form": form})

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # ✅ Create the User first
            user = User.objects.create_user(
                username=user_form.cleaned_data["username"],
                password=user_form.cleaned_data["password1"],  # Ensure `password1` is in `UserRegistrationForm`
                email=user_form.cleaned_data["email"]
            )

            # ✅ Create the UserProfile linked to the new user
            profile = profile_form.save(commit=False)
            profile.user = user  # Associate profile with the newly created user

            # ✅ Save location only if geolocation is enabled
            if "geolocation_enabled" in request.POST:
                profile.latitude = request.POST.get("latitude", 0.0)
                profile.longitude = request.POST.get("longitude", 0.0)

            profile.save()
            return redirect("profile", username=user.username)

    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, "users/register.html", {"user_form": user_form, "profile_form": profile_form})
