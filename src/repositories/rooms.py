
from src.repositories.base import BaseRepositary
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepositary):
    model = RoomsOrm
        