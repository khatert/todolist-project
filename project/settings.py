from pathlib import Path
 
BASE_DIR = Path(__file__).resolve().parent.parent
 
SECRET_KEY = 'django-insecure-todolist-secret-key-change-in-production'
 
DEBUG = True
 
ALLOWED_HOSTS = ['*'] 

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'rest_framework',
    'todolist',
]
 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
 
ROOT_URLCONF = 'project.urls'
 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]
 
WSGI_APPLICATION = 'project.wsgi.application'
 
# ─── MongoDB Settings ───────────────────────────────────────────────────────────────
MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DB  = 'todolist'
 

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'todolist' / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'