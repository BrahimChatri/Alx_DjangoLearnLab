# Update Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
```

## Expected Output
```
# The command updates the title of the book from "1984" to "Nineteen Eighty-Four"
# The save() method commits the changes to the database
# No direct output, but the book instance is updated
```

## Verification
```python
print(f"Updated book title: {book.title}")
```

## Expected Output
```
# Updated book title: Nineteen Eighty-Four
```
