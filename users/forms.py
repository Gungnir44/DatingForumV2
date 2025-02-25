from django.contrib.auth.models import User
from .models import UserProfile, BlogPost, Message, Comment
from django import forms
from .models import BlogPost  # ✅ Ensure this import is correct

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost  # ✅ Make sure BlogPost is imported
        fields = ["title", "content", "image"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']  # ✅ Correct fields
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Enter subject...'}),
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords must match.")

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'age', 'gender', 'height', 'career', 'income', 'latitude', 'longitude',
            'profile_picture', 'contact_info', 'profile_visibility', 'message_privacy', 'allow_in_search'
        ]
        widgets = {
            'profile_visibility': forms.Select(choices=UserProfile.PRIVACY_CHOICES),
            'message_privacy': forms.Select(choices=UserProfile.MESSAGE_CHOICES),
            'allow_in_search': forms.CheckboxInput()
        }
        geolocation_enabled = forms.BooleanField(
            required=False, label="Enable Geolocation")

    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        return latitude if latitude is not None else 0.0

    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        return longitude if longitude is not None else 0.0

class UserSearchForm(forms.Form):
    distance = forms.IntegerField(label="Max Distance (km)", min_value=1, initial=50)
    min_age = forms.IntegerField(label="Min Age", required=False)
    max_age = forms.IntegerField(label="Max Age", required=False)
    gender = forms.ChoiceField(label="Gender", choices=[('', 'Any'), ('Male', 'Male'), ('Female', 'Female')], required=False)
    career = forms.CharField(label="Career", required=False)
    min_income = forms.DecimalField(label="Min Income ($)", required=False, decimal_places=2, max_digits=10)
    max_income = forms.DecimalField(label="Max Income ($)", required=False, decimal_places=2, max_digits=10)
