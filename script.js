// script.js

async function loadStatus() {
  const res = await fetch("/rooms/status");
  if (!res.ok) return alert("Backend error (status)");
  const data = await res.json();
  renderGrid(data);
}

function renderGrid(data) {
  const grid = document.getElementById("hotelGrid");
  grid.innerHTML = "";

  for (let floor = 10; floor >= 1; floor--) {
    const row = document.createElement("div");
    row.className = "floor-row";

    const label = document.createElement("span");
    label.className = "floor-label";
    label.textContent = `Floor ${floor}`;
    row.appendChild(label);

    for (let r of data[floor]) {
      const div = document.createElement("div");
      div.className = "room";
      div.textContent = r.room;

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
  const val = document.getElementById("roomInput").value.trim();
  if (!val) return alert("Enter a number");

  const num = parseInt(val);
  if (isNaN(num)) return alert("Invalid number");

  const res = await fetch(`/book?value=${num}`, { method: "POST" });
  if (!res.ok) {
    const e = await res.json();
    alert(e.detail);
    return;
  }

  await loadStatus();
}


async function randomFill() {
  const res = await fetch(`/random`, { method: "POST" });
  if (!res.ok) {
    const e = await res.json();
    alert(e.detail);
    return;
  }
  await loadStatus();
}


async function resetHotel() {
  await fetch(`/reset`, { method: "POST" });
  await loadStatus();
}


// === VACATE MODAL ===

let selectedBid = null;

function openVacateModal(bid, room) {
  selectedBid = bid;
  document.getElementById("modalTitle").textContent = `Vacate Booking #${bid}?`;
  document.getElementById("modalRoom").textContent = `Room: ${room}`;
  document.getElementById("vacateModal").style.display = "flex";
}

document.getElementById("confirmVacateBtn").onclick = async () => {
  await fetch(`/vacate?bid=${selectedBid}`, { method: "POST" });
  closeModal();
  await loadStatus();
};

document.getElementById("cancelVacateBtn").onclick = closeModal;

function closeModal() {
  document.getElementById("vacateModal").style.display = "none";
  selectedBid = null;
}


// Initial load
loadStatus();
