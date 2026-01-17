const API_URL = "https://hotel-booking-233l.onrender.com";

let selectedBooking = null;

async function loadStatus() {
  try {
    const res = await fetch(`${API_URL}/rooms/status`);
    const data = await res.json();
    renderGrid(data);
  } catch (err) {
    console.error(err);
    alert("Backend unreachable!");
  }
}

function renderGrid(data) {
  const grid = document.getElementById("hotelGrid");
  grid.innerHTML = "";

  for (let floor = 10; floor >= 1; floor--) {
    const row = document.createElement("div");
    row.classList.add("floor-row");

    const label = document.createElement("span");
    label.classList.add("floor-label");
    label.innerText = `Floor ${floor}`;
    row.appendChild(label);

    for (let r of data[floor]) {
      const div = document.createElement("div");
      div.classList.add("room");
      div.innerText = r.room;

      if (r.occupied) {
        div.classList.add("occupied");
        div.onclick = () => openVacateModal(r.booking_id, r.room);
      }

      row.appendChild(div);
    }

    grid.appendChild(row);
  }
}

async function bookRoom() {
  const room = parseInt(document.getElementById("roomInput").value);
  if (!room) return alert("Enter room number");

  const res = await fetch(`${API_URL}/book?room=${room}`, { method: "POST" });
  if (!res.ok) {
    const msg = await res.json();
    alert(msg.detail);
  }
  await loadStatus();
}

async function randomFill() {
  await fetch(`${API_URL}/random`, { method: "POST" });
  await loadStatus();
}

async function resetHotel() {
  await fetch(`${API_URL}/reset`, { method: "POST" });
  await loadStatus();
}

function openVacateModal(bid, room) {
  selectedBooking = bid;
  document.getElementById("modalTitle").innerText = `Vacate Booking #${bid}?`;
  document.getElementById("modalRoom").innerText = `Room: ${room}`;
  document.getElementById("vacateModal").style.display = "flex";

  document.getElementById("confirmVacateBtn").onclick = async () => {
    await fetch(`${API_URL}/vacate?bid=${bid}`, { method: "POST" });
    closeModal();
    await loadStatus();
  };

  document.getElementById("cancelVacateBtn").onclick = closeModal;
}

function closeModal() {
  document.getElementById("vacateModal").style.display = "none";
}

loadStatus();
