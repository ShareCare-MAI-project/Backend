from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.auth import auth_routes as auth
from app.user import user_routes as user
from app.items import router as items
from app.requests import router as requests
from app.sharecare import router as sharecare


def setup(app: FastAPI):
    _include_routes(app)
    _add_middleware(app)
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


def _include_routes(app: FastAPI):
    app.include_router(router=auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(router=user.router, prefix="/user", tags=["User"])
    app.include_router(router=items.router, prefix="/items", tags=["Items"])
    app.include_router(router=requests.router, prefix="/requests", tags=["Requests"])
    app.include_router(router=sharecare.router, prefix="/sharecare", tags=["ShareCare"])


def _add_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
