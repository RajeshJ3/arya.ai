# fastapi
from fastapi import APIRouter
from fastapi_sqlalchemy import db

# starlette
from starlette.requests import Request

# models
from server.models import User

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
    user_id = request.state.user_id
    user = db.session.query(User).filter(
        User.id == user_id
    ).first()
    return user.dict()
