// Thin API client for the backend. The base URL is configurable via the
// VITE_API_URL build/runtime variable so the same frontend works locally and
// when deployed to the cloud. Defaults to the local backend port.
// VITE_API_URL controls where API calls go:
//   undefined        -> local dev default (separate backend on :8000)
//   "" (empty)       -> same-origin / relative (backend serves this build)
//   full URL or host -> use as-is (prepend https:// if only a host is given)
const RAW = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const BASE_URL =
  RAW === "" ? "" : /^https?:\/\//.test(RAW) ? RAW : `https://${RAW}`;

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
