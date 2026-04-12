import { create } from "zustand";
import { TasksAPI, type TaskDto } from "../services/tasks.api";

type TasksState = {
  tasks: TaskDto[];
  loading: boolean;
  error: string | null;
  loadTasks: () => Promise<void>;
};

export const useTasksStore = create<TasksState>((set) => ({
  tasks: [],
  loading: false,
  error: null,

  loadTasks: async () => {
    set({ loading: true, error: null });
    try {
      const response = await TasksAPI.getAll();
      set({ tasks: response.data, loading: false });
    } catch {
      set({ error: "Could not load tasks", loading: false });
    }
  },
}));
