import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import axiosClient from '../../api/axiosClient'
import {
  Box,
  Text,
  TextArea,
  Button,
  CheckboxCards,
  Flex,
} from '@radix-ui/themes'

export const createSolicitud = async (data) => {
  const res = await axiosClient.post('/solicitudes', data)
  return res.data
}

export const SolicitudFormulario = () => {
    const [opciones, setOpciones] = useState<Array<string>>([]);
    const [descripcion, setDescripcion] = useState<string>("");
    const [otros, setOtros] = useState<string>("");
  const queryClient = useQueryClient()
  const [formData, setFormData] = useState({
    estudiantes_id: '',
    constancia_id: '',
    solicitud_estatus_id: 1,
    fecha_solicitud: '',
    fecha_entrega: null,
  })

  //   const mutation = useMutation(createSolicitud, {
  //     onSuccess: () => {
  //       queryClient.invalidateQueries(["solicitudes"]);
  //     },
  //   });

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // mutation.mutate(formData);
  }

  const seleccionarOpcion = (value: string) => {
    const nuevasOpciones= opciones.includes(value) ? opciones.filter((item) => item !== value) : [...opciones, value];
    setOpciones(nuevasOpciones)
  }

    console.log(opciones)

  return (
    <Box width="700px" mt="3">
      <form onSubmit={handleSubmit} className="flex flex-col gap-2 max-w-md">
        <Text size="3" weight="bold">
          Descripcion
        </Text>
        <TextArea placeholder="Descripcion de la constancia" mt="2" onChange={(e) => { 
            e.preventDefault();
            setDescripcion(e?.target?.value.trim())
        }}/>
        <Box mt="2" mb="2">
          <CheckboxCards.Root
            defaultValue={[]}
            value={opciones || []}
            columns={{ initial: '1', sm: '3' }}
          >
            <CheckboxCards.Item value="1" onClick={() => { seleccionarOpcion("1") }}>
              <Text weight="bold">Inscritos</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item value="2" onClick={() => { seleccionarOpcion("2") }}>
              <Text weight="bold">Kardex</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item value="3" onClick={() => { seleccionarOpcion("3") }}>
              <Text weight="bold">Seguro Social</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item value="4" onClick={() => { seleccionarOpcion("4") }}>
              <Text weight="bold">Calificaciones del Semestre Anterior</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item value="5" onClick={() => { seleccionarOpcion("5") }}>
              <Text weight="bold">
                Calificaciones de Dos Semestres Anteriores
              </Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item value="6" onClick={() => { seleccionarOpcion("6") }}>
              <Text weight="bold">Egreso</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item value="7" onClick={() => { seleccionarOpcion("7") }}>
              <Text weight="bold">Título en Trámite</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item value="8" onClick={() => { seleccionarOpcion("8") }}>
              <Text weight="bold">Pago</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item value="9" onClick={() => { seleccionarOpcion("9") }}>
              <Text weight="bold">Personalizada</Text>
            </CheckboxCards.Item>
          </CheckboxCards.Root>
        </Box>
        <Text size="3" weight="bold">
          Otros
        </Text>
        <TextArea placeholder="Describe otros motivos" mt="2" value={otros} onChange={(e) => { 
            e.preventDefault();
            setOtros(e?.target?.value.trim())
        }} />
        <Flex width="100%" justify="end" mt="2">
          <Button mt="2" style={{ width: '100px' }}>
            Crear
          </Button>
        </Flex>
      </form>
    </Box>
  )
}
