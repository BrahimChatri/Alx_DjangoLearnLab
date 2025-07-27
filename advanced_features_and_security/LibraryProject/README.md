## Permissions and Security Configuration

### Custom User Model
- Custom user model with additional fields (date_of_birth, profile_photo) implemented and registered in admin.

### Permissions
- Implemented custom permissions for Book model (can_view, can_create, can_edit, can_delete).
- Views protected using @permission_required decorators and PermissionRequiredMixin.

### Security Best Practices
- Set SECURE_CONTENT_TYPE_NOSNIFF, SECURE_BROWSER_XSS_FILTER, X_FRAME_OPTIONS in settings for added security.
- Updated forms and views to use CSRF tokens and prevent SQL injections.

### Testing
- Manually tested with different user roles to ensure proper access control.

### Deployment
- Ensure SSL certificates are configured in the server for HTTPS support.
- Set SECURE_SSL_REDIRECT, SECURE_HSTS_SECONDS, and other security configurations as per production needs.

