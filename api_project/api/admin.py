from django.contrib import admin
from .models import Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at', 'updated_at']
    list_filter = ['author', 'created_at']
    search_fields = ['title', 'author']
    readonly_fields = ['created_at', 'updated_at']
