import { useEffect, useState } from "react";
import { getEquipment, createTicket } from "../api.js";

// Member-facing view (FR-01, FR-02, FR-03): browse equipment and submit a
// validated maintenance ticket.
export default function MemberView() {
  const [equipment, setEquipment] = useState([]);
  const [equipmentId, setEquipmentId] = useState("");
  const [description, setDescription] = useState("");
  const [feedback, setFeedback] = useState(null); // { type, message }
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    getEquipment()
      .then(setEquipment)
      .catch((err) => setFeedback({ type: "error", message: err.message }));
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setFeedback(null);

    // Client-side guard mirroring the backend's FR-03 validation.
    if (!equipmentId) {
      setFeedback({ type: "error", message: "Please select a piece of equipment." });
      return;
    }
    if (description.trim().length < 5) {
      setFeedback({ type: "error", message: "Please describe the issue (at least 5 characters)." });
      return;
    }

    setSubmitting(true);
    try {
      await createTicket(Number(equipmentId), description.trim());
      setFeedback({ type: "success", message: "Thanks! Your report has been submitted." });
      setEquipmentId("");
      setDescription("");
    } catch (err) {
      setFeedback({ type: "error", message: err.message });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="rounded-lg bg-white p-6 shadow">
      <h2 className="mb-1 text-xl font-semibold">Report a Faulty Machine</h2>
      <p className="mb-5 text-sm text-slate-500">
        Found something broken? Let the maintenance team know.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="equipment" className="mb-1 block text-sm font-medium">
            Equipment
          </label>
          <select
            id="equipment"
            value={equipmentId}
            onChange={(e) => setEquipmentId(e.target.value)}
            className="w-full rounded-md border border-slate-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
          >
            <option value="">Select equipment…</option>
            {equipment.map((item) => (
              <option key={item.id} value={item.id}>
                {item.name} — {item.location}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="description" className="mb-1 block text-sm font-medium">
            Describe the issue
          </label>
          <textarea
            id="description"
            rows={4}
            maxLength={500}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="e.g. The treadmill belt slips when running above 10 km/h."
            className="w-full rounded-md border border-slate-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
          />
          <p className="mt-1 text-right text-xs text-slate-400">{description.length}/500</p>
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="rounded-md bg-blue-600 px-5 py-2 font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {submitting ? "Submitting…" : "Submit Report"}
        </button>
      </form>

      {feedback && (
        <p
          className={`mt-4 rounded-md px-4 py-2 text-sm ${
            feedback.type === "success"
              ? "bg-green-100 text-green-800"
              : "bg-red-100 text-red-800"
          }`}
        >
          {feedback.message}
        </p>
      )}
    </section>
  );
}
