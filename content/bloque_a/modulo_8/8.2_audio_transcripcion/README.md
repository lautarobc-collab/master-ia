# 8.2 Audio — Transcripción e Inteligencia sobre Llamadas

## 8.2.1 El Audio como Dato Empresarial No Explotado

Las empresas generan cantidades masivas de audio que permanecen sin analizar: llamadas de atención al cliente, reuniones de equipo, entrevistas comerciales, formaciones, mensajes de voz. Transformar este audio en datos estructurados y accionables es una de las oportunidades más inmediatas y de mayor ROI en IA aplicada.

```
AUDIO EMPRESARIAL — INVENTARIO DE FUENTES:

  FUENTE                    VOLUMEN TÍPICO     VALOR POTENCIAL
  ─────────────────────────────────────────────────────────────
  Call center (servicio)    1.000-50.000 h/mes  Muy alto
  Reuniones de equipo       5-20 h/semana       Alto
  Llamadas comerciales      2-8 h/semana/rep    Alto
  Entrevistas RRHH          4-8 h/semana        Medio
  Formaciones internas      Decenas h/mes       Medio
  Mensajes de voz           Variable            Bajo-Medio
  Webinars y demos          4-8 h/semana        Medio
```

La paradoja: el audio de una llamada de ventas de 45 minutos contiene más información de negocio que el CRM después de la llamada. El comercial registra 3 líneas; en el audio hay objeciones, tonos, compromisos, señales de compra — toda la riqueza de la conversación.

---

## 8.2.2 Stack Tecnológico para Audio Empresarial

```
ARQUITECTURA — PIPELINE DE AUDIO EMPRESARIAL:

  CAPTURA
  ┌──────────────────────────────────────────────────────────────┐
  │  Fuentes de entrada:                                         │
  │  • Integración con plataforma de video (Zoom, Teams, Meet)  │
  │  • Grabación de llamadas en centralita VoIP                  │
  │  • Carga manual de archivos (.mp3, .wav, .m4a, .ogg)        │
  │  • API de mensajería (WhatsApp Business, voicenotes)         │
  └──────────────────────────┬───────────────────────────────────┘
                             │
  TRANSCRIPCIÓN (Speech-to-Text)
  ┌──────────────────────────────────────────────────────────────┐
  │  Opciones por caso de uso:                                   │
  │                                                              │
  │  OpenAI Whisper (open source)                                │
  │    + Gratuito si self-hosted, muy preciso en español        │
  │    + Funciona offline (privacidad)                           │
  │    - Requiere GPU para velocidad aceptable                   │
  │                                                              │
  │  AssemblyAI                                                  │
  │    + API cloud, fácil integración                            │
  │    + Speaker diarization (quién habla cuándo)               │
  │    + Análisis de sentimiento incorporado                     │
  │    - Coste por minuto de audio                               │
  │                                                              │
  │  Google Speech-to-Text / Azure Cognitive                    │
  │    + Integración nativa con ecosistema Google/Microsoft      │
  │    + Buena diarización y puntuación automática               │
  │    - Ecosistema propietario                                  │
  └──────────────────────────┬───────────────────────────────────┘
                             │
  ANÁLISIS (LLM sobre transcripción)
  ┌──────────────────────────────────────────────────────────────┐
  │  Claude / GPT-4 / Gemini                                     │
  │  Procesa el texto de la transcripción para extraer:         │
  │  • Acta de reunión estructurada                              │
  │  • Análisis de sentimiento por segmento                      │
  │  • Identificación de acuerdos y compromisos                  │
  │  • Scoring de llamada comercial                              │
  │  • Detección de señales de alerta                            │
  └──────────────────────────┬───────────────────────────────────┘
                             │
  INTEGRACIÓN
  ┌──────────────────────────────────────────────────────────────┐
  │  Salida estructurada hacia sistemas corporativos:            │
  │  • CRM: registrar resumen + compromisos de llamada           │
  │  • Notion/Confluence: actas de reunión                       │
  │  • RRHH: feedback de entrevistas                             │
  │  • Dashboard: métricas de calidad de servicio                │
  └──────────────────────────────────────────────────────────────┘
```

---

## 8.2.3 Generación Automática de Actas

El caso de uso más inmediato y de mayor adopción. Cada reunión genera automáticamente un acta estructurada sin que nadie tenga que tomarla manualmente.

```
ESTRUCTURA DE ACTA AUTOMÁTICA — CAMPOS ESTÁNDAR:

  CABECERA
  • Título de la reunión
  • Fecha, hora de inicio y fin
  • Participantes identificados (con diarización)
  • Tipo: informativa / de decisión / de trabajo

  CONTEXTO
  • Objetivo de la reunión (detectado del inicio)
  • Documentos o materiales referenciados

  DESARROLLO (cronológico o por temas)
  • Temas tratados con resumen de cada discusión
  • Posiciones diferentes si las hay

  DECISIONES TOMADAS
  → Lista de decisiones con quién la tomó

  ACCIONES / PRÓXIMOS PASOS
  → [ACCIÓN] Responsable — Descripción — Fecha límite
  → [ACCIÓN] Responsable — Descripción — Fecha límite

  PRÓXIMA REUNIÓN
  • Fecha propuesta si se mencionó
  • Temas pendientes para la próxima sesión
```

