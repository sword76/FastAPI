from fastapi import APIRouter, HTTPException, Query

from src.api.dependencies import DBDep, PaginationDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("",
            summary='Получение данных о всех бронированиях',
            description='Получение данных о бронированиях без фильтрации')
async def get_bookings(
                    pagination: PaginationDep,
                    db: DBDep,
):
    per_page = pagination.per_page or 5
    return await db.bookings.get_all(offset=per_page*(pagination.page-1))


@router.get("/me",
            summary='Получение данных о всех бронированиях авторизированного пользователя',
            description='Получение данных о бронированиях по ID пользователя')
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


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
    booking = await db.bookings.add(_booking)
    await db.commit()
    return {"status": "OK", "data": booking}
