from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Create groups and assign permissions for the bookshelf app'

    def handle(self, *args, **options):
        # Get the content type for the Book model
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get or create permissions
        can_view, created = Permission.objects.get_or_create(
            codename='can_view',
            name='Can view book',
            content_type=book_content_type,
        )
        
        can_create, created = Permission.objects.get_or_create(
            codename='can_create',
            name='Can create book',
            content_type=book_content_type,
        )
        
        can_edit, created = Permission.objects.get_or_create(
            codename='can_edit',
            name='Can edit book',
            content_type=book_content_type,
        )
        
        can_delete, created = Permission.objects.get_or_create(
            codename='can_delete',
            name='Can delete book',
            content_type=book_content_type,
        )
        
        # Create groups and assign permissions
        
        # Viewers group - Can only view books
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        viewers_group.permissions.add(can_view)
        
        # Editors group - Can view, create, and edit books
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editors_group.permissions.add(can_view, can_create, can_edit)
        
        # Admins group - Can do everything with books
        admins_group, created = Group.objects.get_or_create(name='Admins')
        admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created groups and permissions:')
        )
        self.stdout.write(f'- Viewers: can_view')
        self.stdout.write(f'- Editors: can_view, can_create, can_edit')
        self.stdout.write(f'- Admins: can_view, can_create, can_edit, can_delete')
        
        # Instructions for assigning users to groups
        self.stdout.write('\nTo assign users to groups, use the Django admin interface or:')
        self.stdout.write('python manage.py shell')
        self.stdout.write('>>> from django.contrib.auth.models import User, Group')
        self.stdout.write('>>> user = User.objects.get(username="username")')
        self.stdout.write('>>> group = Group.objects.get(name="Editors")')
        self.stdout.write('>>> user.groups.add(group)')
