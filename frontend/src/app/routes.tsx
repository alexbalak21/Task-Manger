import { BrowserRouter, Route, Routes } from "react-router";
import TasksPage from "../modules/Tasks/pages/TasksPage";
import LoginPage from "../modules/auth/pages/LoginPage";

export function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/tasks" element={<TasksPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </BrowserRouter>
  );
}
