# 6.3 Monitoreo y Resiliencia de Sistemas IA en Producción

## 6.3.1 Por Qué los Sistemas IA se Degradan con el Tiempo

Un sistema de IA no es un software convencional. El código no cambia, pero el mundo cambia — y con él, el comportamiento del modelo. Esto se llama **drift** (deriva), y es el principal enemigo de un sistema IA en producción.

```
CAUSAS DE DEGRADACIÓN EN SISTEMAS IA:

  DRIFT DE DATOS (más común)
  ─────────────────────────────────────────────────────────────────
  Los inputs que recibe el sistema cambian respecto al entrenamiento.
  Ejemplo: un clasificador entrenado con emails pre-pandemia empieza a
  recibir emails sobre trabajo remoto y no los clasifica bien.

  DRIFT DE CONCEPTO
  ─────────────────────────────────────────────────────────────────
  El significado de "correcto" cambia aunque los datos no cambien.
  Ejemplo: la política de devoluciones cambia en noviembre pero el
  prompt del sistema no se actualiza hasta enero.

  DEGRADACIÓN DEL MODELO BASE
  ─────────────────────────────────────────────────────────────────
  El proveedor actualiza su modelo (Claude 3 → Claude 3.5).
  Comportamientos que funcionaban pueden variar sutilmente.

  CAMBIO EN EL VOLUMEN / DISTRIBUCIÓN
  ─────────────────────────────────────────────────────────────────
  En Black Friday el sistema recibe 10× el tráfico habitual.
  Los rate limits se disparan, la latencia se multiplica.

  INYECCIÓN ADVERSARIAL
  ─────────────────────────────────────────────────────────────────
  Usuarios malintencionados intentan manipular el sistema con
  inputs diseñados para evadir controles (prompt injection).
```

La analogía para directivos: **monitorear un sistema IA es como gestionar un empleado**, no como mantener una máquina. Necesita supervisión continua, feedback y ajustes periódicos, no solo un mantenimiento anual.

---

## 6.3.2 Stack de Monitoreo — Qué Medir y Cómo

Un sistema de monitoreo robusto cubre cuatro dimensiones:

```
LAS CUATRO DIMENSIONES DEL MONITOREO IA:

  1. OPERACIONAL (¿está funcionando?)
  ┌──────────────────────────────────────────────────────────────┐
  │  • Disponibilidad: uptime del sistema completo               │
  │  • Latencia: tiempo de respuesta P50, P95, P99               │
  │  • Tasa de error: % llamadas que fallan                      │
  │  • Throughput: llamadas/minuto que procesa                   │
  │  Herramientas: Datadog, Grafana, CloudWatch, Prometheus      │
  └──────────────────────────────────────────────────────────────┘

  2. DE CALIDAD (¿está respondiendo bien?)
  ┌──────────────────────────────────────────────────────────────┐
  │  • Score de calidad por muestreo humano (semanal)            │
  │  • Tasa de reclamaciones de usuarios                         │
  │  • % de outputs que pasan validación automática              │
  │  • Comparación A/B entre versiones de prompt                 │
  │  Herramientas: LangSmith, Weights & Biases, custom           │
  └──────────────────────────────────────────────────────────────┘

  3. DE NEGOCIO (¿está generando valor?)
  ┌──────────────────────────────────────────────────────────────┐
  │  • KPI del proceso que automatiza (tasa de conversión, etc.) │
  │  • Coste por transacción (tokens consumidos × precio)        │
  │  • ROI: ahorro de tiempo humano vs. coste API                │
  │  • Tasa de override humano (humano cambia la decisión IA)    │
  │  Herramientas: BI corporativo + logs estructurados           │
  └──────────────────────────────────────────────────────────────┘

  4. DE SEGURIDAD (¿está siendo explotado?)
  ┌──────────────────────────────────────────────────────────────┐
  │  • Detección de patrones de prompt injection                 │
  │  • Inputs anormalmente largos o con caracteres raros         │
  │  • Outputs que violan políticas (datos sensibles, sesgo)     │
  │  • Accesos fuera de horario o desde IPs no habituales        │
  │  Herramientas: WAF, logging estructurado, alertas regex      │
  └──────────────────────────────────────────────────────────────┘
```

