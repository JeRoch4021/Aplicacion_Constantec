import { Table } from '@radix-ui/themes';
import { useGetSolicitudes } from './useGetSolicitudes';
export const Solicitudes = () => {
  const { data } = useGetSolicitudes(1);
  
  return (
    <Table.Root>
      <Table.Header>
        <Table.Row>
          <Table.ColumnHeaderCell>Constancia</Table.ColumnHeaderCell>
          <Table.ColumnHeaderCell>No. de Control</Table.ColumnHeaderCell>
          <Table.ColumnHeaderCell>Fecha de Solicitud</Table.ColumnHeaderCell>
          <Table.ColumnHeaderCell>Status</Table.ColumnHeaderCell>
          <Table.ColumnHeaderCell>Descripcion</Table.ColumnHeaderCell>
        </Table.Row>
      </Table.Header>

      <Table.Body>
        {data &&data.map((row) =>( 
          <Table.Row>
            <Table.RowHeaderCell>{row.constancia.descripcion}</Table.RowHeaderCell>
            <Table.Cell>{row.estudiante.no_control}</Table.Cell>
            <Table.Cell>{row.fecha_solicitud}</Table.Cell>
            <Table.Cell>{row.estatus.tipo}</Table.Cell>
            <Table.Cell>{row.estatus.descripcion}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table.Root>
  )
}
