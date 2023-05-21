# fastapi
from fastapi import APIRouter

# starlette
from starlette.requests import Request


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    dependencies=[],
    responses={
        400: {"description": "Bad request"}
    },
)


@router.get("/profile/")
def profile(request: Request):
    return {}
