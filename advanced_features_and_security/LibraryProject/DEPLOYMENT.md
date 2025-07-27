# Deployment Guide for LibraryProject

## HTTPS Configuration and Security Implementation

This guide covers the deployment of the LibraryProject with HTTPS support and security best practices.

### Prerequisites

1. SSL/TLS Certificate (from Let's Encrypt, commercial CA, or self-signed for testing)
2. Web server (Nginx or Apache)
3. Domain name (for production)

### Security Features Implemented

#### 1. Custom User Model
- Extended Django's AbstractUser with additional fields:
  - `date_of_birth`: DateField for user's birth date
  - `profile_photo`: ImageField for user profile pictures
- Custom user manager for proper user creation

#### 2. Permissions and Groups System
- Custom permissions for Book model:
  - `can_view`: Permission to view books
  - `can_create`: Permission to create books
  - `can_edit`: Permission to edit books
  - `can_delete`: Permission to delete books

- User groups with assigned permissions:
  - **Viewers**: can_view
  - **Editors**: can_view, can_create, can_edit
  - **Admins**: can_view, can_create, can_edit, can_delete

#### 3. Security Headers and Settings
- `SECURE_CONTENT_TYPE_NOSNIFF`: Prevents MIME type sniffing
- `SECURE_BROWSER_XSS_FILTER`: Enables browser XSS protection
- `X_FRAME_OPTIONS`: Set to 'DENY' to prevent clickjacking
- CSRF protection enabled on all forms
- Secure cookie settings for HTTPS

#### 4. HTTPS Configuration
For production, the following settings are configured in `settings_production.py`:

```python
# Redirect HTTP to HTTPS
SECURE_SSL_REDIRECT = True

# HSTS Headers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/your/certificate.pem;
    ssl_certificate_key /path/to/your/private.key;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-Frame-Options DENY always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/media/;
    }
}
```

### Apache Configuration Example

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    SSLEngine on
    SSLCertificateFile /path/to/your/certificate.pem
    SSLCertificateKeyFile /path/to/your/private.key
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
    
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    ProxyPreserveHost On
    
    Alias /static/ /path/to/your/staticfiles/
    Alias /media/ /path/to/your/media/
</VirtualHost>
```

### Deployment Steps

1. **Prepare the server:**
   ```bash
   # Install required packages
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

2. **Set up the application:**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd advanced_features_and_security/LibraryProject
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install django pillow
   ```

3. **Configure Django for production:**
   ```bash
   # Set environment variable for production settings
   export DJANGO_SETTINGS_MODULE=LibraryProject.settings_production
   
   # Run migrations
   python manage.py makemigrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   
   # Set up groups and permissions
   python manage.py setup_groups
   
   # Collect static files
   python manage.py collectstatic
   ```

4. **Set up SSL certificate:**
   ```bash
   # For Let's Encrypt (recommended)
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

5. **Configure and start services:**
   ```bash
   # Configure Nginx (use the example above)
   sudo nano /etc/nginx/sites-available/libraryproject
   sudo ln -s /etc/nginx/sites-available/libraryproject /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   
   # Start Django application (consider using Gunicorn for production)
   python manage.py runserver 127.0.0.1:8000
   ```

### Security Testing

1. **Test HTTPS redirection:**
   ```bash
   curl -I http://yourdomain.com
   # Should return 301 redirect to HTTPS
   ```

2. **Test security headers:**
   ```bash
   curl -I https://yourdomain.com
   # Should include HSTS, X-Content-Type-Options, X-Frame-Options headers
   ```

3. **Test permissions:**
   - Create test users and assign them to different groups
   - Verify that users can only access allowed functionality
   - Test CSRF protection on forms

### Production Checklist

- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured
- [ ] SSL certificate installed and configured
- [ ] HTTPS redirection working
- [ ] Security headers present
- [ ] CSRF protection enabled
- [ ] User permissions properly configured
- [ ] Database properly secured
- [ ] Static files served efficiently
- [ ] Error logging configured
- [ ] Regular security updates scheduled

### Monitoring and Maintenance

1. **SSL Certificate Renewal:**
   ```bash
   # For Let's Encrypt certificates
   sudo certbot renew --dry-run
   ```

2. **Security Updates:**
   - Regularly update Django and dependencies
   - Monitor security advisories
   - Review access logs regularly

3. **Backup Strategy:**
   - Regular database backups
   - Media files backup
   - Application code versioning
