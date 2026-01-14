import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useState, useEffect } from 'react'
import axiosClient from '../../api/axiosClient'
import {
  Box,
  Text,
  TextArea,
  Button,
  CheckboxCards,
  Flex,
  Spinner,
  Callout,
} from '@radix-ui/themes'
import {
  ExclamationTriangleIcon,
  CheckCircledIcon,
} from '@radix-ui/react-icons'
import { SolicitudPayload, useCrearSoliciutd } from './useCrearSolicitud'

export const createSolicitud = async (data) => {
  const res = await axiosClient.post('/solicitudes', data)
  return res.data
}

export const SolicitudFormulario = () => {
  const [opciones, setOpciones] = useState<Array<string>>([])
  const [descripcion, setDescripcion] = useState<string>('')
  const [otros, setOtros] = useState<string>('')
  const [errorForm, setErrorForm] = useState<string>('')
  const [folio, setFolio] = useState('')

  const { crearSolicitud, loading, error, status } = useCrearSoliciutd()

  useEffect(() => {
    if (!!error && error.response?.data?.detail) {
      setErrorForm(error.response.data.detail)
    }
  }, [error])

  useEffect(() => {
    if (status === 'success') {
      setDescripcion('')
      setOpciones([])
      setFolio('')
      setOtros('')
    }
  }, [status])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (descripcion.length === 0) {
      setErrorForm('La descripción es obligatoria')
      return
    }

    if (opciones.length === 0) {
      setErrorForm('Selecciona al menos un tipo de constancia')
      return
    }

    if (folio.length === 0) {
      setErrorForm('El folio de pago es obligatorio')
      return
    }

    if (errorForm.length > 0) {
      setErrorForm('')
    }

    const estudiante_id = localStorage.getItem('estudiante_id') || ''

    const peticion: SolicitudPayload = {
      descripcion: descripcion.trim(),
      otros: otros.trim(),
      id_estudiante: estudiante_id,
      constancia_opciones: opciones,
      folio: folio.trim(),
    }

    crearSolicitud(peticion)
  }

  const seleccionarOpcion = (value: string) => {
    const nuevasOpciones = opciones.includes(value)
      ? opciones.filter((item) => item !== value)
      : [...opciones, value]
    setOpciones(nuevasOpciones)
  }

  return (
    <Box width="700px" mt="3">
      <form onSubmit={handleSubmit} className="flex flex-col gap-2 max-w-md">

        {/* DESCRIPCIÓN */}
        <Text size="3" weight="bold">
          Descripción de la solicitud
        </Text>
        <TextArea
          aria-label="Descripción de la solicitud"
          placeholder="Ejemplo: Solicito constancia para trámite de beca"
          mt="2"
          value={descripcion}
          disabled={loading}
          onChange={(e) => setDescripcion(e.target.value)}
        />

        {/* TIPO DE CONSTANCIA */}
        <Text size="3" weight="bold" mt="3">
          Tipo de constancia solicitada
        </Text>
        <Text size="2" color="gray">
          Selecciona una o más opciones según tu necesidad
        </Text>

        <Box mt="2" mb="2">
          <CheckboxCards.Root
            disabled={loading}
            value={opciones}
            columns={{ initial: '1', sm: '3' }}
          >
            {[
              { id: '1', text: 'Inscritos' },
              { id: '2', text: 'Kardex' },
              { id: '3', text: 'Seguro Social' },
              { id: '4', text: 'Calificaciones del Semestre Anterior' },
              { id: '5', text: 'Calificaciones de Dos Semestres Anteriores' },
              { id: '6', text: 'Egreso' },
              { id: '7', text: 'Título en Trámite' },
              { id: '8', text: 'Pago' },
              { id: '9', text: 'Personalizada' },
            ].map((opcion) => (
              <CheckboxCards.Item
                key={opcion.id}
                value={opcion.id}
                onClick={() => seleccionarOpcion(opcion.id)}
              >
                <Text>{opcion.text}</Text>
              </CheckboxCards.Item>
            ))}
          </CheckboxCards.Root>
        </Box>

        {/* FOLIO */}
        <Text size="3" weight="bold">
          Folio de factura de pago
        </Text>
        <TextArea
          aria-label="Folio de factura de pago"
          placeholder="Ejemplo: 12345678 (solo números)"
          mt="2"
          value={folio}
          disabled={loading}
          onChange={(e) =>
            setFolio(e.target.value.replace(/\D/g, ''))
          }
        />

        {/* OTROS */}
        <Text size="3" weight="bold">
          Otros (opcional)
        </Text>
        <TextArea
          aria-label="Otros motivos de la solicitud"
          placeholder="Describe aquí otro motivo si no aparece en la lista"
          mt="2"
          value={otros}
          disabled={loading}
          onChange={(e) => setOtros(e.target.value)}
        />

        {/* BOTÓN */}
        <Flex width="100%" justify="end" mt="2">
          <Button
            type="submit"
            style={{ width: '200px' }}
            size="3"
            disabled={loading}
          >
            {loading ? <Spinner /> : 'Enviar solicitud'}
          </Button>
        </Flex>

        {/* ERRORES */}
        {!!errorForm && (
          <Callout.Root color="red" mt="3">
            <Callout.Icon>
              <ExclamationTriangleIcon />
            </Callout.Icon>
            <Callout.Text>{errorForm}</Callout.Text>
          </Callout.Root>
        )}

        {/* ÉXITO */}
        {status === 'success' && !errorForm && (
          <Callout.Root color="green" mt="3">
            <Callout.Icon>
              <CheckCircledIcon />
            </Callout.Icon>
            <Callout.Text>
              La solicitud se guardó exitosamente
            </Callout.Text>
          </Callout.Root>
        )}
      </form>
    </Box>
  )
}
