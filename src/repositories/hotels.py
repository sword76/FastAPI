from datetime import date

from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.repositories.mapper.mapper import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepositary

from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepositary):
    model = HotelsOrm
    mapper = HotelDataMapper
    
    async def get_filtered_by_time(
         self,
         location,
         title,
         date_from: date,
         date_to: date,
         limit,
         offset,
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_ids_subquery = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_subquery))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
