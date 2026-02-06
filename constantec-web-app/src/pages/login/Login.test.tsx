import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Login } from './Login'

import * as UseAutenticarUsuario from './useAutenticarUsuario'

const useAutenticarUsuarioSpy = vi.spyOn(
  UseAutenticarUsuario,
  'useAutenticarUsuario'
)

describe('<Login />', () => {
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

  it('should show succesful message when the username and password are correct', async () => {
    const mockLogin = vi.fn()
    
    useAutenticarUsuarioSpy.mockReturnValue({
      login: mockLogin,
      loading: false,
      error: null,
      status: 'idle',
      response: { 
        data: {"token": '22240000', "id_estudiante": '1', "tipo": 'estudiante'}, 
        success: true, 
        message: "autenticacion exitosa", 
        error_code: null },
    })

    render(<Login />)

    const loginButton = screen.getByRole('button', { name: /iniciar sesión/i })
    const noControlInput = screen.getByPlaceholderText('Numero de Control')
    const passwordInput = screen.getByPlaceholderText('Enter your password')

    fireEvent.change(noControlInput, { target: { value: '123' } })
    fireEvent.change(passwordInput, { target: { value: 'test' } })
    fireEvent.click(loginButton)

    const successMsg = await screen.findByText(/autenticacion exitosa/i)
    expect(successMsg).toBeInTheDocument()
  })
})
