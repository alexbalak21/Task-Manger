import { create } from "zustand";
import { AuthAPI } from "../services/auth.api";

interface AuthState {
  user: any | null;
  accessToken: string | null;
  refreshToken: string | null;

  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refresh: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: null,
  refreshToken: localStorage.getItem("refresh_token"),

  login: async (email, password) => {
    const res = await AuthAPI.login(email, password);

    set({
      user: res.data.user,
      accessToken: res.data.access_token,
      refreshToken: res.data.refresh_token,
    });

    localStorage.setItem("refresh_token", res.data.refresh_token);
  },

  refresh: async () => {
    const refreshToken = get().refreshToken;
    if (!refreshToken) return;

    const res = await AuthAPI.refresh(refreshToken);

    set({
      accessToken: res.data.access_token,
    });
  },

  logout: () => {
    set({ user: null, accessToken: null, refreshToken: null });
    localStorage.removeItem("refresh_token");
  },
}));
