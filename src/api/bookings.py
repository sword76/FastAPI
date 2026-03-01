from datetime import date

from fastapi import APIRouter, HTTPException, Query

from src.api.dependencies import DBDep, PaginationDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("/me",
            summary='Получение данных о всех бронированиях авторизированного пользователя',
            description='Получение данных о бронированиях по ID пользователя')
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
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


@router.get("",
            summary='Получение данных о всех бронированиях',
            description='Получение данных о бронированиях без фильтрации')
async def get_bookings(
                    pagination: PaginationDep,
                    db: DBDep,
                    room_id: int | None = Query(None, description="ID номера"),
                    user_id: int | None = Query(None, description="ID пользователя"),
                    date_from: date | None = Query(None, description="Дата заезда"),
                    date_to: date | None = Query(None, description="Дата выезда"),
                    price: int | None = Query(None, description="Цена бронирования")
):
    per_page = pagination.per_page or 5

    return await db.bookings.get_all(
        room_id=room_id,
        user_id=user_id,
        date_from=date_from,
        date_to=date_to,
        price=price,
        offset=per_page*(pagination.page-1),
    )
