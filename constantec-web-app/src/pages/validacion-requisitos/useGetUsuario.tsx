import { useQuery } from '@tanstack/react-query'
import axiosClient from '../../api/axiosClient'

export function getNoControlDeToken() {
  const token = localStorage.getItem('token')
  if (!token) return null
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.sub
  } catch {
    return null
  }
}

export function useGetUsuario() {
  const no_control = getNoControlDeToken()

  return useQuery({
    queryKey: ['perfil de estudiante', no_control],
    queryFn: async () => {
      const { data } = await axiosClient.get(`/v1/estudiantes/${no_control}`)
      return data
    },
    enabled: !!no_control,
  })
}