**Prompt de generación de acta** (para usar en producción):

```
Eres el secretario de actas de [Empresa].
Procesa esta transcripción de reunión y genera el acta oficial.

INSTRUCCIONES:
- Usa el formato de acta corporativo de la empresa
- Distingue claramente entre "se discutió", "se decidió" y "se asignó"
- Para cada acción: identificar responsable, acción concreta, fecha si se mencionó
- Si hay ambigüedad sobre quién dijo qué, usa "un participante"
- Tono: formal y conciso
- No incluyas frases de relleno ni saludos de la transcripción

TRANSCRIPCIÓN:
[insertar transcripción aquí]
```

---

## 8.2.4 Análisis de Sentimiento en Llamadas

El análisis de sentimiento sobre transcripciones de llamadas permite a los responsables de servicio al cliente detectar patrones sin escuchar cada llamada.

```
MÉTRICAS DE ANÁLISIS DE LLAMADAS:

  NIVEL DE LLAMADA INDIVIDUAL
  ─────────────────────────────────────────────────────────────
  • Satisfacción percibida del cliente (1-5)
  • Nivel de frustración detectado (bajo/medio/alto)
  • Resolución en primera llamada (sí/no)
  • Temas principales (reclamación/consulta/cancelación/compra)
  • Compromisos adquiridos por el agente
  • Alertas: amenaza de baja, mención competencia, queja de producto

  NIVEL AGREGADO (semana/mes)
  ─────────────────────────────────────────────────────────────
  • Distribución de sentimiento por tipo de llamada
  • Correlación entre duración y satisfacción
  • Top 10 motivos de contacto
  • Agentes con mayor/menor satisfacción percibida
  • Tendencia de alertas (¿aumentan las amenazas de baja?)

  INTEGRACIÓN CON CRM
  ─────────────────────────────────────────────────────────────
  → Registro automático post-llamada:
    { cliente_id, fecha, duracion, sentimiento, temas,
      compromisos_agente, accion_recomendada }
  → Alertas en tiempo real: si sentimiento = muy negativo
    + mención de cancelación → notificación al supervisor
```

---

## 8.2.5 Implementación Práctica — Sin API de Audio

Para empresas que no quieren pagar por una API de transcripción, Whisper de OpenAI es open source y puede instalarse localmente:

```bash
# Instalar Whisper (requiere Python 3.8+)
pip install openai-whisper

# Transcribir un archivo de audio
python -c "
import whisper
modelo = whisper.load_model('base')  # o 'small', 'medium', 'large'
resultado = modelo.transcribe('reunion.mp3', language='es')
print(resultado['text'])
"
```

```
MODELOS DE WHISPER — ELEGIR SEGÚN RECURSOS:

  Modelo    Tamaño    VRAM    Velocidad   Precisión
  ─────────────────────────────────────────────────
  tiny      39 MB     1 GB    ~32×        Baja
  base      74 MB     1 GB    ~16×        Aceptable
  small     244 MB    2 GB    ~6×         Buena
  medium    769 MB    5 GB    ~2×         Muy buena
  large     1.5 GB    10 GB   1×          Excelente

  Para empresas: 'medium' en CPU es suficiente para la mayoría de casos.
  Reuniones de 1h tardan ~5-10 minutos en transcribirse con medium en CPU.
```

**Consideración de privacidad**: Whisper local no envía el audio a ningún servidor externo. Es la opción preferida para reuniones de directivos, entrevistas de RRHH o cualquier contenido sensible.

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Radford et al. / OpenAI (2022) — *Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)* → [arxiv.org/abs/2212.04356](https://arxiv.org/abs/2212.04356)

**Informes de industria:**
- McKinsey (anual) — *The State of AI* → [mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) *(transcripción e inteligencia sobre llamadas como caso de mayor ROI en atención al cliente)*
- Stanford University (anual) — *AI Index Report* → [aiindex.stanford.edu/report/](https://aiindex.stanford.edu/report/) *(estado actual de los sistemas de reconocimiento de voz y su precisión en múltiples idiomas)*

**Libros recomendados:**
- Iansiti & Lakhani (2020) — *Competing in the Age of AI* (HBR Press) — el audio empresarial como activo de datos no explotado y su potencial de transformación operativa

**Documentación oficial:**
- *OpenAI Whisper (repositorio oficial)* → [github.com/openai/whisper](https://github.com/openai/whisper) *(instalación, modelos disponibles y opciones de configuración para transcripción local)*
- *AssemblyAI Documentation* → [docs.assemblyai.com](https://www.assemblyai.com/docs/) *(API de transcripción cloud con diarización de hablantes y análisis de sentimiento)*

*Anterior: [8.1 Visión por IA](../8.1_vision_ia/README.md) | Siguiente: [8.3 Pipelines Multimodales](../8.3_pipelines_multimodales/README.md)*
