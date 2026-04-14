# 7.2 Tool-Calling y Herramientas

## 7.2.1 Cómo los LLMs Usan Herramientas

Los modelos de lenguaje, por diseño, solo generan texto. No pueden ejecutar código, consultar bases de datos ni enviar emails. El mecanismo de **tool-calling** (también llamado function calling) es el puente que conecta la capacidad de razonamiento del LLM con el mundo real.

```
MECANISMO DE TOOL-CALLING — PASO A PASO:

  USUARIO                  APLICACIÓN               LLM (Claude)
  ─────────                ─────────────            ─────────────
  "¿Cuántas               → Enviar mensaje         → Razona: necesito
   oportunidades            + lista de tools          consultar el CRM
   de venta               
   tenemos abiertas?"                              ← Responde:
                                                      {"tool": "consultar_crm",
                                                       "params": {"estado": "abierto",
                                                                  "tipo": "oportunidad"}}

                          → Ejecutar función        
                            consultar_crm(...)      
                            Resultado: 47 opor.     

                          → Enviar resultado        → Razona: tengo el dato
                            al LLM                  ← Responde en lenguaje
                                                      natural: "Actualmente
                                                      tienes 47 oportunidades
                                                      de venta abiertas..."
  ← Recibe respuesta
    comprensible
```

**Punto clave**: el LLM **nunca ejecuta el código**. Solo indica qué herramienta llamar y con qué parámetros. La aplicación ejecuta la herramienta y devuelve el resultado. Esto es fundamental para la seguridad: el desarrollador controla qué herramientas existen y qué pueden hacer.

---

## 7.2.2 Definición de Tools — Anatomía de una Herramienta

Cada herramienta se describe al LLM mediante un schema JSON. La calidad de esta descripción determina si el LLM la usará correctamente.

```
ANATOMÍA DE UNA TOOL — EJEMPLO: consultar_calendario

{
  "name": "consultar_calendario",          ← Nombre único, snake_case
  
  "description": "Busca los eventos del    ← CRÍTICO: descripción clara
    calendario del usuario en un rango      de cuándo y cómo usar esta
    de fechas. Devuelve título, hora        herramienta. El LLM decide
    de inicio y participantes.",            si usarla basándose en esto.
  
  "input_schema": {
    "type": "object",
    "properties": {
      "fecha_inicio": {
        "type": "string",
        "description": "Fecha inicio en    ← Describir el formato esperado
          formato YYYY-MM-DD",
      },
      "fecha_fin": {
        "type": "string",
        "description": "Fecha fin, incluida"
      },
      "filtro_palabras": {
        "type": "string",
        "description": "Opcional: filtrar   ← Indicar si es opcional
          por palabras clave en el título"
      }
    },
    "required": ["fecha_inicio", "fecha_fin"]   ← Parámetros obligatorios
  }
}
```

### Reglas de oro para diseñar buenas tools

| Regla | Mal ejemplo | Buen ejemplo |
|-------|------------|-------------|
| Nombres descriptivos | `fn1`, `execute` | `buscar_cliente_por_email` |
| Descripción inequívoca | "busca datos" | "Busca el perfil completo de un cliente en el CRM por su email. Devuelve nombre, empresa, histórico de compras y último contacto" |
| Un solo propósito | `gestionar_cliente` (crea, edita, borra) | Tools separadas: `crear_cliente`, `actualizar_cliente`, `archivar_cliente` |
| Parámetros con tipo y descripción | `{"q": string}` | `{"email_cliente": {"type": "string", "description": "Email corporativo del cliente, ej: nombre@empresa.com"}}` |
| Indicar formato de retorno | (nada) | "Devuelve JSON con campos: id, nombre, empresa, fecha_ultimo_contacto" |

---

## 7.2.3 Diseño de APIs para Agentes

Las APIs que los agentes consumen tienen requisitos distintos a las APIs diseñadas para uso humano directo.

