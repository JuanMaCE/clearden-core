import pytest   
from auth.application.password_hasher import PasswordHasher
from auth.infrastructure.bcrypt_password_hasher import BcryptPasswordHasher


@pytest.fixture
def hasher() -> PasswordHasher:
    return BcryptPasswordHasher()


def test_verify_returns_true_for_correct_password(hasher: PasswordHasher):
    hasged = hasher.hash("mysecretpassword")
    assert hasher.verify("mysecretpassword", hasged)
    

def test_verify_returns_false_for_wrong_password(hasher: PasswordHasher):
    hashed = hasher.hash("mysecretpassword")          # el usuario se registró con esta
    assert not hasher.verify("wrongpassword", hashed)  # en el login escribe otra

def test_hash_does_not_store_plain_password(hasher: PasswordHasher):
    password = "mysecretpassword"
    hashed = hasher.hash(password)

    assert hashed != password          # lo guardado no es la contraseña
    assert password not in hashed
    
def test_same_password_produces_different_hashes(hasher: PasswordHasher):
    password1 = "mysecretpassword"

    hashed1 = hasher.hash(password1)
    hashed2 = hasher.hash(password1)

    assert hashed1 != hashed2
    assert hasher.verify("mysecretpassword", hashed1)
    assert hasher.verify("mysecretpassword", hashed2)


def test_verify_works_with_non_ascii_password(hasher: PasswordHasher):
    hashed = hasher.hash("mysecretpasswordñ")
    assert hasher.verify("mysecretpasswordñ", hashed)

def test_verify_returns_false_for_malformed_hash(hasher: PasswordHasher):
    assert not hasher.verify("mysecretpassword", "esto-no-es-un-hash")