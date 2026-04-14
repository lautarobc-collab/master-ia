# 1.3 Construcción del Caso de Negocio para IA

## 1.3.1 Qué es un Caso de Negocio y por qué es imprescindible

Un caso de negocio (*business case*) de IA no es un documento técnico — es el argumento financiero y estratégico que justifica invertir recursos en una iniciativa concreta. Sin él, los proyectos de IA mueren en la fase de piloto por falta de presupuesto o de apoyo directivo.

### La brecha entre entusiasmo y aprobación

```
Lo que ocurre sin caso de negocio:

  Equipo técnico          Dirección
  ─────────────           ─────────────
  "La IA puede            "¿Cuánto cuesta?
  hacerlo"                ¿Cuánto ganamos?
                          ¿En cuánto tiempo?"
         │                     │
         └─────── SILENCIO ─────┘
                  Proyecto bloqueado
```

Un caso de negocio bien construido traduce el potencial técnico al lenguaje que importa a quien toma la decisión: **euros, tiempo y riesgo**.

### Los 5 componentes de un caso de negocio sólido

| Componente | Pregunta que responde | Ejemplo |
|---|---|---|
| **Problema** | ¿Qué duele hoy? | Informes tardando 3 días, 12h/semana |
| **Solución propuesta** | ¿Qué hacemos exactamente? | Pipeline IA que genera informe en 10 min |
| **Impacto cuantificado** | ¿Cuánto vale en €? | 28.800€/año en tiempo ahorrado |
| **Inversión requerida** | ¿Cuánto cuesta? | 2.000€ desarrollo + 60€/mes API |
| **Riesgos y mitigaciones** | ¿Qué puede fallar? | Calidad outputs → validación humana en ciclo |

---

## 1.3.2 Estructura del Documento: de la Portada al Apéndice

Un caso de negocio estándar para una iniciativa de IA media (no un proyecto de millones) se estructura en 6 secciones:

### Sección 1 — Resumen Ejecutivo (max. 1 página)
Escrito para quien no leerá el resto. Debe contener:
- El problema en 2 frases
- La solución propuesta en 1 frase
- Los 3 números clave: inversión, ahorro anual, ROI
- La decisión que se solicita (presupuesto, equipo, plazo)

> **Regla de oro:** si el resumen ejecutivo no convence, el documento no se lee. Escríbelo al final, cuando ya tienes todos los datos.

### Sección 2 — Descripción del Problema Actual
No describas la IA todavía. Aquí describes el dolor actual con datos:
- ¿Cuántas horas se invierten en el proceso?
- ¿Con qué frecuencia ocurren errores y qué cuestan?
- ¿Qué impacto tiene en el cliente, en el equipo, en el resultado?

```
Ejemplo — Proceso de cribado de CVs (RRHH):
  · Volumen: 80-120 CVs por vacante
  · Tiempo actual: 3h por técnico de selección × 4 vacantes/mes = 12h/mes
  · Coste: 12h × 35€/h = 420€/mes = 5.040€/año
  · Problema añadido: inconsistencia en criterios entre evaluadores
  · Impacto: time-to-hire 18 días promedio (benchmark sector: 12 días)
```

### Sección 3 — Solución Propuesta
Describe la solución técnica a nivel comprensible para no técnicos:
- Qué herramientas se usan (sin jerga innecesaria)
- Cómo funciona el flujo paso a paso
- Qué hace la IA y qué sigue haciendo el humano (HITL)
- Qué datos necesita y de dónde vienen

### Sección 4 — Análisis Financiero
Es el núcleo del caso de negocio. Tres tablas obligatorias:

**Tabla de inversión:**
```
INVERSIÓN
  Desarrollo (horas internas o externas)  ___€  [one-time]
  Infraestructura / setup                 ___€  [one-time]
  Licencias / API (mensual × 12)          ___€  [recurrente]
  Formación del equipo                    ___€  [one-time]
  ──────────────────────────────────────────────
  TOTAL AÑO 1                             ___€
  TOTAL AÑO 2+ (solo recurrente)          ___€
```

**Tabla de beneficios:**
```
BENEFICIOS ANUALES
  Ahorro en horas (h/año × €/h)           ___€
  Reducción de errores (N × €/error)      ___€
  Aceleración de ciclo (impacto en KPI)   ___€  [si aplica]
  ──────────────────────────────────────────────
  TOTAL BENEFICIO ANUAL                   ___€
```

**Resumen ROI:**
```
ROI AÑO 1 = (Beneficio - Inversión año 1) / Inversión año 1
ROI AÑO 2 = (Beneficio - Coste recurrente) / Coste recurrente
Payback    = Inversión one-time / Beneficio mensual neto
```

### Sección 5 — Plan de Implementación
Cronograma realista en fases. Nunca más de 3 fases para proyectos de menos de 6 meses:

```
FASE 1 — Prototipo (semanas 1-3)
  · Desarrollar pipeline básico
  · Validar con muestra de 20 casos reales
  · Criterio de go/no-go: precisión > 85%

FASE 2 — Piloto controlado (semanas 4-8)
  · Despliegue en 1 departamento
  · Métricas en producción
  · Ajustes de prompt y flujo

FASE 3 — Escala (semanas 9-12)
  · Rollout al resto de departamentos
  · Formación de usuarios finales
  · Documentación y handoff
```