```
APIs PARA HUMANOS vs. APIs PARA AGENTES:

  PARA HUMANOS                        PARA AGENTES
  ─────────────────────────────────   ─────────────────────────────────
  Interfaz rica (HTML, formularios)   Respuesta estructurada (JSON limpio)
  Paginación con scroll infinito      Paginación con limit/offset explícito
  Errores con página 404 bonita       Errores con código y mensaje útil
  Autenticación con redirect OAuth    Autenticación con API key o token
  Tolerancia a parámetros extras      Validación estricta de inputs
  Respuesta con HTML/CSS              Respuesta solo con datos
```

### Principios para diseñar APIs que los agentes usen bien

```
PRINCIPIO 1 — RESPUESTAS PREDECIBLES
  Devolver siempre la misma estructura, incluso en casos vacíos:
  
  MAL:  Si no hay resultados → error 404
  BIEN: Si no hay resultados → {"resultados": [], "total": 0}

PRINCIPIO 2 — ERRORES INFORMATIVOS
  El agente necesita saber QUÉ falló para decidir si reintentar:
  
  MAL:  {"error": "Bad request"}
  BIEN: {"error": "PARAM_INVALID", "campo": "email_cliente",
         "detalle": "Formato de email incorrecto: recibido 'juan.empresa'"}

PRINCIPIO 3 — IDEMPOTENCIA DONDE SEA POSIBLE
  Si el agente llama dos veces a crear_pedido por un timeout,
  no debe crear dos pedidos. Usar idempotency keys.

PRINCIPIO 4 — OPERACIONES ATÓMICAS
  Mejor una tool que haga un paso que muchas cosas a la vez.
  Si falla en el paso 3 de 5, ¿el agente sabe qué deshacer?

PRINCIPIO 5 — TIEMPO REAL VS. ASYNC
  Las tools deben ser rápidas (< 5s). Si la operación es lenta
  (ej: generar un informe complejo), usar patrón async:
    1. crear_tarea() → devuelve task_id
    2. consultar_estado(task_id) → PENDIENTE / COMPLETADO
    3. obtener_resultado(task_id) → resultado final
```

---

## 7.2.4 Catálogo de Tools Corporativas — Ejemplos Reales

Este es un catálogo de referencia de las herramientas más útiles en entornos empresariales:

```
CATEGORÍA: CALENDARIO Y COMUNICACIÓN
─────────────────────────────────────────────────────────────────
  consultar_disponibilidad(persona, fecha_inicio, fecha_fin)
    → slots libres de la persona en el rango indicado

  crear_reunion(titulo, participantes[], fecha, duracion, descripcion)
    → crea evento en Google Calendar / Outlook y envía invitaciones

  enviar_email(destinatarios[], asunto, cuerpo, cc[], adjuntos[])
    → envía email corporativo desde la cuenta del agente

  buscar_emails(query, desde, hasta, carpeta)
    → busca emails por criterio, devuelve lista con preview

CATEGORÍA: CRM (HubSpot / Salesforce)
─────────────────────────────────────────────────────────────────
  buscar_contacto(email)
    → devuelve perfil completo del contacto en el CRM

  actualizar_etapa_oportunidad(id_oportunidad, nueva_etapa)
    → mueve la oportunidad en el pipeline

  crear_tarea_crm(id_contacto, titulo, fecha_vencimiento, responsable)
    → crea tarea de seguimiento asignada a un comercial

  registrar_interaccion(id_contacto, tipo, fecha, notas)
    → registra llamada, reunión o email como actividad en CRM

CATEGORÍA: BASE DE DATOS / ERP
─────────────────────────────────────────────────────────────────
  consultar_stock(sku, almacen)
    → devuelve unidades disponibles, reservadas y en tránsito

  consultar_pedido(numero_pedido)
    → estado, líneas, fechas estimadas de entrega

  crear_solicitud_compra(proveedor, articulos[], urgencia)
    → genera solicitud en ERP pendiente de aprobación

  consultar_factura(numero_factura)
    → datos de factura, estado de pago, vencimiento

CATEGORÍA: DOCUMENTOS Y CONOCIMIENTO
─────────────────────────────────────────────────────────────────
  buscar_en_base_conocimiento(query, categoria)
    → devuelve fragmentos relevantes de la wiki corporativa

  crear_documento(titulo, contenido, carpeta, permisos)
    → crea documento en Google Drive / SharePoint

  extraer_texto_pdf(url_o_id_documento)
    → devuelve texto extraído de un PDF corporativo
```

