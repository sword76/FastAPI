from fastapi import Query, Body, Path, HTTPException, APIRouter

from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomAddRequest, RoomPatch

from src.api.dependencies import PaginationDep

from src.db import async_session_maker

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])


@router.get("",
            summary='Получение данных об комнатах в отеле',
            description='Получение списка всех номеров по отелю с его ID',
            response_model=list[Room])
async def get_rooms(hotel_id: int, pagination: PaginationDep):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@router.post("",
            summary='Добавление комнаты в отель',
            description='Добавить комнату в отель по ID отеля')
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Аппартаменты на два человека",
        "value": { 
            "title": "Аппартаменты, 2 чел.",
            "description": "Аппартаменты с видом на море",
            "price": 123,
            "quantity": 3, 
        }
    },
    "2": {
        "summary": "Двухкомнатный номер на четыре человека",
        "value": { 
            "title": "Номер, 2 ком., 4 чел.",
            "description": "Двухкомнатный номер на четыре человека с видом во двор",
            "price": 150,
            "quantity": 3, 
        }
    }
})
):
    room_add = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add_one(room_add)
        await session.commit()

    return {"status": "OK", "data": room}


@router.get("/{room_id}",
            summary='Получение данных о номере по ID',
            description='Получить все данных о номере на основании его ID')
async def get_hotels(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)
    

@router.put("/{room_id}",
         summary='Полное обновление записи о номере',
         description='Данная функция обновляет полностью запись о номере в базе данных',
         )
async def edit_hotel(room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        repo = RoomsRepository(session)
        if not await repo.get_one_or_none(id=room_id):
            raise HTTPException(status_code=404, detail="Room no found")
        await repo.edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}
    
    
@router.patch(
    "/{room_id}",
    summary="Частичное обновление данных о номере",
    description="Тут мы частично обновляем данные о номере: можно отправить ...",
            )
async def partially_edit_hotel(
        room_id: int,
        hotel_data: RoomPatch,
):
    async with async_session_maker() as session:
        repo = RoomsRepository(session)
        if not await repo.get_one_or_none(id=room_id):
            raise HTTPException(status_code=404, detail="Room no found")
        await repo.edit(hotel_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{room_id}")
async def delete_hotel(room_id: int):
    async with async_session_maker() as session:
        repo = RoomsRepository(session) 
        if not await repo.get_one_or_none(id=room_id):
            raise HTTPException(status_code=404, detail="Room not found")
        await repo.delete(id=room_id)
        await session.commit() 
    return {"status": "OK"}