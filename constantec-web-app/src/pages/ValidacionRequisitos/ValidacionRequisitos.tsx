import { useEffect, useMemo, useState } from 'react'
import { Flex, Text, Button, Separator } from '@radix-ui/themes'

/* =========================
   TIPOS
========================= */

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

/* =========================
   CONFIGURACIÓN
========================= */

// 👉 SOLO PARA PRUEBAS (si no hay nada en localStorage)
const ESTADO_MOCK: EstadoValidacion = 'SIN_COMPROBANTE'

const MOTIVO_RECHAZO_MOCK =
  'El comprobante no es legible o no corresponde al trámite.'

const STORAGE_KEY = 'validacion_requisitos_alumno'

const MAX_MB = 5
const MAX_BYTES = MAX_MB * 1024 * 1024
const ALLOWED_TYPES = ['application/pdf', 'image/png', 'image/jpeg']

/* =========================
   COMPONENTE
========================= */

export function ValidacionRequisitos() {
  const [data, setData] = useState<ValidacionData>({
    estado: 'SIN_COMPROBANTE',
  })

  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  /* =========================
     CARGAR ESTADO (LOCALSTORAGE / MOCK)
  ========================= */

  const fetchEstadoValidacion = async () => {
    const stored = localStorage.getItem(STORAGE_KEY)

    // 1️⃣ Si hay algo guardado, se usa eso
    if (stored) {
      setData(JSON.parse(stored))
      return
    }

    // 2️⃣ Si no hay nada, usar mock
    if (ESTADO_MOCK === 'RECHAZADO') {
      setData({
        estado: 'RECHAZADO',
        motivo: MOTIVO_RECHAZO_MOCK,
        archivoNombre: 'comprobante.pdf',
        actualizadoEn: new Date().toLocaleString(),
      })
    } else if (ESTADO_MOCK === 'PENDIENTE') {
      setData({
        estado: 'PENDIENTE',
        archivoNombre: 'comprobante.pdf',
        actualizadoEn: new Date().toLocaleString(),
      })
    } else if (ESTADO_MOCK === 'APROBADO') {
      setData({
        estado: 'APROBADO',
        archivoNombre: 'comprobante.pdf',
        actualizadoEn: new Date().toLocaleString(),
      })
    } else {
      setData({ estado: 'SIN_COMPROBANTE' })
    }
  }

  useEffect(() => {
    fetchEstadoValidacion()
  }, [])

  /* =========================
     MANEJO DE ARCHIVO
  ========================= */

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] ?? null
    setError(null)
    setFile(null)

    if (!selected) return

    if (!ALLOWED_TYPES.includes(selected.type)) {
      setError('Formato no permitido. Solo PDF, JPG o PNG.')
      return
    }

    if (selected.size > MAX_BYTES) {
      setError(`El archivo excede ${MAX_MB} MB.`)
      return
    }

    setFile(selected)
  }

  /* =========================
     SUBIR COMPROBANTE
  ========================= */

  const subirComprobante = async () => {
    if (!file) {
      setError('Selecciona un archivo antes de enviar.')
      return
    }

    setLoading(true)
    setError(null)

    // 🔹 Simulación de envío
    await new Promise((r) => setTimeout(r, 800))

    const newData: ValidacionData = {
      estado: 'PENDIENTE',
      archivoNombre: file.name,
      actualizadoEn: new Date().toLocaleString(),
    }

    setData(newData)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newData))

    setFile(null)
    setLoading(false)
  }

  /* =========================
     UX SEGÚN ESTADO
  ========================= */

  const estadoTexto = useMemo(() => {
    switch (data.estado) {
      case 'SIN_COMPROBANTE':
        return 'Sin comprobante'
      case 'PENDIENTE':
        return 'Pendiente de validación'
      case 'RECHAZADO':
        return 'Rechazado'
      case 'APROBADO':
        return 'Aprobado'
      default:
        return 'Desconocido'
    }
  }, [data.estado])

  const puedeSubir =
    data.estado === 'SIN_COMPROBANTE' || data.estado === 'RECHAZADO'

  /* =========================
     RENDER
  ========================= */

  return (
    <Flex width="100%" justify="center">
      <Flex direction="column" style={{ maxWidth: 720, width: '100%' }} gap="3">
        <Text size="7" weight="bold" align="center">
          Validación de Requisitos
        </Text>

        <Text color="gray" align="center">
          Para continuar con el trámite de tu constancia, sube tu comprobante de
          pago (PDF o imagen). El documento será revisado por el personal
          administrativo.
        </Text>

        <Separator />

        <Text>
          <strong>Estado:</strong> {estadoTexto}
        </Text>

        {data.archivoNombre && (
          <Text color="gray">Último archivo: {data.archivoNombre}</Text>
        )}

        {data.actualizadoEn && (
          <Text color="gray">Actualizado: {data.actualizadoEn}</Text>
        )}

        {data.estado === 'PENDIENTE' && (
          <Text color="gray">
            Tu comprobante está en revisión. Espera la validación del personal
            administrativo.
          </Text>
        )}

        {data.estado === 'RECHAZADO' && data.motivo && (
          <Text color="red">
            <strong>Motivo de rechazo:</strong> {data.motivo}
          </Text>
        )}

        {data.estado === 'APROBADO' && (
          <Text color="green">
            ✅ Tu comprobante fue aprobado. Ya puedes continuar con el trámite.
          </Text>
        )}

        <Separator />

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
              <Button disabled={!file || loading} onClick={subirComprobante}>
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
