# 8.3 Pipelines Multimodales

## 8.3.1 Qué es un Pipeline Multimodal y por Qué Importa

Un pipeline multimodal combina texto, imágenes y audio en un flujo de procesamiento automático. La potencia no está en cada modalidad por separado, sino en cómo se encadenan para transformar datos en bruto (una foto, un audio, un PDF) en acciones de negocio (un asiento contable, una alerta, un ticket de CRM).

```
DIFERENCIA: TAREA PUNTUAL vs. PIPELINE MULTIMODAL

  TAREA PUNTUAL:
  ────────────────────────────────────────────────────────────
  "Extrae los datos de esta factura"
  → 1 imagen + 1 prompt → 1 resultado

  PIPELINE MULTIMODAL:
  ────────────────────────────────────────────────────────────
  1. Recibir email con PDF adjunto [trigger]
  2. Convertir PDF a imagen [procesamiento]
  3. Claude extrae datos de la factura [IA visual]
  4. Validar datos contra pedido en ERP [herramienta]
  5. Si válida → contabilizar automáticamente [acción]
  6. Si discrepancia → crear tarea en el sistema financiero [HITL]
  7. Notificar al responsable con resumen [output]

  El pipeline opera 24/7 sin intervención humana en el caso feliz.
  Solo escala a humanos cuando hay excepciones.
```

**Para directivos**: un pipeline multimodal bien diseñado no es un proyecto de IA, es un rediseño de proceso. La pregunta no es "¿cómo usamos IA aquí?" sino "¿cómo debería funcionar este proceso si tuviésemos un empleado perfecto, rápido, disponible 24/7?"

---

## 8.3.2 Caso de Uso Completo — Procesamiento de Facturas

Este es el pipeline de mayor adopción en empresas. Reduces semanas de trabajo manual a horas, con mayor precisión.

```
PIPELINE COMPLETO — PROCESAMIENTO AUTOMÁTICO DE FACTURAS:

  ┌─────────────────────────────────────────────────────────────┐
  │  TRIGGER: Email recibido en facturas@empresa.com            │
  │           con PDF adjunto                                   │
  └──────────────────────────┬──────────────────────────────────┘
                             │
  ┌──────────────────────────▼──────────────────────────────────┐
  │  PASO 1: CAPTURA Y PREPARACIÓN                              │
  │  • Descargar adjunto del email                              │
  │  • Verificar que es PDF/imagen (no ejecutable)              │
  │  • Convertir PDF a imagen(es) si es necesario               │
  │  • Almacenar en carpeta de procesamiento                    │
  └──────────────────────────┬──────────────────────────────────┘
                             │
  ┌──────────────────────────▼──────────────────────────────────┐
  │  PASO 2: EXTRACCIÓN CON IA VISUAL                           │
  │  • Claude analiza la imagen de la factura                   │
  │  • Extrae: proveedor, NIF, fecha, número, líneas, total     │
  │  • Detecta moneda, idioma, tipo (factura/albarán/nota)      │
  │  • Confianza por campo: alta / media / baja                 │
  └──────────────────────────┬──────────────────────────────────┘
                             │
  ┌──────────────────────────▼──────────────────────────────────┐
  │  PASO 3: VALIDACIÓN CONTRA SISTEMAS                         │
  │  • Verificar proveedor en maestro de proveedores            │
  │  • Buscar pedido de compra relacionado en ERP               │
  │  • Comparar importes (factura vs. pedido, tolerancia 1%)   │
  │  • Comprobar que no es duplicado (número ya registrado)     │
  └──────────────────────────┬──────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │ VALIDADA     │ DISCREPANCIA │ ERROR CRÍTICO
              ▼              ▼              ▼
  ┌───────────────┐ ┌───────────────┐ ┌───────────────────┐
  │ PASO 4A:      │ │ PASO 4B:      │ │ PASO 4C:          │
  │ CONTABILIZAR  │ │ TAREA HUMANA  │ │ ALERTA INMEDIATA  │
  │ AUTOMÁTICO   │ │               │ │                   │
  │ • Asiento ERP │ │ • Asignar al  │ │ • Posible fraude  │
  │ • Programar   │ │   responsable │ │   o error grave   │
  │   pago según  │ │ • Resumen de  │ │ • Notificar DPO   │
  │   vencimiento │ │   discrepancia│ │   si datos PII    │
  │ • Archivar    │ │ • SLA: 24h   │ │   afectados       │
  └───────────────┘ └───────────────┘ └───────────────────┘
              │
  ┌──────────────────────────────────────────────────────────────┐
  │  PASO 5: NOTIFICACIÓN Y REGISTRO                            │
  │  • Email de confirmación al proveedor                        │
  │  • Registro de auditoría completo                            │
  │  • Dashboard actualizado (facturas/día, tasa de error)       │
  └──────────────────────────────────────────────────────────────┘
```

**KPIs de éxito del pipeline**:
- Tasa de procesamiento automático: objetivo > 80% sin intervención humana
- Precisión de extracción: objetivo > 98% de campos críticos correctos
- Tiempo de ciclo: de días a minutos
- Tasa de duplicados detectados: objetivo 100%

---

## 8.3.3 Patrones de Orquestación Multimodal

Hay tres patrones principales para combinar modalidades en un pipeline:

