import { BrowserRouter, Navigate, Route, Routes } from "react-router";
import type { ReactNode } from "react";
import TasksPage from "../modules/Tasks/pages/TasksPage";
import LoginPage from "../modules/auth/pages/LoginPage";
import { useAuthStore } from "../modules/auth/state/auth.store";

function ProtectedRoute({ children }: { children: ReactNode }) {
  const accessToken = useAuthStore((state) => state.accessToken);
  const isHydrating = useAuthStore((state) => state.isHydrating);

  if (isHydrating) {
    return <div>Loading session...</div>;
  }

  if (!accessToken) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

export function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/tasks"
          element={
            <ProtectedRoute>
              <TasksPage />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<LoginPage />} />
        <Route path="*" element={<Navigate to="/tasks" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
