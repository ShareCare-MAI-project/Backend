

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.auth import auth_routes as auth


def setup(app: FastAPI):
    _include_routes(app)
    _add_middleware(app)


def _include_routes(app: FastAPI):
    app.include_router(router=auth.router)


def _add_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



