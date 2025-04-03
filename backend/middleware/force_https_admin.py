from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import re
import os

class ForceHttpsAdminFormMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Solo interceptamos el login del admin
        if request.url.path == "/admin/login" and response.status_code == 200:
            # Leemos el contenido HTML
            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            html = body.decode("utf-8")

            # Reemplazamos la action del formulario si es http://
            host = request.headers.get("host")
            https_url = f"https://{host}/admin/login"

            html = re.sub(
                r'action="http://[^"]+(/admin/login)"',
                f'action="{https_url}"',
                html
            )

            return Response(content=html, status_code=200, media_type="text/html")

        return response
