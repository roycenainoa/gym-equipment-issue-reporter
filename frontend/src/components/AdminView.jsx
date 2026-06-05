import { useEffect, useState } from "react";
import { getTickets, updateTicketStatus } from "../api.js";

const STATUSES = ["Open", "In Progress", "Resolved"];

const statusStyle = {
  Open: "bg-red-100 text-red-800",
  "In Progress": "bg-amber-100 text-amber-800",
  Resolved: "bg-green-100 text-green-800",
};

// Administrator dashboard (FR-04, FR-05): view all tickets and update statuses.
export default function AdminView() {
  const [tickets, setTickets] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  function load() {
    setLoading(true);
    getTickets()
      .then(setTickets)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }

  useEffect(load, []);

  async function handleStatusChange(ticketId, status) {
    setError(null);
    try {
      const updated = await updateTicketStatus(ticketId, status);
      setTickets((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
    } catch (err) {
      setError(err.message);
    }
  }

  const formatDate = (iso) => new Date(iso).toLocaleString();

  return (
    <section className="rounded-lg bg-white p-6 shadow">
      <div className="mb-5 flex items-center justify-between">
        <h2 className="text-xl font-semibold">Maintenance Tickets</h2>
        <button
          onClick={load}
          className="rounded-md border border-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50"
        >
          Refresh
        </button>
      </div>

      {error && (
        <p className="mb-4 rounded-md bg-red-100 px-4 py-2 text-sm text-red-800">{error}</p>
      )}

      {loading ? (
        <p className="text-sm text-slate-500">Loading…</p>
      ) : tickets.length === 0 ? (
        <p className="text-sm text-slate-500">No tickets reported yet.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-200 text-slate-500">
              <tr>
                <th className="px-3 py-2">Equipment</th>
                <th className="px-3 py-2">Issue</th>
                <th className="px-3 py-2">Reported</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Update</th>
              </tr>
            </thead>
            <tbody>
              {tickets.map((ticket) => (
                <tr key={ticket.id} className="border-b border-slate-100 align-top">
                  <td className="px-3 py-3 font-medium">{ticket.equipment.name}</td>
                  <td className="px-3 py-3 text-slate-600">{ticket.description}</td>
                  <td className="px-3 py-3 whitespace-nowrap text-slate-500">
                    {formatDate(ticket.created_at)}
                  </td>
                  <td className="px-3 py-3">
                    <span
                      className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium ${statusStyle[ticket.status]}`}
                    >
                      {ticket.status}
                    </span>
                  </td>
                  <td className="px-3 py-3">
                    <select
                      value={ticket.status}
                      onChange={(e) => handleStatusChange(ticket.id, e.target.value)}
                      className="rounded-md border border-slate-300 px-2 py-1 text-sm focus:border-blue-500 focus:outline-none"
                    >
                      {STATUSES.map((s) => (
                        <option key={s} value={s}>
                          {s}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
