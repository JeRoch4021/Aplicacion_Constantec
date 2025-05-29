import { Flex, Tabs, Separator, Container, Button, Avatar, Text } from '@radix-ui/themes';
import { Solicitudes } from './Solicitudes';
import { SolicitudFormulario } from './SolicitudFormulario/SolicitudFormulario';

export const Dashboard = () => {
  return (
    <>
      <Flex width="100%" align="center" justify="between" p="1">
        <Flex direction="row" align="center">
          <Avatar
            src="https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453?&w=256&h=256&q=70&crop=focalpoint&fp-x=0.5&fp-y=0.3&fp-z=1&fit=crop"
            fallback="A"
          />
          <Text size="5" ml="2">Constantec</Text>
        </Flex>
        <Flex direction="row" align="center">
          <Button>Perfil</Button>
          <Button variant='soft' ml="2">Cerrar sesion</Button>
        </Flex>
      </Flex>
      <Separator style={{ width: '100%'}} />
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
  );
}