### Dashboard ejecutivo recomendado

| Métrica | Verde | Amarillo | Rojo |
|---------|-------|----------|------|
| Uptime | > 99.5% | 98–99.5% | < 98% |
| Latencia P95 | < 3s | 3–8s | > 8s |
| Tasa de error | < 0.5% | 0.5–2% | > 2% |
| Score calidad (muestreo) | > 90% | 75–90% | < 75% |
| Coste por transacción | En presupuesto | +20% presupuesto | +50% presupuesto |
| Override humano | < 5% | 5–15% | > 15% |

---

## 6.3.3 Circuit Breakers — Protección ante Fallos en Cascada

El concepto de circuit breaker viene de la ingeniería eléctrica: un interruptor que corta la corriente cuando detecta sobrecarga, protegiendo el sistema completo.

```
PATRÓN CIRCUIT BREAKER PARA SISTEMAS IA:

  ESTADO CERRADO (normal)
  ┌──────────────────────────────────┐
  │  Todas las llamadas pasan al LLM │
  │  Contador de errores = 0         │
  │                                  │
  │  Si errores > umbral en ventana  │
  │  → ABRE el circuito              │
  └──────────────────────────────────┘
             │
             ▼ (demasiados errores)
  ESTADO ABIERTO (fallo)
  ┌──────────────────────────────────┐
  │  Llamadas NO van al LLM          │
  │  Sistema usa FALLBACK:           │
  │    • Respuesta predefinida       │
  │    • Reglas deterministas        │
  │    • Cola para procesar después  │
  │    • Escalada a humano           │
  │                                  │
  │  Después de timeout (ej: 60s)    │
  │  → pasa a SEMIABIERTO            │
  └──────────────────────────────────┘
             │
             ▼ (timeout expirado)
  ESTADO SEMIABIERTO (prueba)
  ┌──────────────────────────────────┐
  │  Deja pasar UNA llamada de prueba│
  │  Si tiene éxito → CIERRA         │
  │  Si falla → vuelve a ABRIR       │
  └──────────────────────────────────┘

  PARÁMETROS CONFIGURABLES:
    umbral_errores:  número de fallos para abrir (ej: 5 en 60s)
    timeout_abierto: tiempo antes de probar de nuevo (ej: 30s)
    umbral_exito:    éxitos necesarios para cerrar (ej: 2)
```

### Estrategias de fallback según criticidad del sistema

```
CRITICIDAD ALTA (decisiones financieras, médicas):
  Fallback → Escalada inmediata a humano
  No usar respuesta automatizada degradada
  SLA: resolución humana en < 4 horas

CRITICIDAD MEDIA (soporte al cliente, clasificación):
  Fallback → Respuesta genérica + ticket de seguimiento
  El cliente recibe confirmación, el equipo resuelve offline
  SLA: resolución en < 24 horas

CRITICIDAD BAJA (generación de contenido, resúmenes):
  Fallback → Cola de reintentos con backoff exponencial
  El usuario ve "procesando..." hasta que el sistema vuelva
  SLA: resolución en < 2 horas
```

---

## 6.3.4 SLAs para Sistemas IA — Cómo Negociarlos

Los SLAs (Service Level Agreements) para IA tienen particularidades que los SLAs de software tradicional no contemplan.

```
COMPONENTES DE UN SLA PARA SISTEMA IA:

  DISPONIBILIDAD
  ─────────────────────────────────────────────────────────────
  Definir qué cuenta como "disponible":
    ¿El sistema responde? ¿Con calidad aceptable?
  Fórmula: uptime = (minutos_disponible / minutos_periodo) × 100
  Recomendado: 99.5% mensual = máx 3.6 horas de caída/mes

  LATENCIA
  ─────────────────────────────────────────────────────────────
  Usar percentiles, no promedios:
    P50 (mediana): el usuario típico espera X segundos
    P95: el 95% de los usuarios espera menos de Y segundos
    P99: el 1% más lento espera menos de Z segundos
  Recomendado para IA conversacional: P95 < 5 segundos

  CALIDAD
  ─────────────────────────────────────────────────────────────
  El SLA más difícil de definir. Opciones:
    • % de outputs que superan validación automática (> 95%)
    • Score de satisfacción de usuarios (NPS > 40)
    • Tasa de reclamaciones (< 1% de interacciones)
  Revisión: evaluación mensual por muestreo (100 casos)

  COSTE
  ─────────────────────────────────────────────────────────────
  Presupuesto máximo de tokens por período
  Alertas automáticas al 70%, 90%, 100% del presupuesto
  Throttling automático al superar límite
```

