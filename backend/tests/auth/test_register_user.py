import pytest

from auth.application.password_hasher import PasswordHasher
from auth.application.register_user import RegisterUser, RegisterUserCommand
from auth.domain.email import Email
from auth.domain.errors import EmailAlreadyRegistered, InvalidEmail, WeakPassword
from auth.infrastructure.in_memory_user_repository import InMemoryUserRepository


class FakeHasher(PasswordHasher):
    def hash(self, plain: str) -> str:
        return f"hashed:{plain}"


@pytest.fixture
def users() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def register_user(users: InMemoryUserRepository) -> RegisterUser:
    return RegisterUser(users, FakeHasher())


def test_registers_user_with_hashed_password(register_user, users):
    user_id = register_user.execute(RegisterUserCommand("Ana@Example.com ", "secreto123"))

    user = users.find_by_email(Email("ana@example.com"))
    assert user is not None
    assert user.id == user_id
    assert user.password_hash == "hashed:secreto123"
    assert user.is_active


def test_rejects_duplicated_email(register_user):
    register_user.execute(RegisterUserCommand("ana@example.com", "secreto123"))

    with pytest.raises(EmailAlreadyRegistered):
        register_user.execute(RegisterUserCommand("ANA@example.com", "otro12345"))


def test_rejects_invalid_email(register_user):
    with pytest.raises(InvalidEmail):
        register_user.execute(RegisterUserCommand("no-es-un-email", "secreto123"))


@pytest.mark.parametrize("password", ["corta", "x" * 73])
def test_rejects_weak_password(register_user, password):
    with pytest.raises(WeakPassword):
        register_user.execute(RegisterUserCommand("ana@example.com", password))
