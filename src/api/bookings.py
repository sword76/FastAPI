from fastapi import Body, APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("/{booking_id}",
            summary='Получение данных о бронировании',
            description='Получение данных брони по её ID')
async def get_booking(db: DBDep, booking_id: int):
    return await db.bookings.get_filtered(id=booking_id)


@router.post("",
             summary='Добавление бронирования')
async def add_booking(db: DBDep, 
                      user_id: UserIdDep, 
                      booking_data: BookingAddRequest,                   
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Номер не найден")

    _booking = BookingAdd(
        room_id=booking_data.room_id,
        user_id=user_id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
        price=room.price,
    )
    booking = await db.bookings.add_one (_booking)
    await db.commit()
    return {"status": "OK", "data": booking}
