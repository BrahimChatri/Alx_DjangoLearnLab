from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Book, CustomUser
import datetime

class BookForm(forms.ModelForm):
    """
    Form for creating and editing books with proper validation
    and security measures to prevent injection attacks.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': 200
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': 100
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year',
                'min': 1000,
                'max': datetime.datetime.now().year
            })
        }
    
    def clean_title(self):
        """Validate and sanitize book title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 2:
                raise forms.ValidationError("Title must be at least 2 characters long.")
        return title
    
    def clean_author(self):
        """Validate and sanitize author name"""
        author = self.cleaned_data.get('author')
        if author:
            author = author.strip()
            if len(author) < 2:
                raise forms.ValidationError("Author name must be at least 2 characters long.")
        return author
    
    def clean_publication_year(self):
        """Validate publication year"""
        year = self.cleaned_data.get('publication_year')
        current_year = datetime.datetime.now().year
        
        if year and (year < 1000 or year > current_year):
            raise forms.ValidationError(f"Publication year must be between 1000 and {current_year}.")
        return year

class CustomUserForm(forms.ModelForm):
    """
    Form for creating and editing custom users.
    """
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'profile_photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_date_of_birth(self):
        """Validate date of birth"""
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = datetime.date.today()
            if dob > today:
                raise forms.ValidationError("Date of birth cannot be in the future.")
            
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 13:
                raise forms.ValidationError("User must be at least 13 years old.")
        return dob

class SearchForm(forms.Form):
    """
    Secure search form with proper validation to prevent XSS and injection attacks.
    """
    search = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books by title...',
            'required': True
        })
    )
    
    def clean_search(self):
        """Validate and sanitize search input"""
        search = self.cleaned_data.get('search')
        if search:
            search = search.strip()
            if len(search) < 2:
                raise forms.ValidationError("Search query must be at least 2 characters long.")
            # Remove any potentially dangerous characters
            import re
            # Allow only alphanumeric characters, spaces, and basic punctuation
            if not re.match(r'^[A-Za-z0-9\s\.\-_,]+$', search):
                raise forms.ValidationError("Search query contains invalid characters.")
        return search
