from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    # create booking
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(2024, 7, 5),
        date_to=date(2024, 7, 10),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)

    # read booking
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id

    # update booking
    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(2024, 7, 5),
        date_to=date(2024, 7, 20),
        price=500,
    )
    await db.bookings.update(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == date(2024, 7, 20)
    assert updated_booking.price == 500

    # delete booking
    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
    await db.commit()
