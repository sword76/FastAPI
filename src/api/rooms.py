from fastapi import Body, HTTPException, APIRouter

from src.db import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

from src.api.dependencies import PaginationDep


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms",
            summary='Получение данных об комнатах в отеле',
            description='Получение списка всех номеров по отелю с его ID')
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms",
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


@router.get("/{hotel_id}/rooms/{room_id}",
            summary='Получение данных о номере по ID',
            description='Получить все данных о номере на основании его ID')
async def get_rooms(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
    

@router.put("/{hotel_id}/rooms/{room_id}",
         summary='Полное обновление записи о номере',
         description='Данная функция обновляет полностью запись о номере в базе данных',
         )
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}
    
    
@router.patch("/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="Тут мы частично обновляем данные о номере: можно отправить ...",
            )
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPatchRequest(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}
