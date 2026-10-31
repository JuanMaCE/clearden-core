from fastapi import FastAPI

from auth.application.register_user import RegisterUser
from auth.domain.user_repository import UserRepository
from auth.infrastructure.bcrypt_password_hasher import BcryptPasswordHasher
from auth.infrastructure.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from auth.infrastructure.router import build_auth_router
from shared.infrastructure.database import build_engine, build_session_factory
from shared.infrastructure.settings import Settings


def create_app(users: UserRepository | None = None) -> FastAPI:
    app = FastAPI(title="Clearden API")

    if users is None:
        settings = Settings()
        session_factory = build_session_factory(build_engine(settings.database_url))
        users = SQLAlchemyUserRepository(session_factory)

    register_user = RegisterUser(users, BcryptPasswordHasher())
    app.include_router(build_auth_router(register_user))

    return app
