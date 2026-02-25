from fastapi import Query, Body, Path, HTTPException, APIRouter

from src.repositories.hotels import HotelsRepository
from sqlalchemy import select, func

from src.api.dependencies import PaginationDep

from src.db import async_session_maker
from src.models.hotels import HotelsOrm

from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("",
            summary='Получение данных об отелях',
            description='Получить полных список отелей, либо конкретном отеле по названию или местоположению')
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Местоположение отеля")
):
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location, 
            title=title, 
            limit=per_page, 
            offset=per_page * (pagination.page-1)
        )
    

@router.get("/hotel_id",
            summary='Получение данных об отеле по ID',
            description='Получить все данных по отелю на основании его ID')
async def get_hotels(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("",
            summary='Добавление отеля',
            description='Добавить отель с полями title и location')
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": { 
            "title": "Отель Солнцеу моря 5 звезд",
            "location": "г. Сочи, ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Рай й фонтана",
            "location": "г. Дубай, ул. Шейха, 2",
        }
    }
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add_one(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}",
         summary='Полное обновление записи',
         description='Данная функция обновляет полностью запись об отела в базе данных',
         )
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        repo = HotelsRepository(session)
        if not await repo.get_one_or_none(id=hotel_id):
            raise HTTPException(status_code=404, detail="Hotel no found")
        await repo.edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}
    
    
@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
            )
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        repo = HotelsRepository(session)
        if not await repo.get_one_or_none(id=hotel_id):
            raise HTTPException(status_code=404, detail="Hotel no found")
        await repo.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        repo = HotelsRepository(session) 
        if not await repo.get_one_or_none(id=hotel_id):
            raise HTTPException(status_code=404, detail="Hotel not found")
        await repo.delete(id=hotel_id)
        await session.commit() 
    return {"status": "OK"}
