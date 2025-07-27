# Delete Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
```

## Expected Output
```
# The command deletes the book from the database
# Returns: (1, {'bookshelf.Book': 1})
# The tuple indicates (number of objects deleted, dictionary of deletions by model)
```

## Verification
```python
books = Book.objects.all()
print(f"All books after deletion: {books}")
```

## Expected Output
```
# All books after deletion: <QuerySet []>
# This confirms that the book has been successfully deleted
```
