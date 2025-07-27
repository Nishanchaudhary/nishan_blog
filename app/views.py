from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import re
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseNotFound
from django.template.exceptions import TemplateDoesNotExist


# Create your views here.
def Home(request):
    blogs_list = Blog.objects.all().order_by('-created_at')
    technology_count = sum(1 for blog in blogs_list if blog.category == 'Technology')
    travel_count = sum(1 for blog in blogs_list if blog.category == 'Travel')
    food_count = sum(1 for blog in blogs_list if blog.category == 'Food')
    lifestyle_count = sum(1 for blog in blogs_list if blog.category == 'Lifestyle')
    business_count = sum(1 for blog in blogs_list if blog.category == 'Business')

    category_counts = Blog.objects.values('category').annotate(count=Count('id'))
    category_data = {
        'Technology': 0,
        'Travel': 0,
        'Food': 0,
        'Lifestyle': 0,
        'Other': 0
    }
    
    for item in category_counts:
        category_data[item['category']] = item['count']
    
   
    content = {
        'technology': technology_count,
        'travel': travel_count,
        'food': food_count,
        'lifestyle': lifestyle_count,
        'business': business_count,
        'categories': category_data,
    }
    return render(request, 'app/home.html', {'blogs': blogs_list, 'content': content})

def my_blogs(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your blogs.")
        return redirect('login')
    blogs_list = Blog.objects.filter(author=request.user).order_by('-created_at')
    paginator = Paginator(blogs_list, 9)  # Show 9 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app/myblog.html', {'page_obj': page_obj, 'blogs': blogs_list})


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully. Please log in.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserForm()
    return render(request, 'app/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

@login_required
def profile(request, username=None):
    # If no username is provided, show the current user's profile
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    context = {
        'profile_user': user,
        'social_links': getattr(user, 'social_links', None),
        'has_social_links': getattr(user, 'has_social_links', False)
    }
    return render(request, 'app/profile.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'app/profile_update.html', {'form': form})

def blog_list(request):
    blogs_list = Blog.objects.all().order_by('-created_at')
    category = request.GET.get('category')
    if category:
        blogs_list = blogs_list.filter(category=category)
        if not blogs_list.exists():
            messages.warning(request, f"No blogs found in category '{category}'.")
    paginator = Paginator(blogs_list, 9)  # Show 9 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/blog_list.html', {'page_obj': page_obj, 'blogs': blogs_list, 'selected_category': category})

def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    comments = blog.comments.all()
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You need to login to comment.")
            return redirect('login')  # Assuming you have a login URL
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('blog_detail', blog_id=blog.id)
    else:
        comment_form = CommentForm()
        
    return render(request, 'app/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form
    })

def comment(request, blog_id):
    if request.user.is_authenticated:
        blog = Blog.objects.get(id=blog_id)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.author = request.user
                comment.save()
                messages.success(request, "Comment added successfully.")
                return redirect('blog_detail', blog_id=blog.id)
        else:
            form = CommentForm()
        return render(request, 'app/add_comment.html', {'form': form, 'blog': blog})
    else:
        messages.error(request, "You need to be logged in to comment on a blog.")
        return redirect('login/')
    
@login_required
def delete_comment(request, comment_id):
            comment = get_object_or_404(Comment, id=comment_id)
            if comment.user == request.user or request.user.is_superuser:
                blog_id = comment.blog.id
                comment.delete()
                messages.success(request, "Comment deleted successfully.")
                return redirect('blog_detail', blog_id=blog_id)
            else:
                messages.error(request, "You are not authorized to delete this comment.")
                return redirect('blog_detail', blog_id=comment.blog.id)

        

def like_blog(request, blog_id):
    if request.user.is_authenticated:
        blog = Blog.objects.get(id=blog_id)
        like, created = Like.objects.get_or_create(blog=blog, user=request.user)
        if created:
            messages.success(request, "You liked the blog.")
        else:
            like.delete()
            messages.info(request, "You unliked the blog.")
        return redirect('blog_detail', blog_id=blog.id)
    else:
        messages.error(request, "You need to be logged in to like a blog.")
        return redirect('login/')
    
def delete_blog(request, blog_id):
    if request.user.is_authenticated:
        blog = Blog.objects.get(id=blog_id)
        if blog.author == request.user:
            blog.delete()
            messages.success(request, "Blog deleted successfully.")
        else:
            messages.error(request, "You are not authorized to delete this blog.")
        return redirect('profile')
    else:
        messages.error(request, "You need to be logged in to delete a blog.")
        return redirect('login/')
    
def edit_blog(request, blog_id):
    if request.user.is_authenticated:
        blog = Blog.objects.get(id=blog_id)
        if blog.author == request.user:
            if request.method == "POST":
                form = BlogForm(request.POST, instance=blog)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Blog updated successfully.")
                    return redirect('blog_detail', blog_id=blog.id)
            else:
                form = BlogForm(instance=blog)
            return render(request, 'app/edit_blog.html', {'form': form, 'blog': blog})
        else:
            messages.error(request, "You are not authorized to edit this blog.")
            return redirect('profile')
    else:
        messages.error(request, "You need to be logged in to edit a blog.")
        return redirect('login/')
    
@login_required
def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                blog = form.save(commit=False)
                blog.author = request.user
                blog.save()
                messages.success(request, "Blog created successfully.")
                return redirect('blog_detail', blog_id=blog.id)
            except Exception as e:
                messages.error(request, f"An error occurred while saving: {str(e)}")
        else:
            # Improved error handling with field names and custom messages
            for field, errors in form.errors.items():
                field_name = form.fields[field].label if field in form.fields else field
                for error in errors:
                    messages.error(request, f"{field_name}: {error}")
    else:
        try:
            form = BlogForm(initial={
                'created_at': timezone.now()
            })
        except Exception as e:
            messages.error(request, f"Error initializing form: {str(e)}")
            form = BlogForm()
    
    # Safely create empty blog object
    class EmptyBlog:
        def __init__(self):
            self.id = None
            self.image = None
    
    context = {
        'form': form,
        'blog': EmptyBlog()
    }
    
    return render(request, 'app/create_blog.html', context)

def search_blogs(request):
    query = request.GET.get('q', '')
    if query:
        blogs = Blog.objects.filter(title__icontains=query)
    else:
        blogs = Blog.objects.all()
    return render(request, 'app/search_blogs.html', {'blogs': blogs, 'query': query})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully.")
            return redirect('home')
        else:
            messages.error(request, "Error in form submission.")
    else:
        form = ContactForm()
    return render(request, 'app/contact.html', {'form': form})

@ensure_csrf_cookie
def newsletter_view(request):
    form = NewsletterForm()
    return render(request, 'layout/base.html', {'form': form})

# views.py
@require_POST
@csrf_exempt
def subscribe_api(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        
        # Basic validation before form processing
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email address is required'
            }, status=400)

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid email address'
            }, status=400)

        form = NewsletterForm({'email': email})
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Thank you for subscribing!'
            })
        return JsonResponse({
            'success': False,
            'message': form.errors.get('email', ['Invalid submission'])[0]
        }, status=400)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request format'
        }, status=400)

def about(request):
    return render(request, 'app/about.html')

def privacy_policy(request):
    return render(request, 'app/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'app/terms_of_service .html')

def cookie_policy(request):
    return render(request, 'app/cookie_policy.html')
