import { useState } from "react";
import MemberView from "./components/MemberView.jsx";
import AdminView from "./components/AdminView.jsx";

// Two roles share one app, toggled by a simple tab control: members report
// issues, administrators track and update them.
export default function App() {
  const [view, setView] = useState("member");

  const tabClass = (active) =>
    `px-4 py-2 text-sm font-medium rounded-md transition-colors ${
      active ? "bg-white text-blue-700 shadow" : "text-blue-100 hover:bg-blue-500"
    }`;

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800">
      <header className="bg-blue-600 text-white">
        <div className="mx-auto max-w-4xl px-4 py-4 sm:flex sm:items-center sm:justify-between">
          <h1 className="text-lg font-semibold">🏋️ Gym Equipment Issue Reporter</h1>
          <nav className="mt-3 flex gap-2 sm:mt-0">
            <button className={tabClass(view === "member")} onClick={() => setView("member")}>
              Report an Issue
            </button>
            <button className={tabClass(view === "admin")} onClick={() => setView("admin")}>
              Admin Dashboard
            </button>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-4 py-6">
        {view === "member" ? <MemberView /> : <AdminView />}
      </main>
    </div>
  );
}
