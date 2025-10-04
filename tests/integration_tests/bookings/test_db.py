from datetime import date

from src.schemas.bookings import BookingAdd


async def test_add_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(2024, 7, 5),
        date_to=date(2024, 7, 10),
        price=100
    )
    await db.bookings.add(booking_data)
    await db.commit()