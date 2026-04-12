import { api } from "../../../services/api.ts";

export type TaskDto = {
  id: number;
  title: string;
  description: string | null;
  priority_id: number;
  status_id: number;
  due_date: string | null;
  created_at: string | null;
  updated_at: string | null;
};

export const TasksAPI = {
  getAll: () => api.get<TaskDto[]>("/api/tasks"),
};
