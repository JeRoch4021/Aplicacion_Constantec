import { Flex, Tabs, Separator, Button, Avatar, Text } from '@radix-ui/themes'
import { Solicitudes } from '../Solicitudes'
import { SolicitudFormulario } from '../SolicitudFormulario/SolicitudFormulario'
import { useState } from 'react'
import logo from '../../assets/images/constantec_logo.jpg'
import profile from '../../assets/images/profile.png'

export const Dashboard = () => {
  const [error, setError] = useState<string | null>(null)

  const cerrarSession = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  }

  return (
    <>
      <Flex width="100%" align="center" justify="between" p="1">
        <Flex direction="row" align="center">
          <Avatar
            src={logo}
            fallback="A"
          />
          <Text size="5" ml="2">
            Constantec
          </Text>
        </Flex>
        <Flex direction="row" align="center">
          <Avatar
            src={profile}
            fallback="A"
          />
          <Button variant="soft" ml="2" onClick={cerrarSession}>
            Cerrar sesion
          </Button>
        </Flex>
      </Flex>
      <Separator style={{ width: '100%' }} />
      <Tabs.Root defaultValue="solicitudes" className="w-full">
        <Tabs.List className="flex border-b gap-4 p-4">
          <Tabs.Trigger value="solicitudes">Solicitudes</Tabs.Trigger>
          <Tabs.Trigger value="crear">Crear Solicitud</Tabs.Trigger>
        </Tabs.List>

        <Tabs.Content value="solicitudes" className="p-4">
          <Flex width="100%" justify="center">
            <Solicitudes />
          </Flex>
        </Tabs.Content>
        <Tabs.Content value="crear" className="p-4">
          <Flex width="100%" justify="center">
            <SolicitudFormulario />
          </Flex>
        </Tabs.Content>
      </Tabs.Root>
    </>
  )
}
