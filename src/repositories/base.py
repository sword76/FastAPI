from sqlalchemy import select, insert, update, delete as rec_delete
from pydantic import BaseModel

from src.repositories.mapper.base import DataMapper


class BaseRepositary:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session


    async def get_filtered(self, *filter, **filter_by):
        query = (select(self.model)
                 .filter(*filter)
                 .filter_by(**filter_by))
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]


    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.model_to_domain_entity(model)


    async def get_list_or_none_batch(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        models = result.scalars().all()
        if not models:
            return None
        return [self.mapper.map_to_domain_entity(model) for model in models]


    async def add(self, data: BaseModel):
        new_instance = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(new_instance)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)
    

    async def add_batch(self, data: list[BaseModel]):
        new_instance = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(new_instance)
    

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        
        await self.session.execute(query)


    async def delete(self, **filter_by) -> None:
        query = rec_delete(self.model).filter_by(**filter_by)
        await self.session.execute(query)
    