from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import booking_logic as logic

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/rooms/status")
def status():
    occupied = {}
    for b in logic.state["bookings"]:
        for r in b["rooms"]:
            occupied[r] = b["id"]

    result = {}
    for floor in range(1, 11):
        result[floor] = [
            {"room": r, "occupied": r in occupied, "booking_id": occupied.get(r)}
            for r in logic.ALL_ROOMS[floor]
        ]
    return result


@app.post("/book")
def book(value: int):
    rooms, bid = logic.commit_booking(value)
    if rooms is None:
        raise HTTPException(400, bid)
    return {"status": "booked", "booking_id": bid, "rooms": rooms}


@app.post("/vacate")
def vacate(bid: int):
    logic.vacate_booking(bid)
    return {"status": "vacated", "booking_id": bid}


@app.post("/reset")
def reset():
    logic.reset_hotel()
    return {"status": "reset"}


@app.post("/random")
def random():
    rm = logic.random_room()
    if rm is None:
        raise HTTPException(400, "No rooms available")
    rooms, bid = logic.commit_booking(rm)
    return {"status": "booked", "booking_id": bid, "rooms": rooms}


@app.get("/bookings")
def bookings():
    return logic.state["bookings"]
