
from src.repositories.base import BaseRepositary
from src.models.users import UsersOrm
from src.schemas.users import User

class UsersRepository(BaseRepositary):
    model = UsersOrm
    schema = User
