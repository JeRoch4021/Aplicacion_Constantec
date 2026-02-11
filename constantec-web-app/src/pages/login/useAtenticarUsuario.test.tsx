import { beforeEach, describe, expect, it, vi } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react' // Needed for hooks
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { http, HttpResponse } from 'msw'
import { server } from '../../mocks/server'
import { useAutenticarUsuario } from './useAutenticarUsuario'

// Setup React Query for testing
const testQueryClient = () =>
  new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })

describe('<useAtenticarUsuario />', () => {
  let queryClient: QueryClient

  beforeEach(() => {
    queryClient = testQueryClient()
    vi.spyOn(Storage.prototype, 'setItem')
  })

  it('should save the token and student ID to localStorage on success', async () => {
    const mockData = { usuario: '123', password: 'test' }
    const mockToken = 'abc.eyJ0aXBvIjoidXNlciJ9.xyz'
    const mockId = '1'

    server.use(
      http.post('/v1/login/', () => {
        return HttpResponse.json({
          success: true,
          data: {
            token: mockToken,
            id_estudiante: mockId,
            tipo: 'estudiante',
          },
        })
      })
    )

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    )

    const { result } = renderHook(() => useAutenticarUsuario(), { wrapper })

    result.current.login(mockData)

    await waitFor(() => expect(result.current.status).toBe('success'))

    expect(localStorage.setItem).toHaveBeenCalledWith('token', mockToken)
    expect(localStorage.setItem).toHaveBeenCalledWith('id_estudiante', mockId)
    expect(localStorage.setItem).toHaveBeenCalledTimes(2)
  })

  it('should handle a 404 error when the user is not found', async () => {
    const mockData = { usuario: '123', password: '1234' }
    const mockResponse = { success: false, message: 'Usuario no encontrado' }
    const mockStatus = 404

    server.use(
      http.post('/v1/login/', () => {
        return HttpResponse.json(mockResponse, { status: mockStatus })
      })
    )

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    )

    const { result } = renderHook(() => useAutenticarUsuario(), { wrapper })

    result.current.login(mockData)

    await waitFor(() => expect(result.current.status).toBe('error'))

    expect(result.current.error?.response?.data).toEqual(mockResponse)
    expect(result.current.error?.response?.status).toEqual(mockStatus)
    expect(result.current.error).toBeDefined()
    expect(localStorage.setItem).not.toHaveBeenCalled()
  })
})
