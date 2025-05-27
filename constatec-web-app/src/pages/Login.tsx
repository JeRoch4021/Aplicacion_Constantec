import { Container, Box, TextField, Text, Flex, Button } from '@radix-ui/themes'
import { useState } from 'react'
import logo from '../assets/images/login_image.jpeg'

export const Login = () => {
  const [noControl, setNoControl] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  const handleOnLogin = () => {
    if (noControl?.length == 0) {
      setError('Numero de Control Requerido')
      return
    }

    if (password?.length == 0) {
      setError('Password Requerido')
      return
    }

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
          <Text size="3">No. de Control</Text>
          <TextField.Root
            type="number"
            size="2"
            placeholder="Numero de Control"
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
              e.preventDefault()
              setNoControl(e?.target?.value.trim())
            }}
          />
          <Text size="3">Password</Text>
          <TextField.Root
            type="password"
            size="2"
            placeholder="Enter your password"
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
              e.preventDefault()
              setPassword(e?.target?.value.trim())
            }}
          />
          {error && (
            <Text color="tomato" size="3">
              {error}
            </Text>
          )}
          <Flex pt="3" direction="row" justify="end" width="100%">
            <Button style={{ width: '100%' }} onClick={handleOnLogin}>
              Login
            </Button>
          </Flex>
        </Box>
      </Flex>
    </Container>
  )
}
