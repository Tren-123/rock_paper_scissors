"""
ASGI config for rock_paper_scissors project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from game.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rock_paper_scissors.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket" : AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(ws_urlpatterns)))
})
