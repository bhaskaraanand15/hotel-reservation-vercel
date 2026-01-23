import random

ALL_ROOMS = {
    floor: (
        [1000 + i for i in range(1, 8)] if floor == 10
        else [floor * 100 + i for i in range(1, 11)]
    )
    for floor in range(1, 11)
}

state = {
    "next_booking_id": 1,
    "bookings": []
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


def available_rooms_sorted():
    occupied = set(get_occupied_rooms())
    rooms = [r for f in ALL_ROOMS for r in ALL_ROOMS[f] if r not in occupied]
    rooms.sort()
    return rooms


def book_one(room: int):
    bid = state["next_booking_id"]
    state["bookings"].append({"id": bid, "rooms": [room]})
    state["next_booking_id"] += 1
    return bid


def book_multiple(count: int, start_floor=None):
    occupied = set(get_occupied_rooms())
    result = []

    # If no preferred floor, just pick lowest free rooms
    if start_floor is None:
        for f in range(1, 11):
            for r in ALL_ROOMS[f]:
                if r not in occupied and len(result) < count:
                    result.append(r)
        return result

    # 1. Try same floor first
    for r in ALL_ROOMS[start_floor]:
        if r not in occupied and len(result) < count:
            result.append(r)

    if len(result) == count:
        return result

    # 2. Try nearest floors by travel time difference
    for dist in range(1, 10):
        for direction in (-1, 1):
            f = start_floor + dist * direction
            if f < 1 or f > 10:
                continue
            for r in ALL_ROOMS[f]:
                if r not in occupied and len(result) < count:
                    result.append(r)
            if len(result) == count:
                return result

    return result


def commit_booking(input_value: int):
    # If room number (>= 100)
    if input_value >= 100:
        room = input_value
        if not room_exists(room):
            return None, "Room does not exist"
        if is_occupied(room):
            return None, "Room already occupied"
        bid = book_one(room)
        return [room], bid

    # If count
    count = input_value
    rooms = book_multiple(count)
    if len(rooms) < count:
        return None, "Not enough rooms available"

    bid = state["next_booking_id"]
    state["bookings"].append({"id": bid, "rooms": rooms})
    state["next_booking_id"] += 1
    return rooms, bid


def vacate_booking(bid: int):
    state["bookings"] = [b for b in state["bookings"] if b["id"] != bid]


def reset_hotel():
    state["next_booking_id"] = 1
    state["bookings"] = []


def random_room():
    available = available_rooms_sorted()
    return random.choice(available) if available else None
