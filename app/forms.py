from django import forms 
from .models import *
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    roll = forms.CharField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)
    twitter = forms.URLField(required=False)
    linkedin = forms.URLField(required=False)
    website = forms.URLField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',
                 'roll', 'bio', 'profile_picture', 'twitter', 'linkedin', 'website']

class ProfileUpdateForm(UserChangeForm):
    password = None  # Remove the password field

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'email',
            'roll',
            'bio',
            'profile_picture',
            'twitter',
            'linkedin',
            'website',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
            'roll': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 'created_at', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'border: 1px solid #ced4da;'}),
        }
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'style': 'border: 1px solid #ced4da;'}),
        }
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'px-4 py-3 rounded-l-lg w-full text-gray-900 focus:outline-none',
                'placeholder': 'Your email',
                'required': True
            })
        }