import { useMutation } from '@tanstack/react-query'
import axiosClient from '../../api/axiosClient'
import { AxiosError } from 'axios'

export type SolicitudPayload = {
  descripcion: string
  otros: string
  id_estudiante: string
  constancia_opciones: string[]
}

const createSolicitud = async (data: SolicitudPayload) => {
  const response = await axiosClient.post(
    'http://localhost:8000/v1/solicitudes/',
    data,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )

  return response.data
}

type FastApiErrorResponse = {
  detail: string
}

export const useCrearSoliciutd = () => {
  const {
    mutate,
    error,
    isPending: loading,
    data: response,
    ...rest
  } = useMutation<any, AxiosError<FastApiErrorResponse>, SolicitudPayload>({
    mutationFn: (data: SolicitudPayload) => createSolicitud(data),
  })

  const crearSolicitud = (request: SolicitudPayload) => {
    mutate(request)
  }

  return { ...rest, crearSolicitud, loading, error, response }
}