---

## 7.2.5 Seguridad en Tool-Calling

Las herramientas son el vector de riesgo más alto de un agente. Un agente con tool-calling mal diseñado puede borrar datos, enviar emails masivos o exponer información sensible.

```
PRINCIPIOS DE SEGURIDAD EN TOOL-CALLING:

  MÍNIMO PRIVILEGIO
  ─────────────────────────────────────────────────────────────
  Cada agente tiene solo las tools que necesita para su tarea.
  Un agente de atención al cliente NO necesita:
    ✗ crear_pedido_masivo
    ✗ acceder_datos_financieros
    ✗ modificar_precios
  Solo necesita: consultar_pedido, registrar_reclamacion, escalar_ticket

  ACCIONES IRREVERSIBLES → SIEMPRE CONFIRMAR
  ─────────────────────────────────────────────────────────────
  Antes de ejecutar:
    • eliminar_cliente
    • enviar_email_a_toda_la_bbdd
    • procesar_pago
    • borrar_documentos
  El agente debe mostrar un resumen y pedir confirmación humana.
  (Ver módulo 7.3 — Permisología y HITL)

  SANITIZACIÓN DE INPUTS
  ─────────────────────────────────────────────────────────────
  Los parámetros que el LLM pasa a las tools pueden contener
  prompt injection de un usuario malicioso.
  Validar siempre: tipos, rangos, caracteres especiales.
  Nunca ejecutar SQL generado directamente por el LLM.

  LOGGING COMPLETO
  ─────────────────────────────────────────────────────────────
  Registrar cada llamada a una tool:
    • timestamp
    • agente que la llamó
    • nombre de la tool
    • parámetros de entrada
    • resultado devuelto
    • usuario que inició la sesión
  Retención mínima: 90 días.
```

### Matriz de riesgo de tools

| Tipo de acción | Riesgo | Requiere confirmación |
|----------------|--------|----------------------|
| Solo lectura (consultar, buscar) | Bajo | No |
| Escritura reversible (crear, actualizar) | Medio | Recomendado para cambios masivos |
| Escritura irreversible (borrar, enviar) | Alto | Siempre |
| Acción financiera (pagar, aprobar crédito) | Muy alto | Siempre + doble aprobación |

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Schick et al. (2023) — *Toolformer: Language Models Can Teach Themselves to Use Tools* → [arxiv.org/abs/2302.04761](https://arxiv.org/abs/2302.04761)
- Yao et al. (2022) — *ReAct: Synergizing Reasoning and Acting in Language Models* → [arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)

**Informes de industria:**
- McKinsey (anual) — *The State of AI* → [mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) *(tool-calling y function calling como base de la automatización agéntica empresarial)*

**Libros recomendados:**
- Iansiti & Lakhani (2020) — *Competing in the Age of AI* (HBR Press) — cómo los sistemas de herramientas conectadas a LLMs redefinen los procesos operativos

**Documentación oficial:**
- *Anthropic Documentation — Tool Use* → [docs.anthropic.com](https://docs.anthropic.com) *(referencia técnica completa para implementar tool-calling con Claude: schemas, tipos de retorno y manejo de errores)*

*Anterior: [7.1 Anatomía de un Agente IA](../7.1_anatomia_agente/README.md) | Siguiente: [7.3 Permisología y Human-in-the-Loop](../7.3_permisologia_hitl/README.md)*
