from django.http import HttpResponseNotFound
from django.urls import path
from .views import *
from .views import *

urlpatterns = [
    path('', Home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('profile/', profile, name='profile'), 
    path('profile/update/', profile_update, name='profile_update'),  
    path('profile/<str:username>/', profile, name='user_profile'), 

    path('blogs/', blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('blogs/<int:blog_id>/edit/', edit_blog, name='edit_blog'),
    path('blogs/create/', create_blog, name='create_blog'),
    path('my_blogs/', my_blogs, name='my_blogs'),
    path('blogs/<int:blog_id>/like/', like_blog, name='like_blog'),
    path('blogs/<int:blog_id>/comment/', comment, name='add_comment'),
    path('blogs/<int:blog_id>/delete/', delete_blog, name='delete_blog'),
    path('blogs/search/', search_blogs, name='search_blogs'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),

    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('privacy/', privacy_policy, name='privacy'),
    path('terms/', terms_of_service, name='terms'),
    path('cookie_policy/', cookie_policy, name="cookie_policy"),

    path('newsletter/', newsletter_view, name='newsletter'),
    path('subscribe/', subscribe_api, name='subscribe_api'),

]
