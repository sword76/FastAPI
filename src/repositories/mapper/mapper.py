from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from src.repositories.mapper.base import DataMapper

class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel
    