from dataclasses import dataclass


@dataclass
class UserResponse:
    """ Represents a user creation request."""
    email: str
    role: str