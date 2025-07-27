# CRUD Operations for Book Model

This document contains all CRUD operations performed on the Book model through Django shell.

## Create Operation
```python
# Create a Book instance
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Created book: {book}")
# Output: Created book: 1984
```

## Retrieve Operation
```python
# Retrieve all books
books = Book.objects.all()
print(f"All books: {books}")
# Output: All books: <QuerySet [<Book: 1984>]>

# Retrieve specific book
book = Book.objects.get(title="1984")
print(f"Book title: {book.title}")
print(f"Book author: {book.author}")
print(f"Book publication year: {book.publication_year}")
# Output: 
# Book title: 1984
# Book author: George Orwell
# Book publication year: 1949
```

## Update Operation
```python
# Update book title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated book title: {book.title}")
# Output: Updated book title: Nineteen Eighty-Four
```

## Delete Operation
```python
# Delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")

# Verify deletion
books = Book.objects.all()
print(f"All books after deletion: {books}")
# Output: 
# Book deleted successfully
# All books after deletion: <QuerySet []>
```
