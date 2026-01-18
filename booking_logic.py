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

def get_occupied_rooms():
    occ = []
    for b in state["bookings"]:
        occ += b["rooms"]
    return occ

def is_occupied(room: int) -> bool:
    return room in get_occupied_rooms()

def commit_booking(room: int):
    bid = state["next_booking_id"]
    state["bookings"].append({"id": bid, "rooms": [room]})
    state["next_booking_id"] += 1
    return bid

def vacate_booking(bid: int):
    state["bookings"] = [b for b in state["bookings"] if b["id"] != bid]

def reset_hotel():
    state["next_booking_id"] = 1
    state["bookings"] = []

def random_room():
    occupied = set(get_occupied_rooms())
    available = [r for f in ALL_ROOMS for r in ALL_ROOMS[f] if r not in occupied]
    return random.choice(available) if available else None
