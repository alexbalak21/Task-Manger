import axios from "axios";
import type { AxiosError, InternalAxiosRequestConfig } from "axios";
import { useAuthStore } from "../modules/auth/state/auth.store";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// Attach token
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auto refresh
api.interceptors.response.use(
  (res) => res,
  async (error: AxiosError) => {
    const original = error.config as
      | (InternalAxiosRequestConfig & { _retry?: boolean })
      | undefined;

    if (!original) {
      return Promise.reject(error);
    }

    const isRefreshCall = original.url?.includes("/api/auth/refresh");
    if (error.response?.status === 401 && !original._retry && !isRefreshCall) {
      original._retry = true;

      try {
        await useAuthStore.getState().refresh();
        return api(original);
      } catch {
        useAuthStore.getState().logout();
      }
    }

    return Promise.reject(error);
  }
);
