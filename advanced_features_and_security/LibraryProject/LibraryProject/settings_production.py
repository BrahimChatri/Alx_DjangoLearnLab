"""
Production settings for LibraryProject.
This file contains security configurations for production deployment with HTTPS.
"""

from .settings import *

# Security Settings for Production
DEBUG = False

# Add your production domain here
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'localhost']

# HTTPS Security Configuration
# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security (HSTS)
# Instructs browsers to only access the site via HTTPS for 1 year
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure Cookies - Only send cookies over HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Prevent browsers from MIME-sniffing a response away from the declared content-type
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enable the browser's XSS filtering and help prevent XSS attacks
SECURE_BROWSER_XSS_FILTER = True

# Prevent the site from being framed (clickjacking protection)
X_FRAME_OPTIONS = 'DENY'

# Additional Security Headers
SECURE_REFERRER_POLICY = 'same-origin'

# Content Security Policy (CSP) Headers
# Uncomment and configure according to your needs
# CSP_DEFAULT_SRC = ("'self'",)
# CSP_SCRIPT_SRC = ("'self'",)
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
# CSP_IMG_SRC = ("'self'", "data:")
# CSP_FONT_SRC = ("'self'",)
# CSP_CONNECT_SRC = ("'self'",)
# CSP_FRAME_ANCESTORS = ("'none'",)

# Database configuration for production
# Replace with your production database configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'your_db_name',
#         'USER': 'your_db_user',
#         'PASSWORD': 'your_db_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Static files configuration for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Email configuration for production
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Cache configuration for production
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#     }
# }
