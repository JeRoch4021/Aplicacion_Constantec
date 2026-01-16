import { useQuery } from '@tanstack/react-query'
import axiosClient from '../../api/axiosClient'

export const useGetEncuestaEstatus = (id_estudiante: number) => {
    return useQuery({
        queryKey: ['estadoComprobante', id_estudiante],
        queryFn: async () => {
            const { data } = await axiosClient.get(`/v1/encuestas/verificar/${id_estudiante}`);
            return data.completada as boolean; 
        },
        enabled: !!id_estudiante, // Solo ejecuta si existe el ID
        staleTime: Infinity, // La respuesta no cambia (si ya respondió, ya respondió)
    })
}