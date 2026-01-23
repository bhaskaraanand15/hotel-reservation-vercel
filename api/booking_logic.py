# booking_logic.py

import random

# Room definitions
# Floors 1–9 → 100–910
# Floor 10 → 1001–1007
ALL_ROOMS = {
    floor: (
        [1000 + i for i in range(1, 8)] if floor == 10
        else [floor * 100 + i for i in range(1, 11)]
    )
    for floor in range(1, 11)
}

# Stateful in-memory booking system
state = {
    "next_booking_id": 1,
    "bookings": []  # each = { id: int, rooms: [list-of-rooms] }
}


def room_exists(room: int) -> bool:
    return any(room in rooms for rooms in ALL_ROOMS.values())


def floor_of(room: int) -> int:
    if room >= 1000:
        return 10
    return room // 100


def get_occupied_rooms():
    occ = []
    for b in state["bookings"]:
        occ += b["rooms"]
    return occ


def is_occupied(room: int) -> bool:
    return room in get_occupied_rooms()


def available_rooms():
    occ = set(get_occupied_rooms())
    return [r for f in ALL_ROOMS for r in ALL_ROOMS[f] if r not in occ]


def book_single(room: int):
    bid = state["next_booking_id"]
    state["bookings"].append({"id": bid, "rooms": [room]})
    state["next_booking_id"] += 1
    return [room], bid


def book_multiple(count: int, preferred_floor=None):
    occupied = set(get_occupied_rooms())
    result = []

    # ---- 1. Fill same floor first (travel time = 0) ----
    if preferred_floor:
        for r in ALL_ROOMS[preferred_floor]:
            if r not in occupied and len(result) < count:
                result.append(r)

    # ---- 2. Closest floors next (travel priority 1,2,3…) ----
    if len(result) < count:
        for dist in range(1, 10):
            for direction in (-1, 1):
                f = (preferred_floor or 5) + dist * direction  # fallback center = floor 5
                if f < 1 or f > 10:
                    continue

                for r in ALL_ROOMS[f]:
                    if r not in occupied and len(result) < count:
                        result.append(r)

            if len(result) >= count:
                break

    # ---- 3. If still not enough, fill absolute global free ----
    if len(result) < count:
        for f in range(1, 11):
            for r in ALL_ROOMS[f]:
                if r not in occupied and len(result) < count:
                    result.append(r)

    return result


def commit_booking(value: int):
    """
    Booking Interpretation:
    - Value >= 100 → exact room number
    - Value < 100 → count (bulk)
    """
    if value >= 100:  # exact room
        room = value

        if not room_exists(room):
            return None, "Room does not exist"
        if is_occupied(room):
            return None, "Room is already occupied"

        return book_single(room)

    # Bulk booking
    count = value
    if count <= 0:
        return None, "Invalid room count"

    preferred_floor = 5  # neutral center, improves packing
    rooms = book_multiple(count, preferred_floor)

    if len(rooms) < count:
        return None, "Not enough rooms available"

    bid = state["next_booking_id"]
    state["bookings"].append({"id": bid, "rooms": rooms})
    state["next_booking_id"] += 1

    return rooms, bid


def vacate(bid: int):
    state["bookings"] = [b for b in state["bookings"] if b["id"] != bid]


def reset():
    state["bookings"] = []
    state["next_booking_id"] = 1


def random_room():
    free = available_rooms()
    return random.choice(free) if free else None
