# Django Blog Project

A comprehensive Django blog application with advanced features including CRUD operations, commenting system, tagging functionality, search capabilities, and user authentication.

## Features Implemented

### ✅ **CRUD Operations for Comments**
- **CommentCreateView**: Class-based view for creating new comments
- **CommentUpdateView**: Class-based view for updating comments with UserPassesTestMixin
- **CommentDeleteView**: Class-based view for deleting comments with UserPassesTestMixin
- **CommentForm**: ModelForm with validation rules (10-1000 characters)

### ✅ **URL Structure**
- **Post URLs**: `/post/new/`, `/post/<int:pk>/update/`, `/post/<int:pk>/delete/`
- **Comment URLs**: `/post/<int:post_id>/comments/new/`, `/comments/<int:pk>/edit/`, `/comments/<int:pk>/delete/`
- **Logical and intuitive URL patterns** as required

### ✅ **Templates**
- **Post Templates**: `post_list.html`, `post_detail.html`, `post_form.html`, `post_confirm_delete.html`
- **Comment Templates**: `comment_form.html`, `comment_confirm_delete.html`
- **User Templates**: Registration, login, profile templates
- **Search and Tag Templates**: `search_results.html`, `posts_by_tag.html`

### ✅ **Authentication & Authorization**
- **LoginRequiredMixin**: Applied to all create, update, and delete views
- **UserPassesTestMixin**: Ensures only post/comment authors can edit/delete their content
- **Custom User Registration**: Extended UserCreationForm with email field
- **User Profile Management**: Profile update functionality

### ✅ **Tagging Functionality**
- **django-taggit Integration**: Added to INSTALLED_APPS in settings.py
- **Post Tagging**: Posts can be tagged with multiple tags
- **Tag-based Filtering**: View posts by specific tags
- **Tag Search**: Search functionality includes tag names

### ✅ **Search Functionality**
- **Multi-field Search**: Search across title, content, and tags
- **Case-insensitive Search**: Uses `icontains` for flexible matching
- **Search Results Page**: Dedicated template for search results
- **Result Count Display**: Shows number of search results

### ✅ **Form Validation**
- **CommentForm Validation**: 
  - Minimum 10 characters
  - Maximum 1000 characters
  - Required field validation
- **PostForm Validation**: 
  - Tag validation and cleaning
  - Duplicate tag removal
  - Case normalization

## Project Structure

```
django_blog/
├── django_blog/          # Main project settings
│   ├── settings.py      # Django settings with taggit
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── blog/                 # Blog application
│   ├── models.py        # Post and Comment models with taggit
│   ├── views.py         # Class-based views with mixins
│   ├── forms.py         # Forms with validation
│   ├── urls.py          # URL patterns
│   ├── admin.py         # Admin configuration
│   └── migrations/      # Database migrations
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── post_*.html      # Post-related templates
│   ├── comment_*.html   # Comment-related templates
│   └── registration/    # Auth templates
├── static/              # Static files
├── requirements.txt     # Dependencies
└── manage.py           # Django management script
```

## Models

### Post Model
- `title`: CharField (max_length=200)
- `content`: TextField
- `published_date`: DateTimeField (auto_now_add=True)
- `author`: ForeignKey to User
- `tags`: TaggableManager (django-taggit)

### Comment Model
- `post`: ForeignKey to Post
- `author`: ForeignKey to User
- `content`: TextField (with validation)
- `created_at`: DateTimeField (auto_now_add=True)
- `updated_at`: DateTimeField (auto_now=True)

## Views

### Class-Based Views
- **PostListView**: List all posts with pagination
- **PostDetailView**: Display individual post with comments
- **PostCreateView**: Create new posts (LoginRequiredMixin)
- **PostUpdateView**: Update posts (LoginRequiredMixin + UserPassesTestMixin)
- **PostDeleteView**: Delete posts (LoginRequiredMixin + UserPassesTestMixin)
- **CommentCreateView**: Create new comments (LoginRequiredMixin)
- **CommentUpdateView**: Update comments (LoginRequiredMixin + UserPassesTestMixin)
- **CommentDeleteView**: Delete comments (LoginRequiredMixin + UserPassesTestMixin)

### Function-Based Views
- **home**: Display latest posts
- **search_posts**: Search functionality
- **posts_by_tag**: Filter posts by tag
- **register**: User registration
- **profile**: User profile management

## Forms

### PostForm
- Title and content fields
- Tag field with comma-separated input
- Automatic tag creation and validation
- Bootstrap styling

### CommentForm
- Content field with validation
- Minimum 10, maximum 1000 characters
- Bootstrap styling

### CustomUserCreationForm
- Extended UserCreationForm with email
- Custom validation and styling

## URL Patterns

### Post URLs
- `post/new/` → PostCreateView
- `post/<int:pk>/` → PostDetailView
- `post/<int:pk>/update/` → PostUpdateView
- `post/<int:pk>/delete/` → PostDeleteView

### Comment URLs
- `post/<int:post_id>/comments/new/` → CommentCreateView
- `comments/<int:pk>/edit/` → CommentUpdateView
- `comments/<int:pk>/delete/` → CommentDeleteView

### Search and Tag URLs
- `search/` → search_posts
- `tags/<str:tag_name>/` → posts_by_tag

### Authentication URLs
- `register/` → register
- `login/` → LoginView
- `logout/` → LogoutView
- `profile/` → profile

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Access the Application**
   - Home: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - Posts: http://localhost:8000/posts/

## Dependencies

- **Django 4.2.7**: Web framework
- **django-taggit 4.0.0**: Tagging functionality
- **Pillow 10.0.1**: Image processing

## Security Features

- **Authentication Required**: Protected endpoints require login
- **Author-only Access**: Only post/comment authors can edit/delete
- **CSRF Protection**: Enabled by default
- **Input Validation**: Comprehensive form validation
- **SQL Injection Protection**: Django ORM protection

## Testing

The project includes comprehensive functionality testing:
- CRUD operations for posts and comments
- Authentication and authorization
- Search and filtering capabilities
- Form validation
- URL routing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
