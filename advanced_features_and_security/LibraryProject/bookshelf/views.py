from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .models import Book
from .forms import BookForm

# Function-based views with permission decorators

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books. Requires 'can_view' permission.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book. Requires 'can_create' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'title': 'Create Book'
    })

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to edit a book. Requires 'can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'title': 'Edit Book',
        'book': book
    })

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book. Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# Class-based views with permission mixins

class BookListView(PermissionRequiredMixin, ListView):
    """
    Class-based view to list books with permission checking.
    """
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view'
    raise_exception = True

class BookCreateView(PermissionRequiredMixin, CreateView):
    """
    Class-based view to create books with permission checking.
    """
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_create'
    raise_exception = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Book'
        return context

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Class-based view to update books with permission checking.
    """
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_edit'
    raise_exception = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Book'
        return context

class BookDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Class-based view to delete books with permission checking.
    """
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_delete'
    raise_exception = True

@login_required
def secure_view(request):
    """
    Example of a secure view that demonstrates input validation
    and CSRF protection. This view safely handles user input.
    """
    if request.method == 'POST':
        # Secure handling of user input - validate and sanitize
        search_query = request.POST.get('search', '').strip()
        
        if search_query:
            # Use Django ORM to prevent SQL injection
            # This is the secure way to handle database queries
            books = Book.objects.filter(
                title__icontains=search_query
            ).select_related()  # Use select_related for optimization
        else:
            books = Book.objects.none()
        
        return render(request, 'bookshelf/search_results.html', {
            'books': books,
            'query': search_query
        })
    
    return render(request, 'bookshelf/search_form.html')
