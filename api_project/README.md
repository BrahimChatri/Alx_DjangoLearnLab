# Django REST Framework API Project

A comprehensive Django REST Framework API project implementing CRUD operations for a Book management system with authentication and permissions.

## Features

- **Django REST Framework API**: Full CRUD operations for Book model
- **Token Authentication**: Secure API access using token-based authentication
- **Multiple Endpoints**: 
  - Simple list view for public access
  - Full ViewSet with authentication for CRUD operations
- **Admin Interface**: Django admin panel for book management
- **Sample Data**: Management command to populate sample books

## Project Structure

```
api_project/
├── api/                          # Main API application
│   ├── management/
│   │   └── commands/
│   │       └── populate_books.py # Sample data population command
│   ├── migrations/               # Database migrations
│   ├── admin.py                  # Admin interface configuration
│   ├── models.py                 # Book model definition
│   ├── serializers.py           # DRF serializers
│   ├── urls.py                   # API URL patterns
│   └── views.py                  # API views and viewsets
├── api_project/                  # Django project settings
│   ├── settings.py              # Project configuration
│   ├── urls.py                  # Main URL configuration
│   └── ...
├── manage.py                     # Django management script
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd api_project
   ```

2. **Install dependencies**:
   ```bash
   pip install django djangorestframework
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Populate sample data**:
   ```bash
   python manage.py populate_books
   ```

6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Public Endpoints

- **GET** `/api/books/` - List all books (no authentication required)

### Authenticated Endpoints (Require Token)

- **GET** `/api/books_all/` - List all books
- **POST** `/api/books_all/` - Create a new book
- **GET** `/api/books_all/{id}/` - Retrieve a specific book
- **PUT** `/api/books_all/{id}/` - Update a specific book
- **DELETE** `/api/books_all/{id}/` - Delete a specific book

### Authentication

- **POST** `/api-token-auth/` - Obtain authentication token

## Usage Examples

### 1. Get Authentication Token

```bash
curl -X POST http://127.0.0.1:8000/api-token-auth/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
```

Response:
```json
{"token": "your_auth_token_here"}
```

### 2. List Books (Public)

```bash
curl http://127.0.0.1:8000/api/books/
```

### 3. List Books (Authenticated)

```bash
curl -H "Authorization: Token your_auth_token_here" \
     http://127.0.0.1:8000/api/books_all/
```

### 4. Create a New Book

```bash
curl -X POST http://127.0.0.1:8000/api/books_all/ \
     -H "Authorization: Token your_auth_token_here" \
     -H "Content-Type: application/json" \
     -d '{"title": "New Book", "author": "Author Name"}'
```

### 5. Update a Book

```bash
curl -X PUT http://127.0.0.1:8000/api/books_all/1/ \
     -H "Authorization: Token your_auth_token_here" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Title", "author": "Updated Author"}'
```

### 6. Delete a Book

```bash
curl -X DELETE http://127.0.0.1:8000/api/books_all/1/ \
     -H "Authorization: Token your_auth_token_here"
```

## Book Model

The Book model includes the following fields:

- `id` (Integer): Primary key (auto-generated)
- `title` (CharField): Book title (max 200 characters)
- `author` (CharField): Author name (max 100 characters)
- `created_at` (DateTimeField): Timestamp when book was created
- `updated_at` (DateTimeField): Timestamp when book was last updated

## Authentication & Permissions

- **Authentication**: Token-based authentication using Django REST Framework's TokenAuthentication
- **Permissions**: 
  - Public list endpoint: No authentication required
  - CRUD endpoints: Authentication required (IsAuthenticated permission)
- **Token Management**: Tokens are automatically created for users and can be obtained via the `/api-token-auth/` endpoint

## Admin Interface

Access the Django admin interface at `/admin/` to manage books and users through a web interface.

## Testing

The project includes comprehensive testing of all CRUD operations:

1. **List Operations**: Both public and authenticated listing
2. **Create Operations**: Creating new books with authentication
3. **Read Operations**: Retrieving individual books
4. **Update Operations**: Modifying existing books
5. **Delete Operations**: Removing books from the database

## Development Notes

- Uses SQLite database for development (configurable)
- Includes proper error handling and validation
- Follows Django REST Framework best practices
- Implements proper HTTP status codes for all operations
- Includes pagination support (can be configured in settings)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is created for educational purposes as part of the ALX Django Learning Lab curriculum.
