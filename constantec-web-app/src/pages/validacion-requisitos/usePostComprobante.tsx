import { useMutation, useQueryClient } from '@tanstack/react-query'
import axiosClient from '../../api/axiosClient'

interface UploadResponse {
  mensaje: string
  estado: string
}

export const usePostComprobante = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (formData: FormData) => {
      // Es vital configurar el header como multipart/form-data
      const { data } = await axiosClient.post<UploadResponse>(
        '/v1/comprobantes/factura',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      )
      return data
    },
    onSuccess: () => {
      // Invalidamos la caché del perfil para que se actualice el estado visualmente
      queryClient.invalidateQueries({ queryKey: ['perfil de estudiante'] })
    },
  })
}
