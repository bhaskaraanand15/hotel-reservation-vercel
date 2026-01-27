# api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import booking_logic as logic

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/rooms/status")
def status():
    """
    Returns structure:
    {
      1: [{room, occupied, booking_id}, ...],
      ...
      10: [...]
    }
    """
    occ = {}
    for b in logic.state["bookings"]:
        for r in b["rooms"]:
            occ[r] = b["id"]

    result = {}
    for floor in range(1, 11):
        result[floor] = [
            {
                "room": r,
                "occupied": r in occ,
                "booking_id": occ.get(r)
            }
            for r in logic.ALL_ROOMS[floor]
        ]
    return result


@app.post("/book")
def book(value: int):
    """
    Booking interpretation:
    - value >= 100 → book room number
    - value < 100 → bulk booking (count)
    """
    rooms, bid_or_err = logic.commit_booking(value)

    if rooms is None:
        raise HTTPException(status_code=400, detail=bid_or_err)

    return {
        "status": "booked",
        "booking_id": bid_or_err,
        "rooms": rooms
    }


@app.post("/vacate")
def vacate(bid: int):
    logic.vacate(bid)
    return {"status": "vacated", "booking_id": bid}


@app.post("/reset")
def reset():
    logic.reset()
    return {"status": "reset"}


@app.post("/random")
def random():
    r = logic.random_room()
    if r is None:
        raise HTTPException(status_code=400, detail="No rooms available")

    rooms, bid = logic.commit_booking(r)
    return {"status": "booked", "booking_id": bid, "rooms": rooms}


@app.get("/bookings")
def bookings():
    return logic.state["bookings"]
