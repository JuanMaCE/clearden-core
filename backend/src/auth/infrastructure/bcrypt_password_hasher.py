import logging

import bcrypt

from auth.application.password_hasher import PasswordHasher

logger = logging.getLogger(__name__)


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, plain: str) -> str:
        return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify(self, plain: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
        except ValueError:
            logger.warning("Hash de contraseña con formato inválido; no se puede verificar")
            return False