# 7.3 Permisología y Human-in-the-Loop

## 7.3.1 El Espectro de Autonomía — Cuándo el Agente Decide Solo

Uno de los errores más comunes al desplegar agentes IA es asignarles o demasiada o demasiada poca autonomía. Demasiada autonomía genera riesgos incontrolados; demasiada poca hace que el sistema no aporte valor.

```
ESPECTRO DE AUTONOMÍA EN AGENTES IA:

  NIVEL 0 — AUTOMATIZACIÓN TOTAL
  ┌──────────────────────────────────────────────────────────────┐
  │  El agente actúa sin ninguna supervisión humana.             │
  │  Apropiado para: tareas de muy bajo riesgo y alto volumen.  │
  │  Ejemplo: clasificar emails entrantes como spam/no spam     │
  │  Ejemplo: formatear documentos según plantilla              │
  │  Riesgo si se abusa: acción masiva incorrecta difícil de    │
  │  revertir (ej: marcar como spam emails legítimos)           │
  └──────────────────────────────────────────────────────────────┘

  NIVEL 1 — SUPERVISIÓN LIGERA
  ┌──────────────────────────────────────────────────────────────┐
  │  El agente actúa y notifica. El humano puede intervenir.    │
  │  Apropiado para: procesos repetitivos con impacto moderado. │
  │  Ejemplo: el agente registra interacciones en CRM y envía   │
  │  un resumen diario al comercial para revisión              │
  │  El humano no aprueba cada acción, pero puede corregir.     │
  └──────────────────────────────────────────────────────────────┘

  NIVEL 2 — APROBACIÓN PARA ACCIONES CRÍTICAS
  ┌──────────────────────────────────────────────────────────────┐
  │  El agente planifica y propone; el humano aprueba antes     │
  │  de acciones de alto impacto.                               │
  │  Ejemplo: el agente prepara el email de oferta al cliente;  │
  │  el comercial lo revisa y aprueba antes de enviarlo        │
  │  Apropiado para: comunicaciones externas, cambios en BD     │
  └──────────────────────────────────────────────────────────────┘

  NIVEL 3 — COPILOTO (el humano siempre en control)
  ┌──────────────────────────────────────────────────────────────┐
  │  El agente asiste y recomienda; el humano ejecuta.          │
  │  Ejemplo: el agente analiza y sugiere "acepta esta oferta"; │
  │  el humano hace clic en "Aceptar" manualmente.              │
  │  Apropiado para: decisiones con consecuencias legales       │
  │  o financieras significativas.                              │
  └──────────────────────────────────────────────────────────────┘
```

**Principio para directivos**: el nivel de autonomía debe correlacionar con la reversibilidad de la acción y el coste del error. No es lo mismo equivocarse en un resumen interno (fácil de corregir) que en un email a 10.000 clientes (irreversible y costoso).

---

## 7.3.2 Diseño del Sistema de Aprobación Humana

El Human-in-the-Loop (HITL) no es solo un botón de "aprobar". Es un sistema completo que debe diseñarse cuidadosamente para que sea usable.

```
ANATOMÍA DE UN SISTEMA HITL BIEN DISEÑADO:

  CUANDO EL AGENTE NECESITA APROBACIÓN:
  ┌──────────────────────────────────────────────────────────────┐
  │  1. CONTEXTO: ¿Qué ha pasado hasta ahora?                   │
  │     "Procesando la solicitud de devolución de María López.  │
  │      Detecté que lleva 8 días fuera del plazo de 30 días."  │
  │                                                              │
  │  2. ANÁLISIS: ¿Qué encontró el agente?                      │
  │     "La cliente lleva 3 años con nosotros, 47 pedidos,      │
  │      solo 2 devoluciones previas. El motivo es razonable." │
  │                                                              │
  │  3. RECOMENDACIÓN: ¿Qué propone el agente?                  │
  │     "Recomiendo APROBAR la excepción. Probabilidad de       │
  │      fidelidad alta si resolvemos positivamente."           │
  │                                                              │
  │  4. OPCIONES: ¿Qué puede hacer el humano?                   │
  │     [✓ APROBAR] [✗ RECHAZAR] [~ APROBAR con cupón] [→ MÁS INFO]│
  │                                                              │
  │  5. CONSECUENCIAS: ¿Qué pasa con cada opción?               │
  │     "Si apruebas: procesamos devolución de 89€ hoy."       │
  │     "Si rechazas: enviamos email con código de cupón 10%."  │
  └──────────────────────────────────────────────────────────────┘
```

### Qué hace que un HITL sea malo

```
ANTIPATRONES DE HUMAN-IN-THE-LOOP:

  "Aprueba esto"
  ─────────────────────────────────────────────────────────────
  Sin contexto, sin análisis, sin opciones.
  El humano no entiende qué está aprobando.
  Consecuencia: aprueba todo sin leer → el HITL no sirve de nada.

  Flujo de aprobación con 7 pasos
  ─────────────────────────────────────────────────────────────
  Demasiado fricción → los aprobadores hacen clic en "aprobar"
  automáticamente para salir del flujo.
  El HITL se convierte en teatro, no en control real.

  Notificaciones sin urgencia diferenciada
  ─────────────────────────────────────────────────────────────
  Todo llega al mismo canal con la misma prioridad.
  Lo urgente se pierde entre lo rutinario.
  El agente espera sin límite de tiempo.

  Sin timeout
  ─────────────────────────────────────────────────────────────
  Si el aprobador no responde, el proceso se bloquea.
  Necesario definir: ¿qué pasa si nadie responde en 4 horas?
  (escalada, acción por defecto, notificación alternativa)
```

---

## 7.3.3 Mapa de Permisología — Qué Puede Hacer Cada Agente

