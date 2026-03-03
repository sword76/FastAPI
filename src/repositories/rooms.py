from datetime import date

from sqlalchemy import select, func

from src.db import engine
from src.repositories.base import BaseRepositary
from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepositary):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        
        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(BookingsOrm.date_from <= date_to,
                    BookingsOrm.date_to >= date_from)
                    .group_by(BookingsOrm.room_id)
                    .cte(name="rooms_count")
        )

        rooms_left_table = (
            select(RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked,0)).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        query = (
            select(rooms_left_table)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0)
        )
        
        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        # result = await self.session.execute(query)
        # return result.scalars().all()

    """
        WITH rooms_count AS (
            SELECT  room_id, count(*) AS rooms_booked FROM bookings
            WHERE date_from <= '2026-11-07' AND date_to >= '2026-01-01'
            GROUP BY room_id
        ),
        rooms_left_table AS (
            SELECT rooms.id AS room_id, quantity - COALESCE(rooms_booked, 0) AS rooms_left
            FROM rooms
            LEFT JOIN rooms_count ON rooms.id = rooms_count.room_id
        )
        SELECT  * FROM rooms_left_table
        WHERE rooms_left > 0;
    """