from auth.domain.email import Email
from auth.domain.user import User
from auth.domain.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._users[user.email.value] = user

    def find_by_email(self, email: Email) -> User | None:
        return self._users.get(email.value)
