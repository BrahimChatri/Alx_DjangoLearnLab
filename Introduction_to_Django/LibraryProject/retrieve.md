# Retrieve Operation

## Command
```python
book = Book.objects.get(title="1984")
```

## Expected Output
```
# The command retrieves the book with title "1984"
# Returns: <Book: 1984>
```

## Display all attributes
```python
print(f"Book title: {book.title}")
print(f"Book author: {book.author}")
print(f"Book publication year: {book.publication_year}")
```

## Expected Output
```
# Book title: 1984
# Book author: George Orwell
# Book publication year: 1949
```
