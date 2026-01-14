import { useQuery } from '@tanstack/react-query'
import axiosClient from '../../api/axiosClient'

export const useGetEstadoComprobante = (no_control: string | undefined) => {
    return useQuery({
    queryKey: ['estadoComprobante', no_control],
    queryFn: async () => {
      const { data } = await axiosClient.get(`/v1/comprobantes/${no_control}`);
      return data; // Debe retornar { estado: 'APROBADO', motivo: '...' } etc.
    },
    enabled: !!no_control, // Solo se ejecuta si tenemos el no_control
    refetchInterval: 30000, // Opcional: consulta cada 30 segundos automáticamente
  });
};