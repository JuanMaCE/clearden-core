from dataclasses import dataclass
from auth.domain.user_repository import UserRepository
from backend.src.auth.application.register_user import MAX_PASSWORD_BYTES, MIN_PASSWORD_LENGTH
from backend.src.auth.domain.email import Email
from backend.src.auth.domain.errors import WeakPassword

@dataclass(frozen=True)
class LoginUserCommand:
    email: str
    password: str

class LoginUser:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, cmd: LoginUserCommand):
        email = Email(cmd.email)

        if len(cmd.password) < MIN_PASSWORD_LENGTH or len(cmd.password.encode("utf-8")) > MAX_PASSWORD_BYTES:
            raise WeakPassword()

        if self._users.find_by_email(email):
            return True