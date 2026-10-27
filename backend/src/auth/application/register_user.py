from dataclasses import dataclass
from uuid import UUID

from auth.application.password_hasher import PasswordHasher
from auth.domain.email import Email
from auth.domain.errors import EmailAlreadyRegistered, WeakPassword
from auth.domain.user import User
from auth.domain.user_repository import UserRepository

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_BYTES = 72  # límite de bcrypt


@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    password: str


class RegisterUser:
    def __init__(self, users: UserRepository, hasher: PasswordHasher):
        self._users = users
        self._hasher = hasher

    def execute(self, cmd: RegisterUserCommand) -> UUID:
        email = Email(cmd.email)

        if len(cmd.password) < MIN_PASSWORD_LENGTH or len(cmd.password.encode("utf-8")) > MAX_PASSWORD_BYTES:
            raise WeakPassword()

        if self._users.find_by_email(email):
            raise EmailAlreadyRegistered(email.value)

        hashed_password = self._hasher.hash(cmd.password)
        user = User.register(email, hashed_password)
        self._users.save(user)
        return user.id
