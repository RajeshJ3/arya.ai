# fastapi
from fastapi import APIRouter
from fastapi_sqlalchemy import db

# starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette import status

# custom
from server.accounts.schemas.response_schemas import (
    GenericResponseSchema,
    LoginResponseSchema
)
from server.accounts.schemas.request_schemas import (
    LoginSchema,
    RegistrationSchema
)

# models
from server.models import User, BankAccount

# helpers
from server.utils.helpers import (
    generate_jwt,
    hash_password,
    compare_password_hash
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[],
    responses={
        400: {"description": "Bad request"}
    },
)


@router.post("/login/", response_model=LoginResponseSchema)
def login(request: Request, payload: LoginSchema):
    # search for user's existence
    user = db.session.query(User).filter(User.email == payload.email).first()

    # return 400 if user with this email already doesn't exists
    if not user:
        return JSONResponse({"details": "account does not exists!"}, status_code=status.HTTP_400_BAD_REQUEST)

    # match the two password hashes
    hash_matched = compare_password_hash(payload.password, user.password)

    # return 400 if the two password hashes doesn't match
    if not hash_matched:
        return JSONResponse({"details": "invalid password!"}, status_code=status.HTTP_400_BAD_REQUEST)

    # generate and return access_token for the user
    return {
        "access_token": generate_jwt(user.id),
        "user": user.dict()
    }


@router.post("/registration/", response_model=GenericResponseSchema, status_code=status.HTTP_201_CREATED)
def registration(request: Request, payload: RegistrationSchema):
    # TODO: check if user with this email already exists?
    user = db.session.query(User).filter(
        User.email == payload.email
    ).first()

    # return 400 if user with this email already exists
    if user:
        return JSONResponse({"details": "user with this email already exists!"}, status_code=status.HTTP_400_BAD_REQUEST)

    # TODO: check for password strength
    if len(payload.password1) <= 6:
        return JSONResponse({"details": "password is weak!"}, status_code=status.HTTP_400_BAD_REQUEST)
    if payload.password1 != payload.password2:
        return JSONResponse({"details": "the two passwords didn't matched!"}, status_code=status.HTTP_400_BAD_REQUEST)

    # TODO: create password hash
    password_hash = hash_password(payload.password1)
    payload.password1 = password_hash
    payload.password2 = password_hash

    # TODO: save user instance to DB
    user = User(
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
        password=payload.password1
    )
    db.session.add(user)
    db.session.commit()

    # TODO: create a default bank account
    bank_account = db.session.add(BankAccount(
        user_id=user.id
    ))
    db.session.add(user)
    db.session.commit()

    return {
        "details": "Account created!"
    }
