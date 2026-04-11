# 🏗️ Application Architecture (React + Modules + Zustand)

This document describes the architecture of the application, including folder structure, module organization, state management, authentication flow, and global infrastructure.

The goal is to provide a scalable, maintainable, and domain-driven structure suitable for large React applications.

---

## 1. 📁 Folder Structure Overview

```txt
src/
│
├── app/
│   ├── App.tsx
│   ├── routes.tsx
│   ├── providers.tsx
│   └── store.ts (optional)
│
├── modules/
│   ├── auth/
│   ├── tasks/
│   └── ...other modules
│
├── components/
├── hooks/
├── layouts/
├── services/
├── utils/
├── assets/
└── index.tsx
```

Each folder has a clear responsibility and avoids mixing concerns.

---

## 2. 🧩 Module-Based Architecture

Modules represent domains of the application (auth, tasks, users, projects, and more).

Each module is self-contained:

```txt
modules/<module>/
│
├── components/   -> UI components for this domain
├── hooks/        -> domain-specific logic hooks
├── services/     -> API calls for this domain
├── state/        -> Zustand store for this domain
├── utils/        -> helpers for this domain
└── pages/        -> screens for this domain
```

This structure ensures:

- High cohesion
- Low coupling
- Easy scalability
- Clear ownership of logic

---

## 3. ⚙️ Global App Layer (app/)

The `app/` folder contains the infrastructure of the application.

### App.tsx

Root component that composes providers and routes.

### routes.tsx

Central routing configuration. Modules plug their pages here.

### providers.tsx

Wraps the app with global providers:

- React Query (optional)
- Theme provider
- Error boundaries
- Any global context

Zustand does not require a provider.

### store.ts

Optional global store (only if needed). Most state lives inside modules.

---

## 4. 🔐 Authentication Architecture (JWT + Refresh Token)

The API returns:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "user": { "id": 1, "name": "John Doe", "role": "admin" }
}
```

The app implements:

- Zustand auth store
- Login
- Auto-refresh on 401
- Token injection via Axios
- Logout on refresh failure
- Protected routes

Token storage strategy:

| Token | Storage | Reason |
|---|---|---|
| access_token | memory (Zustand) | Safest, helps reduce XSS risk |
| refresh_token | localStorage | Needed across sessions |

---

## 5. 🧠 Zustand State Management

Each module has its own store:

```txt
modules/auth/state/auth.store.ts
modules/tasks/state/tasks.store.ts
```

Zustand benefits:

- No provider
- No reducers
- No boilerplate
- Minimal re-renders
- Perfect for domain-scoped state

Example (auth):

```ts
import { create } from "zustand";

type AuthState = {
  user: { id: number; name: string; role: string } | null;
  accessToken: string | null;
  refreshToken: string | null;
  login: (email: string, password: string) => Promise<void>;
  refresh: () => Promise<void>;
  logout: () => void;
};

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: null,
  refreshToken: localStorage.getItem("refresh_token"),

  login: async (email, password) => {
    // login implementation
  },
  refresh: async () => {
    // refresh implementation
  },
  logout: () => {
    // logout implementation
  },
}));
```

---

## 6. 🌐 Global API Layer (services/api.ts)

A single Axios instance handles:

- Base URL
- Token injection
- Auto-refresh
- Retry failed requests

### Request interceptor

Adds `Authorization: Bearer <token>` to every request.

### Response interceptor

If API returns 401:

- Refresh token
- Retry original request
- Logout if refresh fails

This makes authentication transparent to all modules.

---

## 7. 🛡️ Protected Routes

`modules/auth/components/ProtectedRoute.tsx` ensures only authenticated users can access certain pages.

Example:

```tsx
<Route
  path="/tasks"
  element={
    <ProtectedRoute>
      <TasksPage />
    </ProtectedRoute>
  }
/>
```

Role-based access can be added easily.

---

## 8. 🧩 How Modules Use Auth

Any module can access auth via:

```ts
import { useAuth } from "../../auth/hooks/useAuth";
```

Modules can:

- Read user info
- Check roles
- Trigger logout
- Rely on auto-token injection
- Make authenticated API calls without handling tokens

---

## 9. 🎨 Global Shared Layers

### components/

Reusable UI components (`Button`, `Modal`, `Input`, and others).

### hooks/

Reusable logic hooks (`useFetch`, `useDebounce`, and others).

### layouts/

Page wrappers (`DashboardLayout`, `AuthLayout`, and others).

### services/

Global utilities (Axios instance, auth helpers).

### utils/

Global helpers (date formatting, validators, constants).

### assets/

Images, icons, and global styles.
