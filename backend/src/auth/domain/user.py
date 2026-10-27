from dataclasses import dataclass
from uuid import UUID, uuid4

from auth.domain.email import Email


@dataclass
class User:
    id: UUID
    email: Email
    password_hash: str
    is_active: bool

    @classmethod
    def register(cls, email: Email, password_hash: str) -> "User":
        return cls(
            id=uuid4(),
            email=email,
            password_hash=password_hash,
            is_active=True
        )
