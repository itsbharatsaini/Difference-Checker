# -*- coding: utf-8 -*-
import os
from lms.envs.production import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "connect": False,
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "ora2-storage": {
        "KEY_PREFIX": "ora2-storage",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    }
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "My Open edX - http://local.edly.io"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

# ORA2
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {"handlers": ["console"], "level": "WARNING"}

# These warnings are visible in simple commands and init tasks
import warnings

from django.utils.deprecation import RemovedInDjango50Warning, RemovedInDjango51Warning
warnings.filterwarnings("ignore", category=RemovedInDjango50Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango51Warning)

warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="boto.plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="botocore.vendored.requests.packages.urllib3._collections")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs.opener")
SILENCED_SYSTEM_CHECKS = ["2_0.W001", "fields.W903"]

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://local.edly.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "6iO0CNP9pSmfsfiVEJnBJzOg"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "BzwJ4-n3RYsCN_-xnq7d_2bBLqoHCDAAyiI5g_pqmvFlT6G7gnZbivNVDW1KDE4IakfGp8ihd8VnuzrDyH8331S3za-pBXkRGEMQPAsNoHZH2TRB_NWM-m6J3eEV7NeKWeDHIBU1pnqoXFk84cPSgPL66sZ6m2ZTu037Ff4qboJOm0BXR_qTPNsCmmR-CVTFMYvc92cCQhZoaMtPUPjwUUC_T1cdgVFewJ-ga6KImtkTCQ-kB0n7WJYqU4KFEWJTxOKmOVYL3BWulnlcLyXglAAn222rB75Akyda6sHrc7iqIN2_oqJNSIMX_RmHUpKSYqrAmV8D23kjaeVyStXZKQ",
        "n": "nYbWFAhEHYJpL0wMgbij84hZfBHkbqiwhzWnXLCCa0-BTKbq2idS8LGYGX0c9HQh4NuiO4F9FBrHOS9G-NAhq-5nt0LXmKNL2qVqpz3goV5zfRTs8QFb7aTRjaA9hEHDegzQrwOXlU-j1Gr9Z_Q6hsR-MzyMf_HdH-ncwb9PQeMTXRPB_4meLemKZSPOaF7oi1iumgwcPIPTvF8pjoiChaFXeS0dXluhUi9kqeH6uO1C0b9MQLn656vB2Rh_UFSEOC63c_JlR5pCSm7mJF_FknnEgAybXBgoALUvJN9XM9-zHS8X73ji_gxMVMtsmhoRtrkNA7QBdPUcOUnXTboLCQ",
        "p": "vG9V03rCRN-DlCoVXykbfc_huh82QChXTOrR4R-Y8ZmRFOgFPDNeV9eqZuoaJlJaSIM-PUYqO-rC6NaPC74xlur1-Q7AW-TM7oWzZP_moAOG1lRtM6_Is_s4-8hJ7P-D6F9IFOcUDkIju3CU4LGJPv2c6xZMBG2zBYT1C1MF_SU",
        "q": "1gJmhW9Xz0wGJsM4eMKIeqcwQmjkF7jh0ha9QiwIa375vltAcfNcM7Dk0Mos4ef0h_QXIS-4P7ZQNecl9ZlcXkdNmeTaf7bKNUNecPs-sexGw4ImO-8q5S4pTxgSab0orDujPMfXwsoGGBG3PZtuI32LutSsiX82urcJWf8V-xU",
        "dq": "olin1Uml30fY0sb9q_5G8mSqI3bWsXg7NtixMeWdbY6hflpTBR6ML1pd-lWkvqrrwcbVVQOSTiLLrlhvX2S7wXlt0PTfHEtaEhXNKwAti2OmOuIchxLkA3-FLs8gCL7Kf_2t04n2j3oaLWAjFcU3RA0VVuHHEXdD2VjI61CrKBE",
        "dp": "QfJU_yY_RwtSaVAxGpSwYl-WiCTUP6_enbSwrzD3vdYYyFBLRL5VjjiUEmBrtm2r2yTTa25a6Y1HmWU9usZdZIvmebuH5qE0d2WjWv2UIPwa_HefoC8s9pA9aSC3fpIOAA0YlPgqNLNA_iBwehKoDbuEZ2HuSL57oLrfZ48u0WE",
        "qi": "ZuqRaJ5gIZdYVknd92dTXmHhFViClIsdATfmsjstetKhf01bl1roRJYD_NlXPLNVhmBv69kTZeQcWwFN9LiH7YtV7tvOT9K3EkyfPlI0LPclp6fCbxFylGcv0BiOPuVVIzUw8C6R1OxUllBAqUYpRlPvMiT1OHCOCUMTSf9e5zY",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "nYbWFAhEHYJpL0wMgbij84hZfBHkbqiwhzWnXLCCa0-BTKbq2idS8LGYGX0c9HQh4NuiO4F9FBrHOS9G-NAhq-5nt0LXmKNL2qVqpz3goV5zfRTs8QFb7aTRjaA9hEHDegzQrwOXlU-j1Gr9Z_Q6hsR-MzyMf_HdH-ncwb9PQeMTXRPB_4meLemKZSPOaF7oi1iumgwcPIPTvF8pjoiChaFXeS0dXluhUi9kqeH6uO1C0b9MQLn656vB2Rh_UFSEOC63c_JlR5pCSm7mJF_FknnEgAybXBgoALUvJN9XM9-zHS8X73ji_gxMVMtsmhoRtrkNA7QBdPUcOUnXTboLCQ",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.edly.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "6iO0CNP9pSmfsfiVEJnBJzOg"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = True
