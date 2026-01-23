import random

# Build hotel structure
ALL_ROOMS = {
    floor: (
        [1000 + i for i in range(1, 8)] if floor == 10
        else [floor * 100 + i for i in range(1, 11)]
    )
    for floor in range(1, 11)
}

# In-memory state (Vercel safe)
state = {
    "next_booking_id": 1,
    "bookings": []
}

def room_exists(room: int):
    return any(room in rooms for rooms in ALL_ROOMS.values())

def floor_of(room: int):
    if room >= 1000:
        return 10
    return room // 100

def get_occupied_rooms():
    occ = []
    for b in state["bookings"]:
        occ += b["rooms"]
    return occ

def is_occupied(room: int):
    return room in get_occupied_rooms()

def available_by_floor():
    occ = set(get_occupied_rooms())
    return {
        f: [r for r in ALL_ROOMS[f] if r not in occ]
        for f in ALL_ROOMS
    }

def book_single(room: int):
    bid = state["next_booking_id"]
    state["bookings"].append({"id": bid, "rooms": [room]})
    state["next_booking_id"] += 1
    return [room], bid

def book_bulk(count: int):
    free = available_by_floor()

    # 1. Try same floor contiguous clusters
    for floor in range(1, 11):
        frooms = free[floor]
        if len(frooms) >= count:
            return frooms[:count]

    # 2. Try group allocation minimizing travel distance
    best = None
    best_score = 1e9

    for start_floor in range(1, 11):
        candidate = []
        floors = list(range(start_floor, 0, -1)) + list(range(start_floor + 1, 11))
        floors = [start_floor] + floors

        for f in floors:
            for r in free[f]:
                if len(candidate) < count:
                    candidate.append(r)
            if len(candidate) == count:
                break

        if len(candidate) == count:
            rooms_sorted = sorted(candidate)
            floor_span = abs(floor_of(rooms_sorted[0]) - floor_of(rooms_sorted[-1]))
            room_span = max(rooms_sorted) - min(rooms_sorted)
            score = floor_span * 100 + room_span
            if score < best_score:
                best = candidate
                best_score = score

    return best or []

def commit_booking(value: int):
    if value >= 100:
        if not room_exists(value):
            return None, "Room does not exist"
        if is_occupied(value):
            return None, "Room occupied"
        return book_single(value)

    count = value
    rooms = book_bulk(count)
    if not rooms or len(rooms) < count:
        return None, "Not enough rooms"

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
    occ = set(get_occupied_rooms())
    available = [r for f in ALL_ROOMS for r in ALL_ROOMS[f] if r not in occ]
    return random.choice(available) if available else None
