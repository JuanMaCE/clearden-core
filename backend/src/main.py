from fastapi import FastAPI

from auth.application.register_user import RegisterUser
from auth.infrastructure.bcrypt_password_hasher import BcryptPasswordHasher
from auth.infrastructure.in_memory_user_repository import InMemoryUserRepository
from auth.infrastructure.router import build_auth_router


def create_app() -> FastAPI:
    app = FastAPI(title="Clearden API")

    register_user = RegisterUser(InMemoryUserRepository(), BcryptPasswordHasher())
    app.include_router(build_auth_router(register_user))

    return app


app = create_app()