CORS_ALLOW_HEADERS = corsheaders_default_headers + ('use-jwt-cookie',)

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}


######## End of settings common to LMS and CMS

######## Common LMS settings
LOGIN_REDIRECT_WHITELIST = ["studio.local.edly.io"]

# Better layout of honor code/tos links during registration
REGISTRATION_EXTRA_FIELDS["terms_of_service"] = "hidden"
REGISTRATION_EXTRA_FIELDS["honor_code"] = "hidden"

# Fix media files paths
PROFILE_IMAGE_BACKEND["options"]["location"] = os.path.join(
    MEDIA_ROOT, "profile-images/"
)

COURSE_CATALOG_VISIBILITY_PERMISSION = "see_in_catalog"
COURSE_ABOUT_VISIBILITY_PERMISSION = "see_about_page"

# Allow insecure oauth2 for local interaction with local containers
OAUTH_ENFORCE_SECURE = False

# Email settings
DEFAULT_EMAIL_LOGO_URL = LMS_ROOT_URL + "/theming/asset/images/logo.png"
BULK_EMAIL_SEND_USING_EDX_ACE = True
FEATURES["ENABLE_FOOTER_MOBILE_APP_LINKS"] = False

# Branding
MOBILE_STORE_ACE_URLS = {}
SOCIAL_MEDIA_FOOTER_ACE_URLS = {}

# Make it possible to hide courses by default from the studio
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = False

# Caching
CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_lms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_lms",
}

