from django.core.management.base import BaseCommand
from api.models import Book


class Command(BaseCommand):
    help = 'Populate the database with sample books'

    def handle(self, *args, **options):
        # Clear existing books
        Book.objects.all().delete()
        
        # Sample books data
        books = [
            {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
            {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
            {'title': '1984', 'author': 'George Orwell'},
            {'title': 'Pride and Prejudice', 'author': 'Jane Austen'},
            {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger'},
        ]
        
        # Create books
        for book_data in books:
            book = Book.objects.create(**book_data)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created book: {book.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated {len(books)} books')
        )
