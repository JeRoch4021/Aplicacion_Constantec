import {
  RouterProvider,
  createRootRoute,
  createRoute,
  createRouter,
  Outlet,
  redirect,
} from '@tanstack/react-router'
import { Login, Dashboard } from './pages'

const isAuthenticated = () => {
  return !!localStorage.getItem('token')
}

const rootRoute = createRootRoute({
  component: () => <Outlet />,
})

const LoginRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: Login,
  beforeLoad: () => {
    if (isAuthenticated()) {
      throw redirect({ to: '/dashboard' })
    }
  },
})

const DashboardRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/dashboard',
  component: Dashboard,
  beforeLoad: () => {
    if (!isAuthenticated()) {
      throw redirect({ to: '/' })
    }
  },
})

const routeTree = rootRoute.addChildren([LoginRoute, DashboardRoute])

const router = createRouter({ routeTree })

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  )
}

export default App
