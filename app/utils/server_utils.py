from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.auth import auth_routes as auth
from app.user import user_routes as user


def setup(app: FastAPI):
    _include_routes(app)
    _add_middleware(app)


def _include_routes(app: FastAPI):
    app.include_router(router=auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(router=user.router, prefix="/user", tags=["User"])


def _add_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
