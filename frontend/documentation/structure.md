# 📁 Project Structure Overview (Zustand Version)

This document explains the role of each folder in the React module‑based architecture using Zustand for state management.

---

## **src/**
Root directory containing all source code for the application.

---

## **app/**
Global application layer — responsible for wiring the entire app together.

- **store.js**  
  Optional global store setup (only if you have shared global state).  
  With Zustand, most state lives inside modules, so this file may be minimal or unused.

- **routes.jsx**  
  Central routing configuration for all modules.

- **providers.jsx**  
  Wraps the app with global providers (React Query, Theme, etc.).  
  Zustand does **not** require a provider.

This folder defines the *infrastructure* of the application.

---

## **modules/**
Each module is a self‑contained domain (tasks, auth, users, etc.).  
A module contains everything related to its domain.

### Example: `modules/tasks/`

- **components/**  
  UI components specific to the tasks domain  
  (e.g., `TaskCard`, `TaskForm`, `TaskList`).

- **hooks/**  
  Custom hooks for business logic  
  (e.g., `useTasks`).

- **services/**  
  API calls for this module  
  (e.g., `tasks.api.js`).

- **state/**  
  Zustand store for this module  
  (e.g., `tasks.store.js`).  
  This is where the module keeps its state, actions, and selectors.

- **utils/**  
  Helpers and utilities specific to tasks  
  (e.g., `task.helpers.js`).

- **pages/**  
  Screens/pages belonging to this module  
  (e.g., `TasksPage`, `TaskDetailsPage`).

- **index.js**  
  Optional entry point to export module parts cleanly.

### Other modules follow the same structure (e.g., `auth/`, `projects/`, etc.).

---

## **components/**
Global reusable UI components shared across modules.  
Not tied to any business domain.

Examples:  
- `Button.jsx`  
- `Modal.jsx`  
- `Input.jsx`

---

## **hooks/**
Global reusable hooks used across multiple modules.

Example:  
- `useFetch.js`

---

## **layouts/**
Page layout components that wrap multiple pages.

Examples:  
- `DashboardLayout.jsx`  
- `AuthLayout.jsx`

Useful for consistent structure across sections of the app.

---

## **services/**
Global API utilities.

- **api.js**  
  Axios instance + interceptors (token injection, refresh logic).

- **auth.js**  
  Optional global authentication helpers.

Shared across all modules.

---

## **utils/**
Global utilities not tied to any specific module.

Examples:  
- `date.js` — date formatting helpers  
- `validators.js` — form validation  
- `constants.js` — global constants

---

## **assets/**
Static files.

- **images/** — logos, illustrations  
- **icons/** — SVGs, icon sets  
- **styles/** — global CSS, variables, themes  
  - `globals.css`  
  - `variables.css`

---

## **index.js**
Application entry point.  
Mounts `<App />` into the DOM.

---
