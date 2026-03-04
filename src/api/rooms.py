from datetime import date

from fastapi import Body, APIRouter, Query

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms",
            summary='Получение данных об номерах в отеле',
            description='Получение списка всех номеров по отелю с его ID')
async def get_rooms(
        db: DBDep, 
        hotel_id: int,
        date_from: date = Query(example="2026-01-01"),
        date_to: date = Query(example="2026-08-10"),
        ):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.post("/{hotel_id}/rooms",
            summary='Добавление номера в отель',
            description='Добавить номер в отель по ID отеля')
async def create_room(db: DBDep, 
                      hotel_id: int, 
                      room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Аппартаменты на два человека",
        "value": { 
            "title": "Аппартаменты, 2 чел.",
            "description": "Аппартаменты с видом на море",
            "price": 123,
            "quantity": 2,
            "facilities_ids": [1, 2],
        }
    },
    "2": {
        "summary": "Двухкомнатный номер на четыре человека",
        "value": { 
            "title": "Номер, 2 ком., 4 чел.",
            "description": "Двухкомнатный номер на четыре человека с видом во двор",
            "price": 150,
            "quantity": 3,
            "facilities_ids": [1, 2],
        }
    }
})
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]

    await db.rooms_facilities.add_batch(rooms_facilities_data)
    await db.commit()
    
    return {"status": "OK", "data": room}


@router.get("/{hotel_id}/rooms/{room_id}",
            summary='Получение данных о номере по ID',
            description='Получить все данных о номере на основании его ID')
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    

@router.put("/{hotel_id}/rooms/{room_id}",
         summary='Полное обновление записи о номере',
         description='Данная функция обновляет полностью запись о номере в базе данных',
         )
async def edit_room(db: DBDep, 
                    hotel_id: int, 
                    room_id: int, 
                    room_data: RoomAddRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()

    return {"status": "OK"}
    
    
@router.patch("/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="Тут мы частично обновляем данные о номере: можно отправить ...",
            )
async def partially_edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
