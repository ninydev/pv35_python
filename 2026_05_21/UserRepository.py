from UserEntity import UserEntity

class UserRepository:
    """ Repository for managing user data in the database."""

    def __init__(self):
        self._db = []
        self._next_id = 1

    def create_user(self, user: UserEntity) -> UserEntity:
        """ Creates a new user in the repository."""
        user.id = self._next_id
        self._next_id += 1
        self._db.append(user)
        return user
