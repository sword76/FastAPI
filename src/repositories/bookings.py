from src.repositories.base import BaseRepositary
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepositary):
    model = BookingsOrm
    schema = Booking
    