import re
from dataclasses import dataclass

from auth.domain.errors import InvalidEmail


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
            raise InvalidEmail(self.value)
        object.__setattr__(self, "value", normalized)
