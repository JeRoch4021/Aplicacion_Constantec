import { useState, useEffect } from 'react'
import axiosClient from '../../api/axiosClient'
import {
  Box,
  Text,
  TextArea,
  Callout,
  Button,
  Flex,
  Spinner,
} from '@radix-ui/themes' 
import { useGetEncuestaEstatus } from './useGetEncuestaEstatus'
import { CheckCircledIcon } from '@radix-ui/react-icons'

const enviarEncuesta = async (estudiante_id: number, calificacion: number, sugerencia: string) => {
  const response = await axiosClient.post('/v1/encuestas/', {
    estudiante_id,
    calificacion,
    sugerencia
  })
  return response.data
}

export const EncuestaSatisfaccion = () => {
  const estudiante_id = Number (localStorage.getItem('estudiante_id'))
  const { data: yaRespondio, isLoading, refetch } = useGetEncuestaEstatus(estudiante_id)

  const [valor, setValor] = useState<number | null>(null)
  const [sugerencia, setSugerencia] = useState<string>('')
  const [enviado, setEnviado] = useState(false)
  const [errorForm, setErrorForm] = useState<string>('')
  const [status, setStatus] = useState< 'idle' | 'loading' | 'success' | 'error'>('idle')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrorForm('')
    setStatus('loading')
    try {
      await enviarEncuesta(estudiante_id, valor!, sugerencia.trim())
      await refetch()
      setStatus('success')
      setEnviado(true)
      setSugerencia('')
    } catch (error: any) {
      setErrorForm(error?.response?.data?.detail || 'Error al enviar la encuesta')
      setStatus('error')
    }
  }

  useEffect(() => {
    if (status === 'success') {
      setValor(null)
    }
  }, [status])

  if (isLoading) return <Flex justify="center" mt="9"><Spinner size="3" /></Flex>;

  return (
    <Flex direction="column" align="center" justify="center" width="100%" mt="7">
      <Box width="100%" maxWidth="450px">
        { yaRespondio ? (
          <Callout.Root color='green' variant='surface'>
            <Callout.Icon>
              <CheckCircledIcon />
            </Callout.Icon>
            <Callout.Text align="center">
              Tu opinión ya ha sido registrada con exito. Muchas gracias.
            </Callout.Text>
          </Callout.Root>
        ) : (
          <form onSubmit={handleSubmit} 
          style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>

            <Text size="3" weight="bold">
              ¿Qué tan satisfecho estas con el servicio?
            </Text>

            <Text size="2" color="gray" mt="1">
              (1 = Nada satisfecho, 5 = Muy satisfecho)
            </Text>

            <Flex gap="5" mt="5" mb="5" justify="center">
              {[1, 2, 3, 4, 5].map((num) => (
                <label key={num} 
                  style={{ cursor: 'pointer', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
                  <input
                  type="radio"
                  name="satisfaccion"
                  value={num}
                  checked={valor === num}
                  onChange={() => setValor(num)}
                  required
                  disabled={enviado}
                  style={{ width: '20px', height: '20px' }}/>
                  <Text size="3" weight={valor === num ? "bold" : "regular"}>{num}</Text>
                </label>
              ))}
            </Flex>

            <Flex gap="5" justify="center" align="center" style={{ height: '100px', width: '100%' }}>
              <Box mt="1" style={{ width: '300px'}}>
                <Text size="3" weight="bold">Sugerencias</Text>
                <TextArea
                  placeholder="Describe cuales serian tus sugerencias"
                  mt="2"
                  value={ sugerencia }
                  disabled={ status === 'loading' || enviado }
                  onChange={(e) => {
                    e.preventDefault()
                    setSugerencia(e?.target?.value)
                }}/>
              </Box>
            </Flex>

            <Box mt="4">
              <Button type="submit"disabled={ valor === null || enviado || status === 'loading' }>
                { status === 'loading' ? <Spinner/> : 'Enviar' }
              </Button>
            </Box>

            {errorForm && (
              <Callout.Root color="red" mt="4" style={{ width: '100%' }}>
                <Callout.Text>{errorForm}</Callout.Text>
              </Callout.Root>
            )}
            {enviado && status === 'success' && (
              <Callout.Root color="green" mt="4" style={{ width: '100%' }}>
                <Callout.Text>¡Gracias por tu respuesta!</Callout.Text>
              </Callout.Root>
            )}
          </form>
        )}
      </Box>   
    </Flex>
    
  )
}
