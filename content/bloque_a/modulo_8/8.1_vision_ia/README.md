# 8.1 Visión por IA

## 8.1.1 Los LLMs Multimodales — Ver y Entender al Mismo Tiempo

Durante años, la visión artificial y el lenguaje natural fueron dos campos separados. Los modelos de visión (CNNs, YOLO) identificaban objetos pero no podían razonar sobre ellos. Los LLMs razonaban pero no "veían". Los modelos multimodales como Claude, GPT-4V o Gemini fusionan ambas capacidades: ven una imagen y razonan sobre ella con comprensión contextual profunda.

```
EVOLUCIÓN DE LA VISIÓN ARTIFICIAL:

  GENERACIÓN 1 — CLASIFICACIÓN CLÁSICA (2012-2018)
  ┌──────────────────────────────────────────────────────────────┐
  │  Entrada: imagen                                             │
  │  Salida: "gato" con 87% de confianza                        │
  │  Limitación: solo lo que fue entrenado a reconocer          │
  └──────────────────────────────────────────────────────────────┘

  GENERACIÓN 2 — DETECCIÓN DE OBJETOS (2015-2020)
  ┌──────────────────────────────────────────────────────────────┐
  │  Entrada: imagen                                             │
  │  Salida: bounding boxes + etiquetas (3 personas, 1 coche)   │
  │  Limitación: solo detecta, no entiende contexto ni semántica│
  └──────────────────────────────────────────────────────────────┘

  GENERACIÓN 3 — VISIÓN + LENGUAJE (2023→)
  ┌──────────────────────────────────────────────────────────────┐
  │  Entrada: imagen + pregunta en lenguaje natural              │
  │  Salida: respuesta contextual, razonada, detallada           │
  │                                                              │
  │  "¿Hay algún problema de seguridad en esta imagen            │
  │   de la línea de producción?"                               │
  │  → "Sí. El operario de la derecha no lleva casco de         │
  │     seguridad, incumpliendo la normativa. Además,           │
  │     hay un derrame de líquido no señalizado cerca            │
  │     de la máquina A3."                                       │
  └──────────────────────────────────────────────────────────────┘
```

**Para directivos**: el salto no es solo técnico, es económico. Antes se necesitaba un sistema de visión custom (meses de desarrollo, datos etiquetados, mantenimiento) para cada caso de uso. Ahora, con un modelo multimodal, el mismo sistema puede inspeccionar calidad, leer documentos, analizar dashboards y detectar incidencias, simplemente cambiando el prompt.

---

## 8.1.2 Casos de Uso Empresariales — El Mapa de Oportunidades

```
MAPA DE CASOS DE USO — VISIÓN IA EN EMPRESA:

  ┌─────────────────────────────────────────────────────────────┐
  │  MANUFACTURA E INDUSTRIA                                    │
  │  • Inspección de calidad en línea de producción             │
  │  • Detección de defectos en piezas (grietas, deformaciones) │
  │  • Control de presencia de EPIs (cascos, guantes, chalecos) │
  │  • Lectura de medidores analógicos y manómetros             │
  │  ROI típico: -60% de defectos que llegan al cliente         │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  DOCUMENTOS Y ADMINISTRACIÓN                                │
  │  • Extracción de datos de facturas escaneadas (OCR + IA)    │
  │  • Lectura de formularios y contratos en papel              │
  │  • Validación de documentos de identidad                    │
  │  • Digitalización de albaranes de entrega                   │
  │  ROI típico: -80% tiempo en entrada manual de datos         │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  RETAIL Y LOGÍSTICA                                         │
  │  • Verificación de planogramas en tienda (¿está bien puesto │
  │    el producto?)                                            │
  │  • Conteo de inventario por imagen                          │
  │  • Identificación de daños en paquetería                    │
  │  • Lectura de etiquetas y códigos de barras en contexto     │
  │  ROI típico: -40% incidencias de inventario                 │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  NEGOCIO Y ANÁLISIS                                         │
  │  • Análisis de dashboards en imagen (informe de BI a texto) │
  │  • Extracción de datos de gráficos y tablas en PDF          │
  │  • Comparativa visual de diseños o layouts                  │
  │  • Análisis de fotos de visitas comerciales                 │
  │  ROI típico: horas de análisis manual a minutos             │
  └─────────────────────────────────────────────────────────────┘
```

---

## 8.1.3 Anatomía de una Llamada de Visión con Claude

Para usar visión con Claude, se envía la imagen junto con el texto en el mismo mensaje. La imagen puede ser una URL o datos en base64.

