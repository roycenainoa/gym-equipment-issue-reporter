// Thin API client for the backend. The base URL is configurable via the
// VITE_API_URL build/runtime variable so the same frontend works locally and
// when deployed to the cloud. Defaults to the local backend port.
// VITE_API_URL may be a full URL (local dev) or a bare hostname (some hosts
// inject just the host); ensure a protocol is always present.
const RAW = import.meta.env.VITE_API_URL || "http://localhost:8000";
const BASE_URL = /^https?:\/\//.test(RAW) ? RAW : `https://${RAW}`;

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (body.detail) detail = typeof body.detail === "string" ? body.detail : detail;
    } catch {
      /* ignore non-JSON error bodies */
    }
    throw new Error(detail);
  }
  return res.json();
}

export const getEquipment = () => request("/equipment");
export const getTickets = () => request("/tickets");
export const createTicket = (equipmentId, description) =>
  request("/tickets", {
    method: "POST",
    body: JSON.stringify({ equipment_id: equipmentId, description }),
  });
export const updateTicketStatus = (ticketId, status) =>
  request(`/tickets/${ticketId}`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
