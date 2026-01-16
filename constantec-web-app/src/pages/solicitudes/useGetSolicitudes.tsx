import { useQuery } from '@tanstack/react-query'
import axiosClient from '../../api/axiosClient'

export function useGetSolicitudes(id_estudiante) {
  return useQuery({
    queryKey: ['solicitudes'],
    queryFn: async () => {
      const { data } = await axiosClient.get(`/v1/solicitudes/${id_estudiante}`)
      return data
    },
    enabled: !!id_estudiante,
  })
}
