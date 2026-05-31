"""
Configuration settings for CSRF Protection Demo
"""

import os
from datetime import timedelta

# Flask Configuration
DEBUG = os.environ.get('DEBUG', True)
TESTING = False

# Session Configuration
PERMANENT_SESSION_LIFETIME = timedelta(days=1)
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Application Metadata
APP_NAME = "CSRF Protection Demo"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Interactive demonstration of CSRF protection mechanisms"

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Server
HOST = os.environ.get('HOST', '127.0.0.1')
PORT = int(os.environ.get('PORT', 5000))
