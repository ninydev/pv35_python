from dataclasses import dataclass


@dataclass
class UserCreateRequest:
    """ Represents a user creation request."""
    email: str
    password: str