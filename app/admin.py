from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django_summernote.admin import SummernoteModelAdmin  # Add this import

# Register your models here.

class BlogAdmin(SummernoteModelAdmin):  # Changed from ModelAdmin to SummernoteModelAdmin
    list_display = ('title', 'author', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('category', 'created_at')
    summernote_fields = ('content',)  # Add this line to enable Summernote for content field

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'created_at')
    list_filter = ('email', 'created_at')
    search_fields = ('name', 'email', 'subject')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'content', 'created_at')
    search_fields = ('blog__title', 'user__username', 'content')
    list_filter = ('created_at',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_at')
    search_fields = ('blog__title', 'user__username')
    list_filter = ('created_at',)

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'roll')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('roll', 'bio', 'profile_picture', 'twitter', 'linkedin', 'website')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('roll', 'bio', 'profile_picture', 'twitter', 'linkedin', 'website')}),
    )

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active')
    search_fields = ('email',)
    ordering = ('-created_at',)

admin.site.register(User, UserAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)