import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """Query all books by a specific author"""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return []


def list_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return []


def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


# Sample usage
if __name__ == "__main__":
    # Example queries
    print("=== Query Books by Author ===")
    books = query_books_by_author("J.K. Rowling")
    for book in books:
        print(f"- {book.title}")
    
    print("\n=== List Books in Library ===")
    books = list_books_in_library("Central Library")
    for book in books:
        print(f"- {book.title} by {book.author.name}")
    
    print("\n=== Get Librarian for Library ===")
    librarian = get_librarian_for_library("Central Library")
    if librarian:
        print(f"Librarian: {librarian.name}")
    else:
        print("No librarian found for this library")