La permisología define qué acciones puede ejecutar cada agente. Debe ser explícita, documentada y revisada periódicamente.

```
EJEMPLO DE MAPA DE PERMISOLOGÍA — EMPRESA DE SERVICIOS:

  AGENTE DE SOPORTE AL CLIENTE
  ─────────────────────────────────────────────────────────────
  PUEDE (autonomía nivel 0):
    ✓ Leer datos del cliente en CRM
    ✓ Consultar estado de pedidos
    ✓ Buscar en base de conocimiento
    ✓ Clasificar y priorizar tickets

  PUEDE CON NOTIFICACIÓN (nivel 1):
    ✓ Registrar interacciones en CRM
    ✓ Enviar emails de confirmación de ticket
    ✓ Escalar ticket a otro departamento

  NECESITA APROBACIÓN (nivel 2):
    ⚑ Emitir reembolso (hasta 100€)
    ⚑ Cambiar estado de pedido
    ⚑ Enviar comunicación personalizada al cliente

  NUNCA PUEDE (bloqueado en código):
    ✗ Emitir reembolso > 100€ (requiere supervisor)
    ✗ Acceder a datos financieros de otros clientes
    ✗ Modificar precios
    ✗ Borrar registros del CRM
    ✗ Enviar emails masivos

  AGENTE COMERCIAL
  ─────────────────────────────────────────────────────────────
  PUEDE (autonomía nivel 0):
    ✓ Buscar información de contactos y empresas
    ✓ Consultar catálogo y precios estándar
    ✓ Generar borradores de propuestas

  PUEDE CON NOTIFICACIÓN (nivel 1):
    ✓ Actualizar etapas del pipeline
    ✓ Programar recordatorios de seguimiento

  NECESITA APROBACIÓN (nivel 2):
    ⚑ Enviar propuesta comercial (aprueba el comercial responsable)
    ⚑ Aplicar descuento (aprueba manager de ventas)

  NUNCA PUEDE:
    ✗ Firmar contratos en nombre de la empresa
    ✗ Acceder a datos de clientes de otros comerciales
    ✗ Modificar datos bancarios de clientes
```

---

## 7.3.4 Auditoría de Acciones del Agente

Toda acción ejecutada por un agente debe ser trazable. La auditoría no es opcional — es un requisito legal (AI Act, GDPR) y operacional.

```
ESTRUCTURA DE UN LOG DE AUDITORÍA:

  {
    "id_log": "LOG-20250506-001234",
    "timestamp": "2025-05-06T14:32:11Z",
    "agente_id": "agente-soporte-v2.1",
    "sesion_id": "SES-abc123",
    "usuario_humano": "maria.garcia@empresa.com",
    
    "accion": {
      "tipo": "tool_use",
      "tool": "emitir_reembolso",
      "parametros": {
        "id_pedido": "PED-98765",
        "importe": 89.50,
        "motivo": "producto defectuoso"
      }
    },
    
    "decision_hitl": {
      "requerida": true,
      "solicitada_a": "supervisor@empresa.com",
      "decision": "APROBADO",
      "aprobado_por": "carlos.lopez@empresa.com",
      "timestamp_decision": "2025-05-06T14:45:22Z",
      "tiempo_espera_segundos": 791
    },
    
    "resultado": {
      "exito": true,
      "id_transaccion": "TXN-456789",
      "mensaje": "Reembolso procesado correctamente"
    },
    
    "contexto_llm": {
      "modelo": "claude-haiku-4-5-20251001",
      "tokens_input": 1243,
      "tokens_output": 87,
      "razonamiento_resumen": "Cliente con historial positivo, motivo válido, dentro del límite de autonomía"
    }
  }
```

### Checklist de auditoría operacional

| Aspecto | Mínimo recomendado |
|---------|-------------------|
| Retención de logs | 2 años (GDPR) / 5 años (finanzas) |
| Búsqueda en logs | Por cliente, agente, fecha, tipo de acción |
| Alertas automáticas | Acciones fuera de horario, volumen anormal |
| Revisión periódica | Muestra mensual de 50 logs aleatorios |
| Acceso a logs | Solo rol de compliance/IT, no el agente mismo |
| Integridad | Logs firmados o en sistema inmutable |

---

## 7.3.5 Escalada — El Mapa de Quién Decide Qué

```
ÁRBOL DE ESCALADA — AGENTE DE SOPORTE:

  Consulta estándar
  → Agente resuelve autónomamente

  Reclamación moderada (reembolso < 100€)
  → Agente propone → aprobación del agente de soporte senior (HITL 2)

  Reclamación compleja (reembolso > 100€, amenaza legal)
  → Agente prepara resumen → escala a supervisor humano (HITL 3)
  → SLA: supervisor responde en < 4 horas laborables

  Incidente de seguridad o datos personales
  → Agente DETIENE toda acción → alerta inmediata al DPO
  → No continúa hasta resolución humana

  Cliente VIP (contrato > 50K€/año)
  → Siempre escalar a account manager responsable
  → Incluso para consultas que podrían resolverse automáticamente

  REGLA DE ORO:
  Si el agente tiene dudas sobre si escalar → escala.
  Mejor escalar de más que equivocarse en una acción irreversible.
```

**Para diseñar el árbol de escalada**: mapear los tipos de situaciones con el equipo de negocio, definir el SLA de respuesta humana para cada nivel y asegurarse de que siempre hay alguien disponible para responder (no solo un email genérico sin SLA).

---

*Anterior: [7.2 Tool-Calling y Herramientas](../7.2_tool_calling/README.md) | Siguiente: [8.1 Visión por IA](../../modulo_8/8.1_vision_ia/README.md)*
