from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import validate_email
from django.utils.safestring import mark_safe

# Create your models here.



class User(AbstractUser):
    roll = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    @property
    def social_links(self):
        """Return a dictionary of all social links"""
        return {
            'twitter': self.twitter,
            'linkedin': self.linkedin,
            'website': self.website,
        }
    
    @property
    def has_social_links(self):
        """Check if user has any social links"""
        return any(self.social_links.values())
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})
    
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


  
class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('Technology', 'Technology'),
        ('Travel', 'Travel'),
        ('Food', 'Food'),
        ('Lifestyle', 'Lifestyle'),
        ('Business', 'Business'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE , related_name='blogs')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Technology')
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    def get_content(self):
        return mark_safe(self.content)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('blog', 'user')
    
    def __str__(self):
        return f"{self.user.username} likes {self.blog.title}"
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True, default=None)
    subject = models.CharField(max_length=100, default='None')
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class Subscriber(models.Model):
    email = models.EmailField(
        unique=True,
        validators=[validate_email]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']