```
PATRÓN 1 — SECUENCIAL (el más común)
─────────────────────────────────────────────────────────────────
Cada modalidad alimenta a la siguiente en cadena lineal.

  Imagen → OCR → Texto → LLM → Acción

Cuándo usarlo: cuando las modalidades tienen dependencias claras.
El output de una es el input de la siguiente.

Ejemplo: foto de albarán → extracción de datos → validación → registro


PATRÓN 2 — PARALELO (para velocidad o redundancia)
─────────────────────────────────────────────────────────────────
Múltiples procesos ejecutan simultáneamente sobre el mismo input.

  Imagen ─┬→ Claude (descripción cualitativa)
          ├→ OCR clásico (texto exacto)
          └→ Modelo de visión clásica (detección objetos)
          │
          └→ Combinar resultados → Output enriquecido

Cuándo usarlo: cuando necesitas complementar las capacidades del LLM
con otras herramientas especializadas (precisión de OCR clásico +
comprensión contextual del LLM).


PATRÓN 3 — CONDICIONAL (para pipelines robustos)
─────────────────────────────────────────────────────────────────
El flujo se bifurca según el contenido detectado.

  Entrada (desconocida)
  → Clasificador: ¿qué tipo de documento es?
    ├─ Factura → pipeline de facturas
    ├─ Albarán → pipeline de albaranes
    ├─ Contrato → pipeline de contratos
    └─ Desconocido → cola de revisión humana

Cuándo usarlo: cuando el sistema recibe documentos de tipo variado
y necesita enrutarlos al proceso correcto automáticamente.
```

---

## 8.3.4 Diseño de Prompts Multimodales Encadenados

En un pipeline multimodal, el output de un prompt se convierte en input del siguiente. Esto requiere diseñar los prompts para producir formatos que los pasos siguientes puedan consumir.

```
EJEMPLO — CADENA DE PROMPTS PARA INFORME DE REUNIÓN CON PRESENTACIÓN:

  PASO 1: Transcripción del audio de la reunión
  ─────────────────────────────────────────────
  Input: audio (.mp3)
  Proceso: Whisper → texto
  Output: transcripción con timestamps y hablantes

  PASO 2: Análisis de la presentación visual
  ─────────────────────────────────────────────
  Input: diapositivas (imágenes PNG)
  Prompt: "Describe cada slide en 1-2 frases. Extrae: título,
           datos clave, gráficos o tablas presentes."
  Output: JSON { slide_1: {...}, slide_2: {...} }

  PASO 3: Síntesis multimodal
  ─────────────────────────────────────────────
  Input: transcripción + descripciones de slides
  Prompt: "Eres el secretario de esta reunión. Tienes la
           transcripción y el contenido de las diapositivas.
           Genera el acta oficial, referenciando los datos
           de las slides cuando sean relevantes."
  Output: acta completa con referencias a datos de las slides

  PASO 4: Extracción de tareas
  ─────────────────────────────────────────────
  Input: acta del paso 3
  Prompt: "Del siguiente acta, extrae SOLO las acciones
           asignadas en formato JSON:
           [{ responsable, accion, fecha_limite }]"
  Output: JSON de tareas → importar al gestor de proyectos
```

---

## 8.3.5 Casos de Uso Multimodales por Industria

```
SECTOR FINANCIERO
─────────────────────────────────────────────────────────────────
Pipeline: Foto del documento de identidad + selfie + formulario
→ OCR del DNI/pasaporte (datos del cliente)
→ Verificación biométrica facial (coincide con DNI)
→ Extracción de datos del formulario
→ Registro en el sistema + validación AML/KYC
→ Notificación de alta o solicitud de documentación adicional
ROI: proceso de onboarding de días a minutos


SECTOR RETAIL/LOGÍSTICA
─────────────────────────────────────────────────────────────────
Pipeline: Foto de recepción de mercancía + albarán del proveedor
→ Claude compara visualmente lo recibido con el albarán
→ Detecta discrepancias (cantidad, daños visibles, referencias)
→ Si OK → confirmación de recepción automática en ERP
→ Si discrepancia → tarea de reclamación con fotos adjuntas
ROI: de 2h de verificación manual a 5 minutos automáticos


SECTOR SALUD (uso con especial atención a GDPR)
─────────────────────────────────────────────────────────────────
Pipeline: Imagen de prescripción médica en papel
→ OCR + Claude extrae: medicamento, dosis, posología, médico
→ Validación contra formulario de medicamentos aprobados
→ Si válido → generación de solicitud de dispensación
→ Si dosis fuera de rango → alerta farmacéutico
ROI: reducción de errores de transcripción manual


SECTOR SEGUROS
─────────────────────────────────────────────────────────────────
Pipeline: Fotos de daños del siniestro + informe del perito (audio)
→ Claude analiza fotos: tipo de daño, extensión, causa probable
→ Whisper transcribe el informe del perito
→ LLM cruza la evaluación visual con el informe
→ Genera estimación de coste de reparación
→ Si < umbral → aprobación automática del siniestro
→ Si > umbral → escala a perito senior con todo el contexto
ROI: resolución de siniestros simples en horas vs. días
```

**Consejo práctico**: no intentes construir el pipeline completo desde el principio. Empieza con Paso 1 + Paso 2, mide la calidad, y añade pasos gradualmente. Cada paso que automatizas bien ya genera valor.

---

*Anterior: [8.2 Audio y Transcripción](../8.2_audio_transcripcion/README.md) | Siguiente: [9.1 AI Act y GDPR](../../modulo_9/9.1_ai_act_gdpr/README.md)*