# Create folders if necessary
for folder in [DATA_DIR, LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

# MFE: enable API and set a low cache timeout for the settings. otherwise, weird
# configuration bugs occur. Also, the view is not costly at all, and it's also cached on
# the frontend. (5 minutes, hardcoded)
ENABLE_MFE_CONFIG_API = True
MFE_CONFIG_API_CACHE_TIMEOUT = 1

# MFE-specific settings

FEATURES['ENABLE_AUTHN_MICROFRONTEND'] = True


FEATURES['ENABLE_NEW_BULK_EMAIL_EXPERIENCE'] = True


LEARNER_HOME_MFE_REDIRECT_PERCENTAGE = 100


######## End of common LMS settings

ALLOWED_HOSTS = [
    ENV_TOKENS.get("LMS_BASE"),
    FEATURES["PREVIEW_LMS_BASE"],
    "lms",
]
CORS_ORIGIN_WHITELIST.append("http://local.edly.io")


# When we cannot provide secure session/csrf cookies, we must disable samesite=none
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"


# CMS authentication
IDA_LOGOUT_URI_LIST.append("http://studio.local.edly.io/logout/")

# Required to display all courses on start page
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = True

# Dynamic config API settings
# https://openedx.github.io/frontend-platform/module-Config.html
MFE_CONFIG = {
    "BASE_URL": "apps.local.edly.io",
    "CSRF_TOKEN_API_PATH": "/csrf/api/v1/token",
    "CREDENTIALS_BASE_URL": "",
    "DISCOVERY_API_BASE_URL": "",
    "FAVICON_URL": "http://local.edly.io/favicon.ico",
    "INFO_EMAIL": "contact@local.edly.io",
    "LANGUAGE_PREFERENCE_COOKIE_NAME": "openedx-language-preference",
    "LMS_BASE_URL": "http://local.edly.io",
    "LOGIN_URL": "http://local.edly.io/login",
    "LOGO_URL": "http://local.edly.io/theming/asset/images/logo.png",
    "LOGO_WHITE_URL": "http://local.edly.io/theming/asset/images/logo.png",
    "LOGO_TRADEMARK_URL": "http://local.edly.io/theming/asset/images/logo.png",
    "LOGOUT_URL": "http://local.edly.io/logout",
    "MARKETING_SITE_BASE_URL": "http://local.edly.io",
    "PASSWORD_RESET_SUPPORT_LINK": "mailto:contact@local.edly.io",
    "REFRESH_ACCESS_TOKEN_ENDPOINT": "http://local.edly.io/login_refresh",
    "SITE_NAME": "My Open edX",
    "STUDIO_BASE_URL": "http://studio.local.edly.io",
    "USER_INFO_COOKIE_NAME": "user-info",
    "ACCESS_TOKEN_COOKIE_NAME": "edx-jwt-cookie-header-payload",
}

# MFE-specific settings


AUTHN_MICROFRONTEND_URL = "http://apps.local.edly.io/authn"
AUTHN_MICROFRONTEND_DOMAIN  = "apps.local.edly.io/authn"
MFE_CONFIG["DISABLE_ENTERPRISE_LOGIN"] = True



ACCOUNT_MICROFRONTEND_URL = "http://apps.local.edly.io/account/"
MFE_CONFIG["ACCOUNT_SETTINGS_URL"] = ACCOUNT_MICROFRONTEND_URL



MFE_CONFIG["ENABLE_NEW_EDITOR_PAGES"] = True
MFE_CONFIG["ENABLE_PROGRESS_GRAPH_SETTINGS"] = True



DISCUSSIONS_MICROFRONTEND_URL = "http://apps.local.edly.io/discussions"
MFE_CONFIG["DISCUSSIONS_MFE_BASE_URL"] = DISCUSSIONS_MICROFRONTEND_URL
DISCUSSIONS_MFE_FEEDBACK_URL = None



WRITABLE_GRADEBOOK_URL = "http://apps.local.edly.io/gradebook"



LEARNER_HOME_MICROFRONTEND_URL = "http://apps.local.edly.io/learner-dashboard/"



LEARNING_MICROFRONTEND_URL = "http://apps.local.edly.io/learning"
MFE_CONFIG["LEARNING_BASE_URL"] = "http://apps.local.edly.io/learning"



ORA_GRADING_MICROFRONTEND_URL = "http://apps.local.edly.io/ora-grading"



PROFILE_MICROFRONTEND_URL = "http://apps.local.edly.io/profile/u/"
MFE_CONFIG["ACCOUNT_PROFILE_URL"] = "http://apps.local.edly.io/profile"



COMMUNICATIONS_MICROFRONTEND_URL = "http://apps.local.edly.io/communications"
MFE_CONFIG["SCHEDULE_EMAIL_SECTION"] = True


LOGIN_REDIRECT_WHITELIST.append("apps.local.edly.io")
CORS_ORIGIN_WHITELIST.append("http://apps.local.edly.io")
CSRF_TRUSTED_ORIGINS.append("http://apps.local.edly.io")


