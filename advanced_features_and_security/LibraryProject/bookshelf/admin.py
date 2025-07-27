from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book

# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for the custom user model.
    Extends the default UserAdmin to include additional fields.
    """
    # Display these fields in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    
    # Add search functionality
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Add filtering options
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Configure the user edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    # Configure the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )

# Book Admin with permissions support
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for the Book model with custom permissions.
    """
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')
    
    # Define which permissions are required for different actions
    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('bookshelf.can_view')
    
    def has_add_permission(self, request):
        return request.user.has_perm('bookshelf.can_create')
    
    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('bookshelf.can_edit')
    
    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('bookshelf.can_delete')