### Matriz de responsabilidades en el SLA

| Responsable | Qué garantiza | Qué NO garantiza |
|-------------|---------------|-----------------|
| Equipo de IA interno | Disponibilidad de la integración, fallbacks | Comportamiento exacto del modelo |
| Proveedor LLM (Anthropic, etc.) | API disponible según sus propios SLAs | Resultados perfectos siempre |
| IT corporativo | Infraestructura de red, autenticación | Calidad de los prompts |
| Negocio (dueño del proceso) | Que los prompts reflejen la política actual | Velocidad de cambios |

---

## 6.3.5 Recuperación ante Fallos — Runbook Operacional

Un runbook es el procedimiento paso a paso que sigue el equipo cuando algo falla. Todo sistema IA en producción debe tenerlo.

```
RUNBOOK — SISTEMA IA DEGRADADO:

  NIVEL 1 — ALERTA AUTOMÁTICA (latencia > 5s o error rate > 2%)
  ┌─────────────────────────────────────────────────────────────┐
  │  1. Sistema activa fallback automático                      │
  │  2. Alerta a canal #alertas-ia (Slack/Teams)                │
  │  3. On-call técnico revisa dashboard (< 15 min)             │
  │  4. Si es problema del proveedor → esperar recuperación     │
  │  5. Si es problema propio → rollback al último despliegue   │
  └─────────────────────────────────────────────────────────────┘

  NIVEL 2 — DEGRADACIÓN DE CALIDAD (score < 75% en 24h)
  ┌─────────────────────────────────────────────────────────────┐
  │  1. Extraer muestra de 50 casos problemáticos               │
  │  2. Identificar patrón común (¿nuevo tipo de input?         │
  │     ¿cambio en los datos? ¿nueva versión del modelo?)       │
  │  3. Ajustar prompt o añadir ejemplos few-shot               │
  │  4. Test en staging con los casos fallidos                  │
  │  5. Desplegar con feature flag (10% → 50% → 100%)           │
  └─────────────────────────────────────────────────────────────┘

  NIVEL 3 — INCIDENTE DE SEGURIDAD (prompt injection detectada)
  ┌─────────────────────────────────────────────────────────────┐
  │  1. Desactivar el endpoint afectado INMEDIATAMENTE          │
  │  2. Preservar logs del incidente (no borrar)                │
  │  3. Notificar a DPO si hay datos personales involucrados    │
  │  4. Analizar el vector de ataque                            │
  │  5. Añadir validación de inputs                             │
  │  6. Reactivar con monitoreo intensivo (72h)                 │
  └─────────────────────────────────────────────────────────────┘
```

**Regla de oro para directivos**: el sistema de IA debe poder desactivarse en menos de 5 minutos sin impacto catastrófico en el negocio. Si no es posible, el proceso tiene demasiada dependencia y necesita un plan de continuidad más robusto.

```
CHECKLIST DE RESILIENCIA — ANTES DE IR A PRODUCCIÓN:

  ☐ Circuit breaker configurado con umbrales documentados
  ☐ Fallback probado (¿funciona el negocio sin la IA?)
  ☐ Alertas configuradas en todos los canales relevantes
  ☐ Runbook documentado y accesible para el equipo on-call
  ☐ Backups de prompts en control de versiones (Git)
  ☐ Prueba de carga realizada (¿aguanta el pico de Black Friday?)
  ☐ Tiempo de rollback medido y < 10 minutos
  ☐ SLAs acordados con todas las partes
  ☐ Plan de comunicación al cliente en caso de caída
  ☐ Revisión de seguridad: test de prompt injection completado
```

---

*Anterior: [6.2 IA como Motor de Decisión](../6.2_ia_motor_decision/README.md) | Siguiente: [7.1 Anatomía de un Agente IA](../../modulo_7/7.1_anatomia_agente/README.md)*