### Sección 6 — Riesgos y Mitigaciones
Muestra que has pensado en lo que puede fallar. Esto genera confianza, no inseguridad.

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Calidad de outputs insuficiente | Media | Alto | Revisión humana obligatoria en ciclo |
| Cambio de precios de API | Baja | Medio | Cláusula de revisión a 6 meses |
| Adopción baja del equipo | Media | Alto | Formación + quick wins visibles |
| Fuga de datos sensibles | Baja | Muy alto | Datos anonimizados, acuerdo DPA con proveedor |

---

## 1.3.3 Cómo Cuantificar el Impacto: Técnicas de Estimación

El mayor error en un caso de negocio es no cuantificar, el segundo mayor es inventar números sin base. Estas técnicas permiten estimar con rigor aunque no tengas datos perfectos.

### Técnica 1 — Cronometraje de referencia
Si no tienes datos históricos del proceso, cronometra manualmente una muestra pequeña:
- 10 casos reales son suficientes para estimar la media
- Multiplica por frecuencia mensual → tiempo total mensual
- Asigna coste hora según perfil

### Técnica 2 — Triangulación por benchmarks sectoriales
Si no puedes medir, busca benchmarks del sector:
- "Coste por ticket de soporte" varía entre 2-15€ según canal
- "Time-to-hire" promedio en España: 28 días (LinkedIn Talent Insights)
- "Coste de error en facturación": 1-3% del importe facturado

### Técnica 3 — Estimación conservadora / optimista / probable
Nunca uses un solo escenario. Presenta tres:

```
                  Conservador   Probable   Optimista
Horas ahorradas/sem:    3h          6h         9h
Coste/hora:            35€         45€         55€
Ahorro anual:        5.040€     12.960€     23.760€

→ Usa el escenario PROBABLE en el resumen ejecutivo
→ Presenta el CONSERVADOR como suelo garantizado
→ El OPTIMISTA muestra el techo si todo funciona
```

### Técnica 4 — Valor de la aceleración (time-to-value)
Cuando la IA acelera un ciclo (ventas, contratación, cierre de proyectos), el valor no es solo el ahorro en horas — es el ingreso adelantado:

```
Ejemplo: acortar ciclo de venta de 30 a 22 días
  · 8 días ganados × 5 deals/mes × ticket medio 3.000€
  · Si el 10% de deals se caen por velocidad del competidor:
    0.5 deals/mes × 3.000€ = 1.500€/mes = 18.000€/año en deals rescatados
```

---

## 1.3.4 Presentación a Dirección: el Pitch de 5 Minutos

El documento escrito abre la puerta — la reunión la cierra. Estructura el pitch en 5 bloques de 1 minuto cada uno:

```
MINUTO 1 — El Problema
  "Hoy [proceso X] nos cuesta [Y horas / Z€] al mes.
   Además genera [consecuencia tangible: errores, retrasos, fricción]."

MINUTO 2 — La Solución
  "Proponemos automatizar [parte concreta] con IA.
   El sistema hace [A], el equipo sigue haciendo [B]."

MINUTO 3 — Los Números
  "La inversión es de [X€]. El ahorro anual estimado es [Y€].
   El ROI es del [Z%] con payback en [N meses]."

MINUTO 4 — El Plan
  "En 12 semanas tendríamos el sistema en producción.
   Necesitamos [recurso concreto: N horas de IT, presupuesto de X€]."

MINUTO 5 — La Decisión
  "¿Nos autorizáis a proceder con la Fase 1 (prototipo)?
   Inversión inicial: [X€]. Criterio de go: [métrica concreta]."
```

> **Tip de presentación:** lleva siempre un ejemplo en vivo o una demo grabada. Un output real de la IA vale más que diez diapositivas.

---

## 1.3.5 Plantilla Reutilizable: el Canvas del Caso de Negocio IA

Una página, todos los elementos esenciales:

```
╔══════════════════════════════════════════════════════════════╗
║              CANVAS — CASO DE NEGOCIO IA                     ║
╠══════════════════╦═══════════════════════════════════════════╣
║ PROBLEMA         ║ SOLUCIÓN                                  ║
║ ─────────────    ║ ──────────────────────────────────────    ║
║ Proceso:         ║ Herramienta:                              ║
║ Coste actual:    ║ Flujo:                                    ║
║ Frecuencia:      ║ Human-in-the-loop:                        ║
╠══════════════════╬═══════════════════════════════════════════╣
║ IMPACTO          ║ INVERSIÓN                                 ║
║ ─────────────    ║ ──────────────────────────────────────    ║
║ Ahorro h/año:    ║ Desarrollo (one-time):                    ║
║ Valor €/año:     ║ API/licencia (mensual):                   ║
║ ROI estimado:    ║ Total año 1:                              ║
║ Payback:         ║ Total año 2+:                             ║
╠══════════════════╩═══════════════════════════════════════════╣
║ RIESGOS TOP 3          DECISIÓN QUE SE SOLICITA              ║
║ 1.                     Presupuesto: ___€                     ║
║ 2.                     Equipo:                               ║
║ 3.                     Plazo inicio:                         ║
╚══════════════════════════════════════════════════════════════╝
```

---

*Anterior: [1.2 IA como Palanca Estratégica](../1.2_ia_palanca_estrategica/README.md) | Siguiente: [2.1 Arquitectura Conceptual de los LLMs](../../modulo_2/2.1_arquitectura_llms/README.md)*
