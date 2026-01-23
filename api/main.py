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
    occ = {}
    for b in logic.state["bookings"]:
        for r in b["rooms"]:
            occ[r] = b["id"]

    return {
        f: [
            {"room": r, "occupied": r in occ, "booking_id": occ.get(r)}
            for r in logic.ALL_ROOMS[f]
        ]
        for f in range(1, 11)
    }

@app.post("/book")
def book(value: int):
    rooms, bid_or_err = logic.commit_booking(value)
    if rooms is None:
        raise HTTPException(400, bid_or_err)
    return {"status": "booked", "booking_id": bid_or_err, "rooms": rooms}

@app.post("/vacate")
def vacate(bid: int):
    logic.vacate(bid)
    return {"status": "vacated"}

@app.post("/reset")
def reset():
    logic.reset()
    return {"status": "reset"}

@app.post("/random")
def random():
    r = logic.random_room()
    if r is None:
        raise HTTPException(400, "No rooms free")
    rooms, bid = logic.commit_booking(r)
    return {"status": "booked", "booking_id": bid, "rooms": rooms}

@app.get("/bookings")
def bookings():
    return logic.state["bookings"]
