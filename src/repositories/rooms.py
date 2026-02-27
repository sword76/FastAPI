from sqlalchemy import select
from src.repositories.base import BaseRepositary
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepositary):
    model = RoomsOrm
    schema = Room

    async def get_all(self, 
                      hotel_id: int, 
                      limit: int, 
                      offset: int):
        query = (
            select(self.model)
            .filter_by(hotel_id=hotel_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]
