from django.urls import path
from . import views

urlpatterns = [
    # Function-based views
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Class-based views (alternative URLs)
    path('books-cbv/', views.BookListView.as_view(), name='book_list_cbv'),
    path('books-cbv/create/', views.BookCreateView.as_view(), name='book_create_cbv'),
    path('books-cbv/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit_cbv'),
    path('books-cbv/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete_cbv'),
    
    # Secure search functionality
    path('search/', views.secure_view, name='search_form'),
]
