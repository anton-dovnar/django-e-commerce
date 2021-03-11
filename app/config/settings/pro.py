import socket

from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-3] + "0.1" for ip in ips]

# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 2592000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
