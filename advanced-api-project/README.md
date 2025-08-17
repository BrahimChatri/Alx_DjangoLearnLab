# Advanced Django REST Framework API Project

This project demonstrates advanced Django REST Framework features including filtering, searching, ordering, and proper permission management.

## Features

### 1. Book Management API
- **CRUD Operations**: Create, Read, Update, and Delete books
- **Authentication Required**: Protected endpoints for create, update, and delete operations
- **Public Read Access**: List and detail views are publicly accessible

### 2. Advanced Filtering & Search
- **Django Filter Backend**: Filter books by title, author name, and publication year
- **Search Functionality**: Search across book titles and author names
- **Ordering**: Sort books by title and publication year (ascending/descending)

### 3. Permission Classes
- **IsAuthenticatedOrReadOnly**: For list and detail views
- **IsAuthenticated**: For create, update, and delete operations

### 4. Test Database Configuration
- **Separate Test Database**: Configured to avoid impacting production/development data
- **Comprehensive Test Coverage**: Tests for all endpoints and permission scenarios

## API Endpoints

| Endpoint | Method | Permission | Description |
|----------|--------|------------|-------------|
| `/api/books/` | GET | Public | List all books with filtering, search, and ordering |
| `/api/books/<id>/` | GET | Public | Get book details |
| `/api/books/create/` | POST | Authenticated | Create a new book |
| `/api/books/update/` | PUT | Authenticated | Update an existing book (requires book ID in body) |
| `/api/books/delete/` | DELETE | Authenticated | Delete a book (requires book ID in body) |

## Query Parameters

### Filtering
- `?title=BookName` - Filter by book title
- `?author__name=AuthorName` - Filter by author name
- `?publication_year=2020` - Filter by publication year

### Searching
- `?search=keyword` - Search in book titles and author names

### Ordering
- `?ordering=title` - Order by title (ascending)
- `?ordering=-title` - Order by title (descending)
- `?ordering=publication_year` - Order by publication year (ascending)
- `?ordering=-publication_year` - Order by publication year (descending)

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

3. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Run Tests**
   ```bash
   python manage.py test
   ```

## Project Structure

```
advanced-api-project/
├── advanced_api_project/     # Main project settings
│   ├── settings.py          # Django settings with REST framework config
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── api/                      # API application
│   ├── models.py            # Book and Author models
│   ├── serializers.py       # DRF serializers with validation
│   ├── views.py             # API views with filtering and permissions
│   ├── urls.py              # API URL patterns
│   ├── admin.py             # Django admin configuration
│   ├── tests.py             # Original test suite
│   └── test_views.py        # Comprehensive unit tests for API endpoints
├── requirements.txt          # Python dependencies
└── manage.py                # Django management script
```

## Dependencies

- **Django 4.2.7**: Web framework
- **Django REST Framework 3.14.0**: API framework
- **Django Filter 23.3**: Advanced filtering capabilities
- **Pillow 10.0.1**: Image processing (if needed)

## Testing

The project includes comprehensive tests covering:
- **test_views.py**: 24 comprehensive unit tests for API endpoints (as required by the task)
- **tests.py**: 15 additional tests for extended functionality
- **Total**: 39 tests covering all aspects of the API

### Test Coverage Includes:
- Authentication and permission checks
- CRUD operations (Create, Read, Update, Delete)
- Filtering, searching, and ordering functionality
- Error handling for invalid requests
- Proper HTTP status codes
- Response data integrity validation
- Edge cases and error scenarios
- Login functionality testing
- Comprehensive filtering capabilities
- Advanced search functionality
- Ordering functionality for multiple fields

### Running Tests:
```bash
# Run all tests
python manage.py test

# Run only the comprehensive API tests
python manage.py test api.test_views

# Run original test suite
python manage.py test api.tests
```

All tests use a separate test database to avoid impacting production data.

## Security Features

- **Authentication Required**: Protected endpoints require user authentication
- **Permission Classes**: Proper role-based access control
- **Input Validation**: Serializer validation for data integrity
- **CSRF Protection**: Enabled by default in Django

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request
