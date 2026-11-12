from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "sandbox.oroborai.com",
    "www.sandbox.oroborai.com",
]

#SSL

# Trust HTTPS forwarded by Nginx
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Force HTTPS (enable after confirming SSL works)
SECURE_SSL_REDIRECT = True

# Session cookie settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Recommended for HTTPS deployments
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False

# Your CSRF trusted domains
CSRF_TRUSTED_ORIGINS = [
    "https://www.sandbox.oroborai.com",
    "https://sandbox.oroborai.com",
]

# Session lifetime (optional)
SESSION_COOKIE_AGE = 1800  # 30 minutes in seconds

# Ensure cookies are valid for your domain
SESSION_COOKIE_DOMAIN = ".sandbox.oroborai.com"
CSRF_COOKIE_DOMAIN = ".sandbox.oroborai.com"

# HTTP Strict Transport Security (HSTS) settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "SAMEORIGIN"

