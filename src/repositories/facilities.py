from src.repositories.base import BaseRepositary
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomsFacility


class FacilitiesRepository(BaseRepositary):
    model = FacilitiesOrm
    schema = Facility

class RoomsFacilitiesRepository(BaseRepositary):
    model = RoomsFacilitiesOrm
    schema = RoomsFacility
    