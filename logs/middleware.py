from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import user_agents

from .tasks import submit_log_to_db


class UserLogMiddleware(MiddlewareMixin):
    EXCLUDED_PATHS = (
        "/static/",
        "/media/",
        "/favicon.ico",
        "/robots.txt",
        "/manifest.json",
        "/service-worker.js",
    )

    EXCLUDED_EXTENSIONS = (
        ".css",
        ".js",
        ".map",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".ico",
        ".webp",
        ".avif",
        ".woff",
        ".woff2",
        ".ttf",
        ".eot",
        ".otf",
        ".mp4",
        ".mp3",
        ".wav",
        ".pdf",
        ".zip",
        ".xml",
        ".txt",
    )

    def process_request(self, request):
        path = request.path.lower()

        if path.startswith(self.EXCLUDED_PATHS):
            return

        if path.endswith(self.EXCLUDED_EXTENSIONS):
            return

        user_agent = user_agents.parse(request.META.get("HTTP_USER_AGENT", ""))

        submit_log_to_db.delay(user=request.user.id if request.user.is_authenticated else None , os=user_agent.os.family , path=request.path , ip=request.META.get("REMOTE_ADDR"))