from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book
from django.contrib.auth.models import User
from django.test.utils import override_settings

@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class BookAPITests(APITestCase):
    """
    Comprehensive unit tests for Book API endpoints.
    Tests functionality, response data integrity, and status code accuracy.
    """
    
    def setUp(self):
        """Set up test data for each test method."""
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.author = Author.objects.create(name="Author1")
        self.book = Book.objects.create(title="Book1", publication_year=2020, author=self.author)
        self.book2 = Book.objects.create(title="Book2", publication_year=2021, author=self.author)

    def test_list_books_success(self):
        """Test successful retrieval of book list."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data integrity
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], "Book1")
        self.assertEqual(response.data[1]['title'], "Book2")

    def test_create_book_authenticated_success(self):
        """Test successful book creation by authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {"title": "Book3", "publication_year": 2022, "author": self.author.id}
        
        response = self.client.post(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check response data integrity
        self.assertEqual(response.data['title'], "Book3")
        self.assertEqual(response.data['publication_year'], 2022)
        self.assertEqual(response.data['author'], self.author.id)

    def test_create_book_unauthenticated_forbidden(self):
        """Test book creation is forbidden for unauthenticated users."""
        url = reverse('book-create')
        data = {"title": "Book3", "publication_year": 2022, "author": self.author.id}
        
        response = self.client.post(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated_success(self):
        """Test successful book update by authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update')
        data = {"id": self.book.id, "title": "Updated Book1", "publication_year": 2023}
        
        response = self.client.put(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data integrity
        self.assertEqual(response.data['title'], "Updated Book1")
        self.assertEqual(response.data['publication_year'], 2023)

    def test_update_book_unauthenticated_forbidden(self):
        """Test book update is forbidden for unauthenticated users."""
        url = reverse('book-update')
        data = {"id": self.book.id, "title": "Updated Book1"}
        
        response = self.client.put(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_missing_id_bad_request(self):
        """Test book update fails when book ID is missing."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update')
        data = {"title": "Updated Book1"}
        
        response = self.client.put(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check response data integrity
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Book ID is required")

    def test_update_book_not_found(self):
        """Test book update fails when book doesn't exist."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update')
        data = {"id": 99999, "title": "Updated Book"}
        
        response = self.client.put(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Check response data integrity
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Book not found")

    def test_delete_book_authenticated_success(self):
        """Test successful book deletion by authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete')
        data = {"id": self.book.id}
        
        response = self.client.delete(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify book was actually deleted
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_book_unauthenticated_forbidden(self):
        """Test book deletion is forbidden for unauthenticated users."""
        url = reverse('book-delete')
        data = {"id": self.book.id}
        
        response = self.client.delete(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_missing_id_bad_request(self):
        """Test book deletion fails when book ID is missing."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete')
        data = {}
        
        response = self.client.delete(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check response data integrity
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Book ID is required")

    def test_delete_book_not_found(self):
        """Test book deletion fails when book doesn't exist."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete')
        data = {"id": 99999}
        
        response = self.client.delete(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Check response data integrity
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Book not found")

    def test_filter_books_by_title(self):
        """Test filtering books by title."""
        url = reverse('book-list') + '?title=Book1'
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data integrity
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Book1")

    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication year."""
        url = reverse('book-list') + '?publication_year=2020'
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data integrity
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2020)

    def test_search_books_by_title(self):
        """Test searching books by title."""
        url = reverse('book-list') + '?search=Book'
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data integrity
        self.assertEqual(len(response.data), 2)

    def test_ordering_books_by_title_ascending(self):
        """Test ordering books by title in ascending order."""
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data integrity
        self.assertEqual(response.data[0]['title'], "Book1")
        self.assertEqual(response.data[1]['title'], "Book2")

    def test_ordering_books_by_publication_year_descending(self):
        """Test ordering books by publication year in descending order."""
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data integrity
        self.assertEqual(response.data[0]['publication_year'], 2021)
        self.assertEqual(response.data[1]['publication_year'], 2020)

    def test_book_detail_view_success(self):
        """Test successful retrieval of book details."""
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data integrity
        self.assertEqual(response.data['title'], "Book1")
        self.assertEqual(response.data['publication_year'], 2020)
        self.assertEqual(response.data['author'], self.author.id)

    def test_book_detail_view_not_found(self):
        """Test book detail view returns 404 for non-existent book."""
        url = reverse('book-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_book_invalid_data_bad_request(self):
        """Test book creation fails with invalid data."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {"title": "", "publication_year": "invalid_year", "author": self.author.id}
        
        response = self.client.post(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_future_publication_year_bad_request(self):
        """Test book creation fails with future publication year."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {"title": "Future Book", "publication_year": 2030, "author": self.author.id}
        
        response = self.client.post(url, data)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_functionality(self):
        """Test login functionality using self.client.login."""
        # Test login with correct credentials
        login_success = self.client.login(username="testuser", password="pass123")
        self.assertTrue(login_success)
        
        # Test login with incorrect credentials
        login_failure = self.client.login(username="testuser", password="wrongpassword")
        self.assertFalse(login_failure)
        
        # Test that we can access protected endpoints after login
        url = reverse('book-create')
        data = {"title": "Book via Login", "publication_year": 2022, "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filtering_capabilities_comprehensive(self):
        """Test comprehensive filtering capabilities for various attributes."""
        # Test filtering by title
        url = reverse('book-list') + '?title=Book1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Book1")
        
        # Test filtering by publication year
        url = reverse('book-list') + '?publication_year=2021'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2021)
        
        # Test filtering by author name
        url = reverse('book-list') + '?author__name=Author1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_functionality_comprehensive(self):
        """Test comprehensive search functionality across multiple fields."""
        # Test search in title field
        url = reverse('book-list') + '?search=Book'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Test search in author name field
        url = reverse('book-list') + '?search=Author1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Test search with partial match
        url = reverse('book-list') + '?search=Book1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_ordering_functionality_comprehensive(self):
        """Test comprehensive ordering functionality for various fields."""
        # Test ordering by title ascending
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Book1")
        self.assertEqual(response.data[1]['title'], "Book2")
        
        # Test ordering by title descending
        url = reverse('book-list') + '?ordering=-title'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Book2")
        self.assertEqual(response.data[1]['title'], "Book1")
        
        # Test ordering by publication year ascending
        url = reverse('book-list') + '?ordering=publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2020)
        self.assertEqual(response.data[1]['publication_year'], 2021)
        
        # Test ordering by publication year descending
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2021)
        self.assertEqual(response.data[1]['publication_year'], 2020)
