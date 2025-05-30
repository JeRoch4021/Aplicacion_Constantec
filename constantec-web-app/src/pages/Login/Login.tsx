import { Container, Box, TextField, Text, Flex, Button, Spinner, Callout } from '@radix-ui/themes'
import { useEffect, useState } from 'react'
import logo from '../../assets/images/login_image.jpeg'
import { AutenticarPayload, useAutenticarUsuario } from './useAutenticarUsuario'
import { ExclamationTriangleIcon } from '@radix-ui/react-icons'

export const Login = () => {
  const [noControl, setNoControl] = useState('')
  const [password, setPassword] = useState('')
  const [errorForm, setError] = useState<string>('');

  const { login, loading, error, status } = useAutenticarUsuario();

  useEffect(() => {
    if (!!error && error.response?.data?.detail) {
      setError(error.response.data.detail)
    }
  }, [error])

  useEffect(() => {
      if (status === 'success') {
        window.location.href = '/dashboard';
      }
    }, [status])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (noControl?.length == 0) {
      setError('Numero de Control Requerido')
      return
    }

    if (password?.length == 0) {
      setError('Password Requerido')
      return
    }

    const peticion: AutenticarPayload = {
      no_control: noControl,
      contrasena: password
    }

    login(peticion);
    console.log('aqui llamamos el api por q ya tenemos usuario y password')
  }

  return (
    <Container size="1">
      <Flex direction="row" justify="center">
        <Box width="300px" pt="7">
          <img
            src={logo}
            alt="Bold typography"
            style={{
              display: 'block',
              objectFit: 'contain',
              width: '100%',
              height: 200,
            }}
          />
          <form onSubmit={handleSubmit} className="flex flex-col gap-2 max-w-md">
            <Text size="3">No. de Control</Text>
            <TextField.Root
              type="number"
              size="3"
              placeholder="Numero de Control"
              mb="3"
              disabled={loading}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                e.preventDefault()
                setNoControl(e?.target?.value.trim())
              }}
            />
            <Text size="3">Password</Text>
            <TextField.Root
              type="password"
              size="3"
              mb="3"
              disabled={loading}
              placeholder="Enter your password"
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                e.preventDefault()
                setPassword(e?.target?.value.trim())
              }}
            />
            <Flex pt="3" direction="row" justify="end" width="100%">
              <Button type="submit" size="3" style={{ width: '100%' }} disabled={loading}>
                {loading && <Spinner />}
                {!loading && 'Iniciar Sesión'}
              </Button>
            </Flex>
            {errorForm && (
              <Callout.Root color="red" mt="3">
                <Callout.Icon>
                  <ExclamationTriangleIcon />
                </Callout.Icon>
                <Callout.Text>{errorForm}</Callout.Text>
              </Callout.Root>
            )}
          </form>
        </Box>
      </Flex>
    </Container>
  )
}
