from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey
from src.db import BaseModel


class BookingsOrm(BaseModel):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date] = mapped_column(DateTime)
    date_to: Mapped[date] = mapped_column(DateTime)
    price: Mapped[int]


    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days
