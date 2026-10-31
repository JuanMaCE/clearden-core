import pytest   
from auth.application.password_hasher import PasswordHasher
from auth.infrastructure.bcrypt_password_hasher import BcryptPasswordHasher


@pytest.fixture
def hasher() -> PasswordHasher:
    return BcryptPasswordHasher()


def test_verify_returns_true_for_correct_password(hasher: PasswordHasher):
    hasged = hasher.hash("mysecretpassword")
    assert hasher.verify("mysecretpassword", hasged)
    

