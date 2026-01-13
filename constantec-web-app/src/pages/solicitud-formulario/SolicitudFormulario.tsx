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
      setErrorForm('Agrega una descripción')
      return
    }

    if (opciones.length === 0) {
      setErrorForm('Selecciona al menos una opcion')
      return
    }

    if (folio.length === 0) {
      setErrorForm('Agrega el folio')
      return
    }

    if (errorForm.length > 0) {
      setErrorForm('')
    }

    const estudiante_id = localStorage.getItem('estudiante_id') || "";

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

  console.log(error, !error, !!error)

  return (
    <Box width="700px" mt="3">
      <form onSubmit={handleSubmit} className="flex flex-col gap-2 max-w-md">
        <Text size="3" weight="bold">
          Folio de factura de pago
        </Text>
          <TextArea
            placeholder="Ingresa el folio"
            mt="2"
            value={folio}
            disabled={loading}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => {
              const soloNumeros = e.target.value.replace(/\D/g, '')
              setFolio(soloNumeros)
            }}
            style={{ padding: 8, borderRadius: 4, border: '1px solid #ccc', marginBottom: 12, width: '100%' }}
        />
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
        <Text size="3" weight="bold">
          Marcar la opción que necesites
        </Text>
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
              <Text>Inscritos (IMSS, ISSTE, Pagobús)</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="2"
              onClick={() => {
                seleccionarOpcion('2')
              }}
            >
              <Text>Promedio general</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="3"
              onClick={() => {
                seleccionarOpcion('3')
              }}
            >
              <Text>Promedio semestre anterior</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="4"
              onClick={() => {
                seleccionarOpcion('4')
              }}
            >
              <Text>Promedio dos últimos semestres</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="5"
              onClick={() => {
                seleccionarOpcion('5')
              }}
            >
              <Text>Egresado</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="6"
              onClick={() => {
                seleccionarOpcion('6')
              }}
            >
              <Text>Bachillerato</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="7"
              onClick={() => {
                seleccionarOpcion('7')
              }}
            >
              <Text>Maestría</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="8"
              onClick={() => {
                seleccionarOpcion('8')
              }}
            >
              <Text>Título en tramite</Text>
            </CheckboxCards.Item>
            <CheckboxCards.Item
              value="9"
              onClick={() => {
                seleccionarOpcion('9')
              }}
            >
              <Text>Incluir número de Seguro Social</Text>
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
