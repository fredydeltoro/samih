#encoding:utf-8
from unipath import Path

BASE_DIR = Path(__file__).ancestor(3)

SECRET_KEY = '_nyhi5h$lhutjt)=ee-h77r9x7h^%j#d49k#lphircp9w833)e'

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'flat',
    'rest_framework',
]

LOCAL_APPS = [
    'apps.inicio',

    #Servicios
    'apps.servicios.administrativos.almacen.farmacia',
    'apps.servicios.administrativos.recursos_humanos.padronprofsalud',
    'apps.servicios.medicos.urgencias.productividad',

    #Catalogos
        'apps.catalogos.estadisticos.especialidades',
        'apps.catalogos.estadisticos.geograficos',
        'apps.catalogos.estadisticos.unidadesmedicas',
        'apps.catalogos.institucionales.servicios',
        'apps.catalogos.institucionales.tipoplazas',
        'apps.catalogos.institucionales.turnos',
        'apps.catalogos.medicos.catcauses',
        'apps.catalogos.medicos.causes',
        'apps.catalogos.medicos.cies',
        'apps.catalogos.medicos.medicamentos',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'samih.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'samih.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-MX'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True