import { describe, expect, it, vi, beforeEach, afterAll } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Login } from './Login'

import * as UseAutenticarUsuario from './useAutenticarUsuario'
import { AxiosError, AxiosHeaders } from 'axios'

const useAutenticarUsuarioSpy = vi.spyOn(
  UseAutenticarUsuario,
  'useAutenticarUsuario'
)

describe('<Login />', () => {
  beforeEach(() => {
    // Use Vitest's built-in helper to mock the global 'location'
    // We cast to 'any' here just to satisfy the mock requirements
    vi.stubGlobal('location', {
      ...window.location, // Copy original properties
      href: '',
      assign: vi.fn(), // Mock common methods to avoid more errors
      replace: vi.fn(),
    })

    localStorage.clear()
    vi.spyOn(Storage.prototype, 'getItem')
  })

  afterAll(() => {
    // This automatically cleans up everything changed by stubGlobal
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('should render the login form', () => {
    useAutenticarUsuarioSpy.mockReturnValue({
      login: vi.fn(),
      loading: false,
      error: null,
      status: 'idle',
      response: undefined,
    })

    render(<Login />)

    expect(screen.getByAltText('Logo Tec')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Numero de Control')).toBeInTheDocument()
    expect(
      screen.getByPlaceholderText('Enter your password')
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Iniciar Sesión' })
    ).toBeInTheDocument()
  })

  it('should show error message when trying to login without user', () => {
    useAutenticarUsuarioSpy.mockReturnValue({
      login: vi.fn(),
      loading: false,
      error: null,
      status: 'idle',
      response: undefined,
    })

    render(<Login />)

    const loginButton = screen.getByRole('button', { name: /iniciar sesión/i })

    fireEvent.click(loginButton)

    expect(screen.getByText('Usuario Requerido')).toBeInTheDocument()
  })

  it('should show error message when trying to login without password', () => {
    useAutenticarUsuarioSpy.mockReturnValue({
      login: vi.fn(),
      loading: false,
      error: null,
      status: 'idle',
      response: undefined,
    })

    render(<Login />)

    const loginButton = screen.getByRole('button', { name: /iniciar sesión/i })
    const noControlInput = screen.getByPlaceholderText('Numero de Control')

    fireEvent.change(noControlInput, { target: { value: '123' } })

    fireEvent.click(loginButton)

    expect(screen.getByText('Password Requerido')).toBeInTheDocument()
  })

  it('should show error message coming from the API call fails', () => {
    const errorResponse = new AxiosError(
      undefined,
      undefined,
      undefined,
      undefined,
      {
        status: 404,
        data: { detail: 'Usuario no encontrado' },
        statusText: 'error',
        config: { headers: new AxiosHeaders() },
        headers: {},
      }
    )

    useAutenticarUsuarioSpy.mockReturnValue({
      login: vi.fn(),
      loading: false,
      error: errorResponse,
      status: 'error',
      response: undefined,
    })

    render(<Login />)

    const loginButton = screen.getByRole('button', { name: /iniciar sesión/i })
    const noControlInput = screen.getByPlaceholderText('Numero de Control')
    const passwordInput = screen.getByPlaceholderText('Enter your password')

    fireEvent.change(noControlInput, { target: { value: '123' } })
    fireEvent.change(passwordInput, { target: { value: 'test' } })
    fireEvent.click(loginButton)

    expect(screen.getByText('Usuario no encontrado')).toBeInTheDocument()
  })

  it('should redirect to admin page when user is an admin', () => {
    const mockToken = 'abc.eyJ0aXBvIjoiYWRtaW4ifQ.xyz'
    vi.spyOn(Storage.prototype, 'getItem').mockReturnValue(mockToken)

    useAutenticarUsuarioSpy.mockReturnValue({
      login: vi.fn(),
      loading: false,
      error: null,
      status: 'success',
      response: {
        success: true,
        message: 'login exitoso',
        error_code: null,
        data: {
          token: mockToken,
          id_estudiante: '1',
          tipo: 'admin',
        },
      },
    })

    render(<Login />)

    const loginButton = screen.getByRole('button', { name: /iniciar sesión/i })
    const noControlInput = screen.getByPlaceholderText('Numero de Control')
    const passwordInput = screen.getByPlaceholderText('Enter your password')

    fireEvent.change(noControlInput, { target: { value: '123' } })
    fireEvent.change(passwordInput, { target: { value: 'test' } })
    fireEvent.click(loginButton)

    expect(window.location.href).toBe(`/admin-access?token=${mockToken}`)
  })

  it('should redirect to student page when user is not an admin', () => {
    const mockToken = 'abc.eyJ0aXBvIjoidXNlciJ9.xyz'
    vi.spyOn(Storage.prototype, 'getItem').mockReturnValue(mockToken)

    useAutenticarUsuarioSpy.mockReturnValue({
      login: vi.fn(),
      loading: false,
      error: null,
      status: 'success',
      response: {
        success: true,
        message: 'login exitoso',
        error_code: null,
        data: {
          token: mockToken,
          id_estudiante: '1',
          tipo: 'estudiante',
        },
      },
    })

    render(<Login />)

    const loginButton = screen.getByRole('button', { name: /iniciar sesión/i })
    const noControlInput = screen.getByPlaceholderText('Numero de Control')
    const passwordInput = screen.getByPlaceholderText('Enter your password')

    fireEvent.change(noControlInput, { target: { value: '123' } })
    fireEvent.change(passwordInput, { target: { value: 'test' } })
    fireEvent.click(loginButton)

    expect(window.location.href).toBe('/dashboard')
  })
})
