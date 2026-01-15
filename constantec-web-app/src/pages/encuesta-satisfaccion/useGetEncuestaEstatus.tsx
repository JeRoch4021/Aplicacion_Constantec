import { useQuery } from '@tanstack/react-query'
import axiosClient from '../../api/axiosClient'

export const useGetEncuestaEstatus = (estudiante_id: number) => {
    return useQuery({
        queryKey: ['estadoComprobante', estudiante_id],
        queryFn: async () => {
            const { data } = await axiosClient.get(`/v1/encuestas/verificar/${estudiante_id}`);
            return data.completada as boolean; 
        },
        enabled: !!estudiante_id, // Solo ejecuta si existe el ID
        staleTime: Infinity, // La respuesta no cambia (si ya respondió, ya respondió)
    })
}