from dataclasses import dataclass


@dataclass
class UserEntity:
    """ Represents a user in the database."""
    id: int
    email: str
    password_hash: str
    is_active: bool
    role: str
