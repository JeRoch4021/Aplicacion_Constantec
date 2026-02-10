import { describe, expect, it, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react' // Needed for hooks
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useAutenticarUsuario } from './useAutenticarUsuario'
import axiosClient from '../../api/axiosClient'

vi.mock('../../api/axiosClient', () => ({
  default: {
    post: vi.fn(),
  },
}))

// Setup React Query for testing
const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
})
const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
)

describe('<useAtenticarUsuario />', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
    vi.spyOn(Storage.prototype, 'setItem')
  })

  it('should save the token and student ID to localStorage on success', async () => {
    const mockData = { usuario: '123', password: 'test' }
    const mockToken = 'abc.eyJ0aXBvIjoidXNlciJ9.xyz'
    const mockId = '1'

    const mockResponse = {
      data: {
        data: {
          token: mockToken,
          id_estudiante: mockId,
          tipo: 'estudiante',
        },
      },
    }

    ;(axiosClient.post as any).mockResolvedValue(mockResponse)

    const { result } = renderHook(() => useAutenticarUsuario(), { wrapper })
    result.current.login(mockData)

    await waitFor(() => {
      expect(localStorage.setItem).toHaveBeenCalledWith('token', mockToken)
    })
    expect(localStorage.setItem).toHaveBeenCalledWith('id_estudiante', mockId)
    expect(localStorage.setItem).toHaveBeenCalledTimes(2)
  })
})
