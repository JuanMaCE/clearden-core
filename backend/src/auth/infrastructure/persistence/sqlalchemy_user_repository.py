from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from auth.domain.email import Email
from auth.domain.errors import EmailAlreadyRegistered
from auth.domain.user import User
from auth.domain.user_repository import UserRepository
from auth.infrastructure.persistence.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def save(self, user: User) -> None:
        with self._session_factory() as session:
            session.merge(self._to_model(user))
            try:
                session.commit()
            except IntegrityError as error:
                # el UNIQUE de email frena registros simultáneos que pasaron find_by_email
                raise EmailAlreadyRegistered(user.email.value) from error

    def find_by_email(self, email: Email) -> User | None:
        with self._session_factory() as session:
            model = session.scalar(select(UserModel).where(UserModel.email == email.value))
            return self._to_domain(model) if model else None

    @staticmethod
    def _to_model(user: User) -> UserModel:
        return UserModel(
            id=user.id,
            email=user.email.value,
            password_hash=user.password_hash,
            is_active=user.is_active,
        )

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            email=Email(model.email),
            password_hash=model.password_hash,
            is_active=model.is_active,
        )
