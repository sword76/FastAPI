from datetime import date

from sqlalchemy import select, func

from src.repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepositary
from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepositary):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        
        query = rooms_ids_for_booking(date_from, date_to, hotel_id)

        return await self.get_filtered(RoomsOrm.id.in_(query))