```python
# Estructura básica de llamada de visión con Claude
import anthropic
import base64

client = anthropic.Anthropic()

# Opción A: imagen desde URL
respuesta = client.messages.create(
    model="claude-opus-4-5",  # o claude-haiku-4-5-20251001
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": "https://ejemplo.com/factura.jpg"
                }
            },
            {
                "type": "text",
                "text": "Extrae: número de factura, fecha, proveedor, importe total e IVA"
            }
        ]
    }]
)

# Opción B: imagen como base64 (para archivos locales)
with open("factura.jpg", "rb") as f:
    imagen_b64 = base64.standard_b64encode(f.read()).decode("utf-8")

respuesta = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": imagen_b64
                }
            },
            {
                "type": "text",
                "text": "¿Hay algún defecto visible en esta pieza industrial?"
            }
        ]
    }]
)
```

### Formatos de imagen compatibles

| Formato | Tipo MIME | Notas |
|---------|-----------|-------|
| JPEG | image/jpeg | Recomendado para fotos |
| PNG | image/png | Recomendado para documentos, texto |
| GIF | image/gif | Solo primer frame |
| WebP | image/webp | Buen balance tamaño/calidad |
| PDF (páginas) | — | Convertir a imagen primero |

---

## 8.1.4 Diseño de Prompts para Visión — Buenas Prácticas

Los prompts para visión tienen sus propias particularidades. El modelo "ve" la imagen completa pero necesita que le indiques qué buscar.

```
PROMPTS DE VISIÓN — PATRONES EFECTIVOS:

  EXTRACCIÓN DE DATOS ESTRUCTURADOS
  ─────────────────────────────────────────────────────────────
  "Extrae los siguientes campos de esta factura y devuelve JSON:
   {numero_factura, fecha, proveedor, nif_proveedor, base_imponible,
   iva_porcentaje, iva_importe, total}"
  
  Por qué funciona: especifica el esquema exacto, pide JSON (parseable)

  INSPECCIÓN CON CRITERIOS DEFINIDOS
  ─────────────────────────────────────────────────────────────
  "Inspecciona este producto terminado según estos criterios:
   1. ¿La superficie presenta grietas, rayaduras o deformaciones?
   2. ¿El color es uniforme? (referencia: RAL 5015 azul cielo)
   3. ¿Las dimensiones parecen correctas (el producto debe ser cuadrado)?
   Responde APROBADO o RECHAZADO para cada criterio con breve justificación."
  
  Por qué funciona: criterios concretos, respuesta estructurada por criterio

  ANÁLISIS CONTEXTUAL
  ─────────────────────────────────────────────────────────────
  "Esta imagen es de la pantalla de nuestro sistema de BI al final
   del mes. Actúa como un analista de negocio y:
   1. Identifica los 3 indicadores que más se desviaron del objetivo
   2. Detecta tendencias preocupantes
   3. Redacta un párrafo de resumen ejecutivo para el Comité de Dirección"
  
  Por qué funciona: da contexto de quién es el modelo, qué hacer y para quién

  COMPARACIÓN VISUAL
  ─────────────────────────────────────────────────────────────
  "Compara estas dos imágenes [imagen A] [imagen B].
   La primera es la distribución esperada en el lineal de tienda.
   La segunda es una foto tomada hoy en tienda.
   Lista todas las diferencias: productos mal colocados, huecos,
   artículos incorrectos o referencias en posición errónea."
```

---

## 8.1.5 Limitaciones y Cuándo No Usar Visión LLM

```
LIMITACIONES A CONOCER:

  PRECISIÓN MÉTRICA
  ─────────────────────────────────────────────────────────────
  Los LLMs no miden. No pueden decir "la pieza tiene 45,3 mm
  de largo". Para medición precisa → visión artificial clásica
  con calibración.

  TIEMPO REAL EN ALTA FRECUENCIA
  ─────────────────────────────────────────────────────────────
  Una llamada de visión tarda 1-5 segundos.
  Para inspección en línea a 100 piezas/minuto → sistema dedicado.
  Para revisión muestral (10% de la producción) → LLM viable.

  CONSISTENCIA ABSOLUTA
  ─────────────────────────────────────────────────────────────
  El mismo defecto puede describirse de formas ligeramente distintas
  en dos llamadas. Para sistemas regulados (farmacéutico, aeroespacial)
  donde la reproducibilidad es legal → validación adicional necesaria.

  PRIVACIDAD
  ─────────────────────────────────────────────────────────────
  Las imágenes se envían a la API del proveedor.
  Imágenes con personas → revisar consentimiento y GDPR.
  Documentos confidenciales → valorar solución on-premise.

  CUÁNDO SÍ ES LA SOLUCIÓN CORRECTA:
  ✓ Casos de uso donde la velocidad no es crítica (< 100 piezas/hora)
  ✓ Documentos sin datos ultra-sensibles
  ✓ Análisis cualitativo (no medición precisa)
  ✓ Prototipos rápidos antes de invertir en sistema dedicado
  ✓ Tareas que combinan visión + razonamiento complejo
```

---

*Anterior: [7.3 Permisología y Human-in-the-Loop](../../modulo_7/7.3_permisologia_hitl/README.md) | Siguiente: [8.2 Audio y Transcripción](../8.2_audio_transcripcion/README.md)*
