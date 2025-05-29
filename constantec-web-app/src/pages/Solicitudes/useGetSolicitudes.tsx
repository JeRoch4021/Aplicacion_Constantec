import { useQuery } from "@tanstack/react-query";
import axiosClient from "../../api/axiosClient";

const fetchSolicitudes = async () => {
  const { data } = await axiosClient.get("/users");
  return data;
};

export function useGetSolicitudes(idEstudiante) {
  return useQuery({
    queryKey: ['solicitudes'],
    queryFn: async () => {
      const { data } = await axiosClient.get(`/v1/solicitudes/${idEstudiante}`);
      return data;
    },
    enabled: !!idEstudiante
  });
}