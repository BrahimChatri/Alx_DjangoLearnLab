# Create Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

## Expected Output
```
# The command creates a new Book instance with the specified attributes
# The book is automatically saved to the database
# Returns: <Book: 1984>
```

## Verification
```python
print(f"Created book: {book}")
# Output: Created book: 1984
```
