from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

class CustomUserCreationForm(UserCreationForm):
    """Extended UserCreationForm with email field"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name

class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts with django-taggit"""
    tags = forms.CharField(
        max_length=200,
        required=False,
        help_text='Enter tags separated by commas (e.g., django, python, web)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'django, python, web'
        })
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Pre-populate tags field with existing tags
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])
    
    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        if tags_str:
            # Clean and validate tags
            tag_names = [tag.strip().lower() for tag in tags_str.split(',') if tag.strip()]
            # Remove duplicates while preserving order
            seen = set()
            unique_tags = []
            for tag in tag_names:
                if tag not in seen:
                    seen.add(tag)
                    unique_tags.append(tag)
            return unique_tags
        return []
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            # Set tags using django-taggit
            post.tags.clear()
            tag_names = self.cleaned_data.get('tags', [])
            if tag_names:
                post.tags.add(*tag_names)
        return post

class CommentForm(forms.ModelForm):
    """Form for creating and editing comments with validation"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...',
                'minlength': '10',
                'maxlength': '1000'
            }),
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Comment content is required.')
        
        if len(content.strip()) < 10:
            raise forms.ValidationError('Comment must be at least 10 characters long.')
        
        if len(content) > 1000:
            raise forms.ValidationError('Comment cannot exceed 1000 characters.')
        
        return content.strip()
