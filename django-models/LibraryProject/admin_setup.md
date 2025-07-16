# Django Admin Interface Setup

## Overview
This document describes the setup and configuration of the Django admin interface for the Book model in the bookshelf app.

## Admin Configuration

### BookAdmin Class
The `BookAdmin` class in `bookshelf/admin.py` provides custom configurations for the Book model:

```python
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')
```

### Features Implemented

1. **List Display**: Shows title, author, and publication year in the admin list view
2. **List Filters**: Provides filter options by author and publication year
3. **Search Fields**: Enables searching by title and author

### Access the Admin Interface

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Access admin interface**:
   - URL: http://127.0.0.1:8000/admin/
   - Username: admin
   - Password: admin123

3. **Manage Books**:
   - View all books in a table format
   - Add new books using the admin form
   - Edit existing books
   - Delete books
   - Use filters to narrow down results
   - Search for specific books

## Benefits

- **User-friendly interface**: Easy to manage book data without writing code
- **Filtering capabilities**: Quick access to books by author or publication year
- **Search functionality**: Find books by title or author
- **CRUD operations**: Complete Create, Read, Update, Delete functionality
- **Data validation**: Automatic form validation based on model constraints
