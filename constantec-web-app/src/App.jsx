import {
  RouterProvider,
  createRootRoute,
  createRoute,
  createRouter,
  Outlet,
} from '@tanstack/react-router'
// import './App.css'
import { Login, Dashboard, Solicitudes } from './pages'

const rootRoute = createRootRoute({
  component: () => <Outlet />,
})

const LoginRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: Login,
})

const DashboardRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/dashboard',
  component: Dashboard,
})

const SolicitudesRoute = createRoute({
  path: '/solicitudes',
  getParentRoute: () => rootRoute,
  component: Solicitudes,
})

const routeTree = rootRoute.addChildren([
  LoginRoute,
  DashboardRoute,
  SolicitudesRoute,
])
const router = createRouter({ routeTree })

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  )
}

export default App
