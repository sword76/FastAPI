from src.repositories.base import BaseRepositary
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepositary):
    model = RoomsOrm
    schema = Room
