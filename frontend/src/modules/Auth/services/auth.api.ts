import { api } from "../../../services/api";

export const AuthAPI = {
  login: (email: string, password: string) =>
    api.post("/auth/login", { email, password }),

  refresh: (refreshToken: string) =>
    api.post("/auth/refresh", { refresh_token: refreshToken }),
};
