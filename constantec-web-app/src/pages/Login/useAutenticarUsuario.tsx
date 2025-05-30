import { useMutation } from '@tanstack/react-query'
import axiosClient from '../../api/axiosClient'
import { AxiosError } from 'axios'

export type AutenticarPayload = {
  no_control: string
  contrasena: string
}

type ApiErrorResponse = {
  detail: string
}

type AutenticarResponse = {
    success: boolean,
    messsage: string,
    error_code: string | null
    data: string
}

const autenticarUsuario = async (data: AutenticarPayload) => {
  const response = await axiosClient.post(
    'http://localhost:8000/v1/login/',
    data,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )
  console.log(response.data)
  if (response.data?.data?.token) {
      localStorage.setItem('token', response.data?.data?.token)
  }
  return response.data
}

export const useAutenticarUsuario = () => {
  const {
    mutate,
    error,
    isPending: loading,
    data: response,
    ...rest
  } = useMutation<AutenticarResponse, AxiosError<ApiErrorResponse>, AutenticarPayload>({
    mutationFn: (data: AutenticarPayload) => autenticarUsuario(data),
  })

  const login = (request: AutenticarPayload) => {
    mutate(request)
  }

  return { ...rest, login, loading, error, response }
}
