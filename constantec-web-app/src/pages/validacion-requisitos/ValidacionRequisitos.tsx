import { useEffect, useMemo, useState } from 'react'
import { Flex, Text, Button, Separator } from '@radix-ui/themes'
import { useGetUsuario } from './useGetUsuario'
import { usePostComprobante } from './usePostComprobante'
import { useGetEstadoComprobante } from './useGetEstadoComprobante'

type EstadoValidacion =
  | 'SIN_COMPROBANTE'
  | 'PENDIENTE'
  | 'RECHAZADO'
  | 'APROBADO'

type ValidacionData = {
  estado: EstadoValidacion
  motivo?: string
  archivoNombre?: string
  actualizadoEn?: string
}

// SOLO PARA PRUEBAS (si no hay nada en localStorage)
const ESTADO_MOCK: EstadoValidacion = 'SIN_COMPROBANTE'

const MOTIVO_RECHAZO_MOCK ='El comprobante no es legible o no corresponde al trámite.'

const STORAGE_KEY = 'validacion_requisitos_alumno'

const MAX_MB = 5
const MAX_BYTES = MAX_MB * 1024 * 1024
const ALLOWED_TYPES = ['application/pdf', 'image/png', 'image/jpeg']

export function ValidacionRequisitos() {
  const { data: estudiante } = useGetUsuario();
  const { mutate, isPending } = usePostComprobante();
  const { data: comprobante, isLoading } = useGetEstadoComprobante(estudiante?.no_control)

  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const data = useMemo(() => {
    return comprobante || { estado: 'SIN_COMPROBANTE' };
  }, [comprobante])

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] ?? null;
    setError(null);
    if (!selected) return;

    if (!ALLOWED_TYPES.includes(selected.type)) {
      setError('Formato no permitido. Solo PDF, JPG o PNG.');
      return;
    }
    if (selected.size > MAX_BYTES) {
      setError(`El archivo excede ${MAX_MB} MB.`);
      return;
    }
    setFile(selected);
  }

  /* =========================
     SUBIR COMPROBANTE
  ========================= */

  const handleEnviar = () => {
    if (!file || !estudiante?.no_control) {
      setError('Información incompleta para el envío.');
      return;
    }

    const formData = new FormData();
    formData.append('archivo', file);
    formData.append('no_control', estudiante.no_control);

    mutate(formData, {
      onSuccess: () => {
        setFile(null);
        setError(null);
      },
      onError: (err: any) => {
        setError(err.response?.data?.detail || 'Error al subir el archivo');
      }
    });
  };
  
  const estadoTexto = useMemo(() => {
    const textos: Record<EstadoValidacion, string> = {
      'SIN_COMPROBANTE': 'Sin comprobante',
      'PENDIENTE': 'Pendiente de validación',
      'RECHAZADO': 'Rechazado',
      'APROBADO': 'Aprobado'
    };
    return textos[data.estado] || 'Desconocido';
  }, [data.estado]);

  const puedeSubir = data.estado === 'SIN_COMPROBANTE' || data.estado === 'RECHAZADO';

  return (
    <Flex width="100%" justify="center">
      <Flex direction="column" style={{ maxWidth: 720, width: '100%' }} gap="3" p="4">
        <Text size="7" weight="bold" align="center" mt="4">
          Validación de Requisitos
        </Text>

        <Text color="gray" align="center">
          Para continuar con el trámite de tu constancia, sube tu comprobante de
          pago (PDF o imagen). El documento será revisado por el personal
          administrativo.
        </Text>

        <Separator size="4" />

        <Text>
          <strong>Estado: </strong>
          <Text color={data.estado === 'APROBADO' ? 'green' : data.estado === 'RECHAZADO' ? 'red' : 'orange'} mt="2">
            {estadoTexto}
          </Text>
        </Text>

        {data.archivoNombre && <Text color="gray" size="2">Archivo registrado: {data.archivoNombre}</Text>}

        {data.estado === 'PENDIENTE' && (
          <Text color="gray" size="2">
            Tu comprobante está en revisión. Espera la validación del personal
            administrativo.
          </Text>
        )}

        {data.estado === 'RECHAZADO' && data.motivo && (
          <Text color="red" weight="bold">
            <strong>Motivo de rechazo:</strong> {data.motivo}
          </Text>
        )}

        {data.estado === 'APROBADO' && (
          <Text color="green">
            Tu comprobante fue aprobado. Ya puedes continuar con el trámite.
          </Text>
        )}

        <Separator size="4" />

        {/* Subida */}
        {puedeSubir && (
          <>
            <Text weight="bold">Subir comprobante</Text>

            <input
              type="file"
              accept=".pdf,image/png,image/jpeg"
              onChange={onFileChange}
            />

            {file && <Text color="gray">Archivo: {file.name}</Text>}
            {error && <Text color="red">{error}</Text>}

            <Flex justify="end">
              <Button disabled={!file || isPending} onClick={ handleEnviar }>
                {loading ? 'Enviando...' : 'Enviar comprobante'}
              </Button>
            </Flex>

            <Text color="gray" size="2">
              Tamaño máximo: {MAX_MB} MB. Formatos permitidos: PDF, JPG, PNG.
            </Text>
          </>
        )}
      </Flex>
    </Flex>
  )
}
