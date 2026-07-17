from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response

from src.config import SERVICE_REGISTRY, PUBLIC_ROUTES, PUBLIC_GET_PREFIXES
from src.auth.jwt_verifier import verify_token
from src.proxy.forwarder import forward_request

router = APIRouter()


def _requires_auth(method: str, full_path: str) -> bool:
    if (method, full_path) in PUBLIC_ROUTES:
        return False
    if method == "GET" and full_path.startswith(PUBLIC_GET_PREFIXES):
        return False
    return True


def _build_target_url(path: str) -> str:
    service_key = path.split("/")[0]
    if service_key not in SERVICE_REGISTRY:
        raise HTTPException(status_code=404, detail=f"No service registered for '{service_key}'")
    return f"{SERVICE_REGISTRY[service_key]}/{path}"


@router.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def gateway(request: Request, path: str) -> Response:
    full_path = f"/api/{path}"

    if _requires_auth(request.method, full_path):
        verify_token(request.headers.get("Authorization"))

    target_url = _build_target_url(path)
    return await forward_request(target_url, request)
