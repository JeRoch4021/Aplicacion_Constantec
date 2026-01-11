import { useState, useEffect } from 'react'
import axiosClient from '../../api/axiosClient'
import {
  Box,
  Text,
  Callout,
  Button,
} from '@radix-ui/themes'


const enviarEncuesta = async (estudiante_id: number, calificacion: number) => {
  const response = await axiosClient.post('http://localhost:8000/v1/encuestas/', {
    estudiante_id,
    calificacion
  })
  return response.data
}


export const EncuestaSatisfaccion = () => {
  const [valor, setValor] = useState<number | null>(null)
  const [enviado, setEnviado] = useState(false)
  const [errorForm, setErrorForm] = useState<string>('')
  const [status, setStatus] = useState< 'idle' | 'success' | 'error'>('idle')

  const estudiante_id = Number (localStorage.getItem('estudiante_id'))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrorForm('')
    setStatus('idle')
    try {
      await enviarEncuesta(estudiante_id, valor!)
      setStatus('success')
      setEnviado(true)
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

  return (
    <Box width="700px" mt="3" style={{ display: 'flex', justifyContent: 'center' }}>
        <form onSubmit={handleSubmit} className="flex flex-col gap-2 max-w-md" style={{ alignItems: 'center', width: '100%' }}>
             <Text size="3" weight="bold" align="center">
                ¿Qué tan satisfecho estas con el servicio?
             </Text>
             <br></br>
             <Text size="2" mt="2" align="center">
                (1 = Nada satisfecho, 5 = Muy satisfecho)
             </Text>
        <div style={{ display: "flex", gap: 16, margin: "16px 0" }}>
        {[1, 2, 3, 4, 5].map((num) => (
          <label key={num} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <input
              type="radio"
              name="satisfaccion"
              value={num}
              checked={valor === num}
              onChange={() => setValor(num)}
              required
              disabled={enviado}
            />
            <Text>{num}</Text>
          </label>
        ))}
        </div>
        <Button type="submit"disabled={valor === null || enviado}>
            Enviar
        </Button>
        {errorForm && (
          <Callout.Root color="red" mt="3">
            <Callout.Text>
              {errorForm}
            </Callout.Text>
          </Callout.Root>
        )}
        {enviado && status === 'success' && (
          <Callout.Root color="green" mt="3">
            <Callout.Text>
              ¡Gracias por tu respuesta!
            </Callout.Text>
          </Callout.Root>
        )}
        </form>
    </Box>   
  )
}
