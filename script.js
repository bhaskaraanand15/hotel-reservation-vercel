const API = "/api";

async function loadStatus() {
  const res = await fetch(`${API}/rooms/status`);
  const data = await res.json();
  renderGrid(data);
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
  const val = parseInt(document.getElementById("roomInput").value);
  if (!val) return alert("Enter value");

  const res = await fetch(`${API}/book?value=${val}`, { method: "POST" });
  if (!res.ok) {
    alert((await res.json()).detail);
  }
  loadStatus();
}

async function randomFill() {
  await fetch(`${API}/random`, { method: "POST" });
  loadStatus();
}

async function resetHotel() {
  await fetch(`${API}/reset`, { method: "POST" });
  loadStatus();
}

function openVacateModal(bid, room) {
  document.getElementById("modalTitle").innerText = `Vacate Booking #${bid}`;
  document.getElementById("modalRoom").innerText = `Room: ${room}`;
  document.getElementById("vacateModal").style.display = "flex";

  document.getElementById("confirmVacateBtn").onclick = async () => {
    await fetch(`${API}/vacate?bid=${bid}`, { method: "POST" });
    closeModal();
    loadStatus();
  };

  document.getElementById("cancelVacateBtn").onclick = closeModal;
}

function closeModal() {
  document.getElementById("vacateModal").style.display = "none";
}

loadStatus();
