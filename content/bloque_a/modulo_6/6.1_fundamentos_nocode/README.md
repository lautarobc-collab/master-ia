# 6.1 Fundamentos No-Code e Integración con IA

## 6.1.1 El Stack No-Code para IA en la Empresa

Las herramientas no-code permiten automatizar flujos con IA sin escribir código. Esto democratiza la implementación: un responsable de operaciones, marketing o RRHH puede construir su propio automatismo sin depender del departamento de IT.

```
STACK NO-CODE PARA IA — 3 CAPAS:

ORQUESTACIÓN (el flujo):
  n8n           → open source, self-hosted, potente, curva media
  Make (Integromat) → cloud, visual, más intuitivo
  Zapier        → cloud, más sencillo, menos potente
  Power Automate → integrado con Microsoft 365

IA (el cerebro):
  Claude API    → calidad, contexto largo, pricing predecible
  OpenAI API    → ecosistema amplio, multimodal nativo
  Gemini API    → integrado con Google Workspace

ALMACENAMIENTO / TRIGGER:
  Google Sheets / Airtable → datos simples, triggers por fila
  Notion        → base de conocimiento + automatización
  Webhooks      → trigger desde cualquier sistema
```

---

## 6.1.2 Casos de Uso No-Code Más Frecuentes

### Caso 1 — Clasificación y enrutamiento automático de emails
```
TRIGGER: Nuevo email en bandeja de soporte
PASO 1:  Extraer asunto + cuerpo del email
PASO 2:  Claude clasifica (consulta/reclamación/pedido) y determina urgencia
PASO 3:  Enrutar al agente correcto y añadir etiqueta en CRM
PASO 4:  Si urgencia alta → notificación instantánea al responsable

Herramientas: Gmail trigger → n8n → Claude API → HubSpot/Gmail
Tiempo de implementación: 2-4 horas
```

### Caso 2 — Generación automática de actas de reunión
```
TRIGGER: Archivo de transcripción subido a carpeta de Drive
PASO 1:  Leer el archivo de texto
PASO 2:  Claude extrae: asistentes, temas tratados, decisiones, próximos pasos con responsable y fecha
PASO 3:  Formatear como documento Notion o Google Doc
PASO 4:  Enviar email con el acta a los asistentes

Herramientas: Google Drive trigger → n8n → Claude API → Notion/Gmail
```

### Caso 3 — Enriquecimiento de leads
```
TRIGGER: Nuevo lead en CRM
PASO 1:  Recoger datos: empresa, cargo, sector, web
PASO 2:  Claude genera resumen de la empresa y perfil del lead
PASO 3:  Clasificar lead por scoring (frío/tibio/caliente) según criterios definidos
PASO 4:  Actualizar CRM con el enriquecimiento y asignar al comercial correcto
```

### Caso 4 — Monitoreo de competidores
```
TRIGGER: Schedule semanal
PASO 1:  Scraping de webs / feeds RSS de competidores
PASO 2:  Claude resume novedades relevantes por competidor
PASO 3:  Genera comparativa con nuestra oferta
PASO 4:  Envía briefing semanal a comercial y marketing
```

---

## 6.1.3 Anatomía de un Flujo en n8n

```
[TRIGGER]
  │  Qué evento arranca el flujo
  │  (nuevo email, schedule, webhook, nueva fila en Sheet)
  ▼
[PREPARACIÓN DE DATOS]
  │  Extraer y formatear los datos del trigger
  │  Construir el prompt con los datos
  ▼
[LLAMADA A IA]
  │  Nodo HTTP Request → Claude API
  │  Método: POST, URL: https://api.anthropic.com/v1/messages
  │  Headers: x-api-key, anthropic-version, content-type
  │  Body: JSON con model, max_tokens, messages
  ▼
[PROCESAMIENTO DEL OUTPUT]
  │  Parsear la respuesta (JSON si el output es JSON)
  │  Transformar si es necesario
  ▼
[ACCIÓN]
  │  Escribir en Sheet, enviar email, crear tarea, actualizar CRM
  ▼
[MANEJO DE ERRORES]
     Si falla → notificación + log → continúa o para
```

---

## 6.1.4 Llamada a Claude API desde n8n

```json
// Configuración del nodo HTTP Request en n8n:
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "headers": {
    "x-api-key": "{{ $env.ANTHROPIC_API_KEY }}",
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
  },
  "body": {
    "model": "claude-haiku-4-5-20251001",
    "max_tokens": 300,
    "messages": [
      {
        "role": "user",
        "content": "{{ $json.prompt }}"
      }
    ]
  }
}

// Extraer la respuesta:
// {{ $json.content[0].text }}
```

---

## 6.1.5 Buenas Prácticas en Flujos No-Code con IA

```
ERRORES COMUNES Y CÓMO EVITARLOS:

1. No manejar errores de la API
   → Siempre añadir nodo de manejo de errores con notificación

2. Prompt hardcoded en el flujo
   → Guardar el prompt en una variable de entorno o un Sheet
     para poder actualizarlo sin tocar el flujo

3. Sin logging
   → Guardar cada llamada (input, output, timestamp) en un Sheet
     para auditoría y mejora del prompt

4. Flujo que procesa sin límite de velocidad
   → Añadir nodo de rate limiting: máx. N llamadas por minuto

5. Datos sensibles en el log
   → Anonimizar antes de guardar
```

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Schick et al. (2023) — *Toolformer: Language Models Can Teach Themselves to Use Tools* → [arxiv.org/abs/2302.04761](https://arxiv.org/abs/2302.04761)

**Informes de industria:**
- McKinsey (anual) — *The State of AI* → [mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) *(automatización no-code como palanca de productividad en empresas medianas)*
- Gartner — *Hype Cycle for Artificial Intelligence* → [gartner.com](https://www.gartner.com) *(posicionamiento de herramientas de automatización low-code/no-code en el mercado empresarial)*

**Libros recomendados:**
- Iansiti & Lakhani (2020) — *Competing in the Age of AI* (HBR Press) — la democratización de la automatización como factor de transformación operativa en empresas de todos los tamaños

**Documentación oficial:**
- *n8n Documentation* → [docs.n8n.io](https://docs.n8n.io) *(referencia técnica para los flujos de automatización descritos en el módulo)*
- *Anthropic Documentation — API Reference* → [docs.anthropic.com](https://docs.anthropic.com) *(estructura de llamadas a la API de Claude desde herramientas no-code)*

*Anterior: [5.3 Integración con Business Intelligence](../../modulo_5/5.3_integracion_bi/README.md) | Siguiente: [6.2 IA como Motor de Decisión](../6.2_ia_motor_decision/README.md)*
