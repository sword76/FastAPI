from src.repositories.base import BaseRepositary
from src.models.facilities import FacilitiesOrm
from src.schemas.facilities import Facility


class FacilitiesRepository(BaseRepositary):
    model = FacilitiesOrm
    schema = Facility
    