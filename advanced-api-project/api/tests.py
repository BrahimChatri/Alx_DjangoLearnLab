from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book
from django.contrib.auth.models import User
from django.test.utils import override_settings

@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.author = Author.objects.create(name="Author1")
        self.book = Book.objects.create(title="Book1", publication_year=2020, author=self.author)
        self.book2 = Book.objects.create(title="Book2", publication_year=2021, author=self.author)

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {"title": "Book3", "publication_year": 2022, "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {"title": "Book3", "publication_year": 2022, "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update')
        data = {"id": self.book.id, "title": "Updated Book1", "publication_year": 2023}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Book1")

    def test_update_book_unauthenticated(self):
        url = reverse('book-update')
        data = {"id": self.book.id, "title": "Updated Book1"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_missing_id(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update')
        data = {"title": "Updated Book1"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete')
        data = {"id": self.book.id}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_book_unauthenticated(self):
        url = reverse('book-delete')
        data = {"id": self.book.id}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_missing_id(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete')
        data = {}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_books_by_title(self):
        url = reverse('book-list') + '?title=Book1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_books_by_publication_year(self):
        url = reverse('book-list') + '?publication_year=2020'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        url = reverse('book-list') + '?search=Book'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_ordering_books_by_title(self):
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Book1")

    def test_ordering_books_by_publication_year_desc(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2021)

    def test_book_detail_view(self):
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Book1")
