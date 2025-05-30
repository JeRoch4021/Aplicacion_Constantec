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
      setOtros('')
    }
  }, [status])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (descripcion.length === 0) {
      setErrorForm('Agrega una descripción')
      return
    }

    if (opciones.length === 0) {
      setErrorForm('Selecciona al menos una opcion')
      return
    }

    if (errorForm.length > 0) {
      setErrorForm('')
    }

    const peticion: SolicitudPayload = {
      descripcion: descripcion.trim(),
      otros: otros.trim(),
      id_estudiante: '1',
      constancia_opciones: opciones,
    }

    crearSolicitud(peticion)
  }

  const seleccionarOpcion = (value: string) => {
    const nuevasOpciones = opciones.includes(value)
      ? opciones.filter((item) => item !== value)
      : [...opciones, value]
    setOpciones(nuevasOpciones)
  }

  console.log(error, !error, !!error)

  return (
    <Box width="700px" mt="3">
      <form onSubmit={handleSubmit} className="flex flex-col gap-2 max-w-md">
        <Text size="3" weight="bold">
          Descripcion
        </Text>
        <TextArea
          placeholder="Descripcion de la constancia"
          mt="2"
          value={descripcion}
          disabled={loading}
          onChange={(e) => {
            e.preventDefault()
            setDescripcion(e?.target?.value)
          }}
        />
        <Box mt="2" mb="2">
          <CheckboxCards.Root
            disabled={loading}
            defaultValue={[]}
            value={opciones || []}
            columns={{ initial: '1', sm: '3' }}
          >
            <CheckboxCards.Item
              value="1"
              onClick={() => {
                seleccionarOpcion('1')
              }}
            >
              <Text>Inscritos</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="2"
              onClick={() => {
                seleccionarOpcion('2')
              }}
            >
              <Text>Kardex</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="3"
              onClick={() => {
                seleccionarOpcion('3')
              }}
            >
              <Text>Seguro Social</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="4"
              onClick={() => {
                seleccionarOpcion('4')
              }}
            >
              <Text>Calificaciones del Semestre Anterior</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="5"
              onClick={() => {
                seleccionarOpcion('5')
              }}
            >
              <Text>Calificaciones de Dos Semestres Anteriores</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="6"
              onClick={() => {
                seleccionarOpcion('6')
              }}
            >
              <Text>Egreso</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="7"
              onClick={() => {
                seleccionarOpcion('7')
              }}
            >
              <Text>Título en Trámite</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="8"
              onClick={() => {
                seleccionarOpcion('8')
              }}
            >
              <Text>Pago</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="9"
              onClick={() => {
                seleccionarOpcion('9')
              }}
            >
              <Text>Personalizada</Text>
            </CheckboxCards.Item>
          </CheckboxCards.Root>
        </Box>
        <Text size="3" weight="bold">
          Otros
        </Text>
        <TextArea
          placeholder="Describe otros motivos"
          mt="2"
          value={otros}
          disabled={loading}
          onChange={(e) => {
            e.preventDefault()
            setOtros(e?.target?.value)
          }}
        />
        <Flex width="100%" justify="end" mt="2">
          <Button
            type="submit"
            mt="2"
            style={{ width: '200px' }}
            size="3"
            disabled={loading}
          >
            {loading && <Spinner />}
            {!loading && 'Enviar'}
          </Button>
        </Flex>
        {!!errorForm && (
          <Callout.Root color="red" mt="3">
            <Callout.Icon>
              <ExclamationTriangleIcon />
            </Callout.Icon>
            <Callout.Text>{errorForm}</Callout.Text>
          </Callout.Root>
        )}
        {status === 'success' && !errorForm && (
          <Callout.Root color="green" mt="3">
            <Callout.Icon>
              <CheckCircledIcon />
            </Callout.Icon>
            <Callout.Text>Se guardo exitosamente</Callout.Text>
          </Callout.Root>
        )}
      </form>
    </Box>
  )
}
