from abc import ABC, abstractmethod

from auth.domain.email import Email
from auth.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None: ...

    @abstractmethod
    def find_by_email(self, email: Email) -> User | None: ...
