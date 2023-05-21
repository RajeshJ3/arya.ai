# starlette
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, JSONResponse
from starlette.requests import Request
from starlette import status

# custom
from server.utils.helpers import is_auth_path, decode_and_validate_token

class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in [
            "/",
            "/docs",
            "/openapi.json"
        ] or is_auth_path(request.url.path):
            return await call_next(request)

        if request.method == "OPTIONS":
            return await call_next(request)

        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "details": "access_token is not provided",
                }
            )

        try:
            auth_token = bearer_token.split(" ")[1].strip()
            token_payload = decode_and_validate_token(auth_token)
        except Exception as e:
            JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": str(e),
                    "body": str(e),
                }
            )
        else:
            request.state.user_id = token_payload["sub"]
        return await call_next(request)
