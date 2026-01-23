const inputEl = document.getElementById("roomInput");
const gridEl = document.getElementById("hotelGrid");

async function loadStatus() {
  const res = await fetch(`/rooms/status`);
  const data = await res.json();
  renderGrid(data);
}

function renderGrid(data) {
  gridEl.innerHTML = "";

  for (let floor = 10; floor >= 1; floor--) {
    const row = document.createElement("div");
    row.className = "floor-row";

    const label = document.createElement("span");
    label.className = "floor-label";
    label.textContent = `Floor ${floor}`;
    row.appendChild(label);

    for (const cell of data[floor]) {
      const div = document.createElement("div");
      div.className = "room";
      div.textContent = cell.room;

      if (cell.occupied) {
        div.classList.add("occupied");
        div.onclick = () => vacatePopup(cell.booking_id, cell.room);
      }

      row.appendChild(div);
    }

    gridEl.appendChild(row);
  }
}

async function bookRoom() {
  let val = parseInt(inputEl.value);
  if (!val) {
    alert("Enter a value 1–5 (bulk) or >=100 (room)");
    return;
  }

  const res = await fetch(`/book?value=${val}`, { method: "POST" });
  const out = await res.json();

  if (!res.ok) {
    alert(out.detail || "Booking failed");
    return;
  }

  alert(`Allocated rooms: [${out.rooms.join(", ")}]`);
  loadStatus();
}

async function randomFill() {
  const res = await fetch(`/random`, { method: "POST" });
  const out = await res.json();
  alert(`Allocated random room: [${out.rooms.join(", ")}]`);
  loadStatus();
}

async function resetHotel() {
  await fetch(`/reset`, { method: "POST" });
  loadStatus();
  alert("Hotel reset");
}

async function vacatePopup(bid, room) {
  const ok = confirm(`Vacate booking #${bid}? (Room ${room})`);
  if (!ok) return;

  await fetch(`/vacate?bid=${bid}`, { method: "POST" });
  loadStatus();
}

loadStatus();
