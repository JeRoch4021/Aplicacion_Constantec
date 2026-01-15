import { useQuery } from '@tanstack/react-query'
import axiosClient from '../../api/axiosClient'

export function useGetSolicitudes(estudiante_id) {
  return useQuery({
    queryKey: ['solicitudes'],
    queryFn: async () => {
      const { data } = await axiosClient.get(`/v1/solicitudes/${estudiante_id}`)
      return data
    },
    enabled: !!estudiante_id,
  })
}
