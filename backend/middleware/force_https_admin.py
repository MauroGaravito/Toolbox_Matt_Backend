from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import re

class ForceHttpsAdminFormMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Solo afecta el login del admin
        if request.url.path == "/admin/login" and response.status_code == 200:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            html = body.decode("utf-8")

            host = request.headers.get("host")
            base_https = f"https://{host}"

            # Reemplazar todas las rutas que empiezan por http://{host}
            html = re.sub(
                r'http://'+re.escape(host),
                base_https,
                html
            )

            return Response(content=html, status_code=200, media_type="text/html")

        return response
