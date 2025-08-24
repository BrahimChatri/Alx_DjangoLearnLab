from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Search and Tag URLs
    path('search/', views.search_posts, name='search'),
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts_by_tag'),
    
    # Comment URLs - Class-based views
    path('post/<int:post_id>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    
    # Legacy function-based comment URLs (keeping for backward compatibility)
    path('post/<int:post_id>/comments/add/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_id>/edit_old/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete_old/', views.delete_comment, name='delete_comment'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog:home'), name='logout'),
    path('profile/', views.profile, name='profile'),
]
