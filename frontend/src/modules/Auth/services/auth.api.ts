import { api } from "../../../services/api.ts";

export const AuthAPI = {
  login: (email: string, password: string) =>
    api.post("/api/auth/login", { email, password }),

  refresh: (refreshToken: string) =>
    api.post("/api/auth/refresh", { refresh_token: refreshToken }),

  logout: () => api.post("/api/auth/logout"),
};
