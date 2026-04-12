import { useEffect } from "react";
import { useAuthStore } from "../../auth/state/auth.store";
import { useTasksStore } from "../state/tasks.store";

export default function TasksPage() {
  const logout = useAuthStore((state) => state.logout);
  const tasks = useTasksStore((state) => state.tasks);
  const loading = useTasksStore((state) => state.loading);
  const error = useTasksStore((state) => state.error);
  const loadTasks = useTasksStore((state) => state.loadTasks);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  return (
    <main style={{ maxWidth: 920, margin: "2rem auto", padding: "0 1rem" }}>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h1>Tasks</h1>
        <button onClick={logout}>Logout</button>
      </header>

      {loading ? <p>Loading tasks...</p> : null}
      {error ? <p style={{ color: "crimson" }}>{error}</p> : null}

      <ul style={{ display: "grid", gap: "0.75rem", padding: 0, listStyle: "none" }}>
        {tasks.map((task) => (
          <li
            key={task.id}
            style={{ border: "1px solid #ddd", borderRadius: 8, padding: "0.75rem" }}
          >
            <strong>{task.title}</strong>
            <p style={{ margin: "0.25rem 0" }}>{task.description ?? "No description"}</p>
            <small>
              priority: {task.priority_id} | status: {task.status_id}
            </small>
          </li>
        ))}
      </ul>
    </main>
  );
}
