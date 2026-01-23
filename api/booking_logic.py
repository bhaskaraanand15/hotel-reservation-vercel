import random

# -------------------------------
# ROOM MODEL
# -------------------------------
ALL_ROOMS = {
    floor: (
        [1000 + i for i in range(1, 8)] if floor == 10
        else [floor * 100 + i for i in range(1, 11)]
    )
    for floor in range(1, 11)
}

# -------------------------------
# STATE
# -------------------------------
state = {
    "next_booking_id": 1,
    "bookings": []
}

# -------------------------------
# HELPERS
# -------------------------------
def room_exists(room: int) -> bool:
    return any(room in rooms for rooms in ALL_ROOMS.values())

def floor_of(room: int) -> int:
    return 10 if room >= 1000 else room // 100

def get_occupied_rooms():
    occupied = []
    for b in state["bookings"]:
        occupied += b["rooms"]
    return occupied

def is_occupied(room: int) -> bool:
    return room in get_occupied_rooms()

def available_rooms_sorted():
    occupied = set(get_occupied_rooms())
    rooms = [r for f in ALL_ROOMS for r in ALL_ROOMS[f] if r not in occupied]
    rooms.sort()
    return rooms

# -------------------------------
# BOOKING MECHANICS
# -------------------------------
def book_one(room: int):
    """Book a single specific room."""
    bid = state["next_booking_id"]
    state["bookings"].append({"id": bid, "rooms": [room]})
    state["next_booking_id"] += 1
    return bid

def book_multiple(count: int, preferred_floor=None):
    """
    Strategy (C - Best competition behavior):
    1. Try same floor if preferred_floor is given
    2. Else fill from lowest floor upwards
    3. If not enough on same floor, spill to nearest floor
    """
    occupied = set(get_occupied_rooms())
    result = []

    # 1. If user provided a preferred_floor (e.g., first room)
    if preferred_floor is not None:
        # → cluster on same floor first
        for r in ALL_ROOMS[preferred_floor]:
            if r not in occupied and len(result) < count:
                result.append(r)

        if len(result) == count:
            return result

        # 2. Try nearest floors by travel optimization
        for d in range(1, 10):
            for direction in (-1, 1):
                f = preferred_floor + d * direction
                if f < 1 or f > 10:
                    continue
                for r in ALL_ROOMS[f]:
                    if r not in occupied and len(result) < count:
                        result.append(r)
                if len(result) == count:
                    return result

        return result

    # No preferred floor → use globally sorted allocation
    for f in range(1, 11):
        for r in ALL_ROOMS[f]:
            if r not in occupied and len(result) < count:
                result.append(r)

    return result


def commit_booking(value: int):
    """
    unified interface for main.py
    - If value >= 100: treat as specific room booking
    - Else treat as bulk booking count
    Returns: (rooms, booking_id) OR (None, error_message)
    """

    # -----------------------------
    # SINGLE ROOM BOOKING
    # -----------------------------
    if value >= 100:
        room = value
        if not room_exists(room):
            return None, "Room does not exist"
        if is_occupied(room):
            return None, "Room already occupied"

        bid = book_one(room)
        return [room], bid

    # -----------------------------
    # BULK BOOKING
    # -----------------------------
    count = value
    if count < 1:
        return None, "Invalid count"

    # Preferred floor = first available room floor (if exists)
    free_rooms = available_rooms_sorted()
    preferred = floor_of(free_rooms[0]) if free_rooms else None

    rooms = book_multiple(count, preferred_floor=preferred)

    if len(rooms) < count:
        return None, "Not enough rooms available"

    bid = state["next_booking_id"]
    state["bookings"].append({"id": bid, "rooms": rooms})
    state["next_booking_id"] += 1
    return rooms, bid


# -------------------------------
# MODIFY
# -------------------------------
def vacate_booking(bid: int):
    state["bookings"] = [b for b in state["bookings"] if b["id"] != bid]

def reset_hotel():
    state["next_booking_id"] = 1
    state["bookings"] = []

def random_room():
    free = available_rooms_sorted()
    return random.choice(free) if free else None
