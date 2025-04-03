from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import re

class ForceHttpsAdminFormMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Solo si estamos en /admin o rutas hijas
        if request.url.path.startswith("/admin") and response.status_code == 200:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            html = body.decode("utf-8")

            host = request.headers.get("host")
            if not host:
                return response

            # Reemplaza todos los recursos que vienen como HTTP por HTTPS
            html = html.replace(f"http://{host}", f"https://{host}")

            return Response(content=html, status_code=200, media_type="text/html")

        return response
