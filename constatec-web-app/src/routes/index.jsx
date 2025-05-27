import {
    Login,
    Dashboard
} from '../pages'
import {
  RouterProvider,
  createRootRoute,
  createRoute,
  createRouter,
  redirect,
} from "@tanstack/react-router";

const rootRoute = createRootRoute({
  component: () => <RouterProvider router={router} />,
});

const loginRoute = createRoute({
  path: "/login",
  getParentRoute: () => rootRoute,
  component: Login,
});

// Protected: Dashboard Route
const dashboardRoute = createRoute({
  path: "/dashboard",
  getParentRoute: () => rootRoute,
  component: Dashboard,
});

// Build Route Tree
const routeTree = rootRoute.addChildren([loginRoute, dashboardRoute]);

// Create Router
export const router = createRouter({ routeTree });