from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.db.models import Q
from taggit.models import Tag
from .models import Post, Comment
from .forms import CustomUserCreationForm, UserProfileForm, PostForm, CommentForm

# Create your views here.

def home(request):
    """Home view that displays the latest posts"""
    posts = Post.objects.all()[:6]  # Get latest 6 posts
    context = {
        'posts': posts,
    }
    return render(request, 'home.html', context)

class PostListView(ListView):
    """View for listing all blog posts"""
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

def search_posts(request):
    """View for searching blog posts"""
    query = request.GET.get('q', '')
    posts = []
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-published_date')
    
    context = {
        'posts': posts,
        'query': query,
        'results_count': posts.count()
    }
    return render(request, 'search_results.html', context)

def posts_by_tag(request, tag_name):
    """View for displaying posts by tag"""
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag).order_by('-published_date')
    
    context = {
        'tag': tag,
        'posts': posts,
        'results_count': posts.count()
    }
    return render(request, 'posts_by_tag.html', context)

class PostDetailView(DetailView):
    """View for displaying individual blog posts"""
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """View for creating new blog posts"""
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('blog:home')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating blog posts"""
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting blog posts"""
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('blog:home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)

class CommentCreateView(LoginRequiredMixin, CreateView):
    """View for creating new comments"""
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs['post_id']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return context

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating comments"""
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object
        context['post'] = self.object.post
        return context

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting comments"""
    model = Comment
    template_name = 'comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def add_comment(request, post_id):
    """View for adding comments to blog posts"""
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('blog:post_detail', pk=post_id)
    else:
        form = CommentForm()
    
    return redirect('blog:post_detail', pk=post_id)

@login_required
def edit_comment(request, comment_id):
    """View for editing comments"""
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Check if user is the author of the comment
    if comment.author != request.user:
        messages.error(request, 'You can only edit your own comments.')
        return redirect('blog:post_detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('blog:post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'comment_form.html', {
        'form': form,
        'comment': comment,
        'post': comment.post
    })

@login_required
def delete_comment(request, comment_id):
    """View for deleting comments"""
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Check if user is the author of the comment
    if comment.author != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('blog:post_detail', pk=comment.post.pk)
    
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('blog:post_detail', pk=post_pk)

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Django Blog!')
            return redirect('blog:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('blog:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    
    context = {
        'form': form,
        'user_posts': user_posts,
    }
    return render(request, 'registration/profile.html', context)
