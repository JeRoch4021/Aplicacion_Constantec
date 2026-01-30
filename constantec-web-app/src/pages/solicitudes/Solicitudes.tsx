import { Table, Badge, ScrollArea } from '@radix-ui/themes'
import { useGetSolicitudes } from './useGetSolicitudes'

export const SolicitudEstatusTipo = {
  PENDIENTE: 1,
  REVISION: 2,
  COMPLETO: 3,
} as const

const SolicitudEstatus = (props) => {
  const { estatus, etiqueta } = props

  switch (estatus) {
    case SolicitudEstatusTipo.PENDIENTE:
      return <Badge color="orange">{etiqueta}</Badge>
    case SolicitudEstatusTipo.REVISION:
      return <Badge color="blue">{etiqueta}</Badge>
    case SolicitudEstatusTipo.COMPLETO:
      return <Badge color="green">{etiqueta}</Badge>
    default:
      return <Badge color="red">No disponible</Badge>
  }
}

export const Solicitudes = () => {
  const id_estudiante = localStorage.getItem('id_estudiante') || ''
  const { data } = useGetSolicitudes(id_estudiante)

  return (
    <ScrollArea
      type="always"
      scrollbars="both"
      style={{ height: 'calc(100vh - 120px)' }}
    >
      <Table.Root style={{ width: '100%%' }} variant="surface" mt="3">
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeaderCell style={{ whiteSpace: 'nowrap' }}>
              Constancia
            </Table.ColumnHeaderCell>
            <Table.ColumnHeaderCell style={{ whiteSpace: 'nowrap' }}>
              Descripción de la Constancia
            </Table.ColumnHeaderCell>
            <Table.ColumnHeaderCell style={{ whiteSpace: 'nowrap' }}>
              No. de Control
            </Table.ColumnHeaderCell>
            <Table.ColumnHeaderCell style={{ whiteSpace: 'nowrap' }}>
              Fecha Solicitud
            </Table.ColumnHeaderCell>
            <Table.ColumnHeaderCell style={{ whiteSpace: 'nowrap' }}>
              Fecha Entrega
            </Table.ColumnHeaderCell>
            <Table.ColumnHeaderCell style={{ whiteSpace: 'nowrap' }}>
              Estatus
            </Table.ColumnHeaderCell>
            <Table.ColumnHeaderCell style={{ whiteSpace: 'nowrap' }}>
              Descripción del Estatus
            </Table.ColumnHeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {Array.isArray(data) &&
            data.length > 0 &&
            data.map((row) => (
              <Table.Row key={row.id}>
                <Table.RowHeaderCell>
                  {row.constancia.opciones[0]?.tipo.tipo ||
                    'Resultado Desconocido'}
                </Table.RowHeaderCell>
                <Table.RowHeaderCell>
                  {row.constancia.descripcion}
                </Table.RowHeaderCell>
                <Table.Cell>{row.estudiante.no_control}</Table.Cell>
                <Table.Cell>{row.fecha_solicitud}</Table.Cell>
                <Table.Cell>
                  {row.estatus.id === SolicitudEstatusTipo.COMPLETO
                    ? row.fecha_entrega
                    : ''}
                </Table.Cell>
                <Table.Cell>
                  <SolicitudEstatus
                    estatus={row.estatus.id}
                    etiqueta={row.estatus.tipo}
                  />
                </Table.Cell>
                <Table.Cell>{row.estatus.descripcion}</Table.Cell>
              </Table.Row>
            ))}
        </Table.Body>
      </Table.Root>
    </ScrollArea>
  )
}
