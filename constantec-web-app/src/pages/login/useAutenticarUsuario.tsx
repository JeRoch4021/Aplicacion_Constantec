import { useMutation } from '@tanstack/react-query'
import axiosClient from '../../api/axiosClient'
import { AxiosError } from 'axios'

export type AutenticarPayload = {
  usuario: string;
  password: string;
}

type ApiErrorResponse = {
  detail: string;
}

type AutenticarResponse = {
    success: boolean;
    messsage: string;
    error_code: string | null;
    data: {
        token: string;
        id_estudiante: string;
        tipo: string;
    }
}

const autenticarUsuario = async (data: AutenticarPayload) => {
  const response = await axiosClient.post(
    '/v1/login/',
    data,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )
  console.log(response.data)
  if (response.data?.data?.token) {
      localStorage.setItem('token', response.data?.data?.token);
      localStorage.setItem('id_estudiante', response.data?.data?.id_estudiante);
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
