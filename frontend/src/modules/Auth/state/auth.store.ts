import { create } from "zustand";
import { AuthAPI } from "../services/auth.api";

type AuthUser = {
  id: number;
  name: string;
  email: string;
  role?: string;
};

interface AuthState {
  user: AuthUser | null;
  accessToken: string | null;
  refreshToken: string | null;
  isHydrating: boolean;

  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refresh: () => Promise<void>;
  hydrate: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: null,
  refreshToken: localStorage.getItem("refresh_token"),
  isHydrating: false,

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
    if (!refreshToken) {
      throw new Error("Missing refresh token");
    }

    const res = await AuthAPI.refresh(refreshToken);

    set({
      accessToken: res.data.access_token,
      refreshToken: res.data.refresh_token,
    });

    if (res.data.refresh_token) {
      localStorage.setItem("refresh_token", res.data.refresh_token);
    }
  },

  logout: () => {
    const hasAccessToken = Boolean(get().accessToken);
    if (hasAccessToken) {
      AuthAPI.logout().catch(() => undefined);
    }
    set({ user: null, accessToken: null, refreshToken: null });
    localStorage.removeItem("refresh_token");
  },

  hydrate: async () => {
    set({ isHydrating: true });
    try {
      if (get().refreshToken) {
        await get().refresh();
      }
    } catch {
      set({ user: null, accessToken: null, refreshToken: null });
      localStorage.removeItem("refresh_token");
    } finally {
      set({ isHydrating: false });
    }
  },
}));
