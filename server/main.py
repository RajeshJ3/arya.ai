from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from uvicorn import run

# controllers
from server.accounts import auth_controllers
from server.accounts import account_controllers
from server.bank import controllers as bank_controllers
from server.debug import debug_controllers

# custom
from server.core.middlewares.auth_middlewares import AuthorizeRequestMiddleware
from server.core.settings import DATABASE_URL

app = FastAPI()

# middlewares
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)
app.add_middleware(AuthorizeRequestMiddleware)


# controllers
app.include_router(auth_controllers.router)
app.include_router(account_controllers.router)
app.include_router(bank_controllers.router)
app.include_router(debug_controllers.router)


@app.get("/")
def root():
    '''
    root end-point to test out, if the server is up or not.
    '''
    return {"detail": "PING PONG! It worked 🚀"}


if __name__ == "__main__":
    run(app, host='0.0.0.0', port=8000)
