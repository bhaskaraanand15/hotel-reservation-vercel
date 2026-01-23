from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from booking_logic import (
    room_exists, is_occupied, commit_booking,
    vacate_booking, reset_hotel, state, ALL_ROOMS,
    random_room
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/rooms/status")
def status():
    occupied_map = {}

    for b in state["bookings"]:
        for r in b["rooms"]:
            occupied_map[r] = b["id"]

    result = {}
    for floor in range(1, 11):
        result[floor] = [
            {
                "room": r,
                "occupied": r in occupied_map,
                "booking_id": occupied_map.get(r)
            }
            for r in ALL_ROOMS[floor]
        ]
    return result


@app.post("/book")
def book(value: int):
    rooms, bid_or_err = commit_booking(value)

    # Error case
    if rooms is None:
        raise HTTPException(400, bid_or_err)

    # Success
    return {
        "status": "booked",
        "booking_id": bid_or_err,
        "rooms": rooms
    }


@app.post("/vacate")
def vacate(bid: int):
    vacate_booking(bid)
    return {"status": "vacated", "booking_id": bid}


@app.post("/reset")
def reset():
    reset_hotel()
    return {"status": "reset"}


@app.post("/random")
def random_fill():
    rm = random_room()
    if rm is None:
        raise HTTPException(400, "No rooms available.")

    rooms, bid = commit_booking(rm)
    return {
        "status": "booked",
        "booking_id": bid,
        "rooms": rooms
    }


@app.get("/bookings")
def bookings():
    return state["bookings"]
