import {
  Box,
  Card,
  Flex,
  Text,
  Avatar,
  Grid,
  Container,
  Badge,
  Skeleton,
} from '@radix-ui/themes'
import { useGetUsuario } from './useGetUsuario'

export const PerfilUsuario = () => {
  const { data: estudiante, isLoading, isError } = useGetUsuario()

  if (isLoading) {
    return (
      <Container size="2" mt="5">
        <Skeleton height="200px" />
      </Container>
    )
  }

  if (isError) {
    return (
      <Container size="2" mt="5">
        <Text color="red">No se pudo cargar la información del perfil.</Text>
      </Container>
    )
  }

  return (
    <Container size="2">
      <Card size="3" mt="5">
        <Flex gap="4" align="center" mb="5">
          <Avatar
            size="6"
            fallback={estudiante?.nombre?.[0] || 'E'}
            radius="full"
          />
          <Box>
            <Text as="div" size="6" weight="bold">
              {estudiante?.nombre} {estudiante?.apellido_paterno}
            </Text>
            <Flex gap="2" align="center">
              <Text as="div" size="2" color="gray">
                No. de Control: {estudiante?.no_control}
              </Text>
              <Badge color="blue">Estudiante</Badge>
            </Flex>
          </Box>
        </Flex>

        <Grid columns={{ initial: '1', sm: '2' }} gap="4">
          <Box>
            <Text as="div" size="1" color="gray" weight="bold">
              CARRERA
            </Text>
            <Text as="div" size="3">
              {estudiante?.carrera || 'No especificada'}
            </Text>
          </Box>

          <Box>
            <Text as="div" size="1" color="gray" weight="bold">
              SEMESTRE
            </Text>
            <Text as="div" size="3">
              {estudiante?.semestre}º Semestre
            </Text>
          </Box>

          <Box>
            <Text as="div" size="1" color="gray" weight="bold">
              CORREO INSTITUCIONAL
            </Text>
            <Text as="div" size="3">
              {estudiante?.correo_institucional}
            </Text>
          </Box>

          <Box>
            <Text as="div" size="1" color="gray" weight="bold">
              ESTATUS ACADÉMICO
            </Text>
            <Text>
              <Badge
                color={estudiante?.is_active ? 'green' : 'red'}
                variant="soft"
                size="2"
              >
                {estudiante?.is_active ? 'Activo' : 'Inactivo'}
              </Badge>
            </Text>
          </Box>

          <Box>
            <Text as="div" size="1" color="gray" weight="bold">
              FECHA DE NACIMIENTO
            </Text>
            <Text as="div" size="3">
              {estudiante?.fecha_nacimiento}
            </Text>
          </Box>

          <Box>
            <Text as="div" size="1" color="gray" weight="bold">
              EDAD
            </Text>
            <Text as="div" size="3">
              {estudiante?.edad}
            </Text>
          </Box>

          <Box>
            <Text as="div" size="1" color="gray" weight="bold">
              MUNICIPIO
            </Text>
            <Text as="div" size="3">
              {estudiante?.municipio}
            </Text>
          </Box>

          <Box>
            <Text as="div" size="1" color="gray" weight="bold">
              FECHA DE REGISTRO
            </Text>
            <Text as="div" size="3">
              {estudiante?.fecha_registro}
            </Text>
          </Box>
        </Grid>
      </Card>
    </Container>
  )
}
