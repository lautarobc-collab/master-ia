# 1.2 IA como Palanca Estratégica

## 1.2.1 Detectar Oportunidades Reales de IA en una Empresa

No toda tarea se beneficia de IA. El error más común en empresas es aplicar IA donde no aporta valor — o no aplicarla donde sí lo haría. El criterio de selección es técnico y económico a la vez.

### El filtro de las 4D

Una tarea es candidata real para IA si cumple al menos 3 de estas 4 condiciones:

| Condición | Pregunta clave | Ejemplo |
|---|---|---|
| **Data** | ¿Hay datos históricos o inputs estructurados? | Emails recibidos, informes pasados |
| **Dull** | ¿Es repetitiva y predecible? | Clasificar tickets de soporte |
| **Difficult** | ¿Requiere sintetizar mucha información? | Resumir 50 contratos |
| **Deadline** | ¿El tiempo de ejecución humana es el cuello de botella? | Reportes que tardan 3 días |

### Mapa de Oportunidades por Departamento

```
ALTA DIRECCIÓN
  ✓ Síntesis de informes ejecutivos (tiempo → minutos)
  ✓ Vigilancia competitiva automatizada
  ✓ Preparación de board decks desde datos raw

OPERACIONES
  ✓ Clasificación y enrutamiento de incidencias
  ✓ Generación de SOPs desde transcripciones
  ✓ Análisis de causas raíz en texto libre

RRHH
  ✓ Cribado semántico de CVs
  ✓ Generación de job descriptions coherentes
  ✓ Onboarding asistido por agente

FINANZAS
  ✓ Extracción de datos de facturas/contratos
  ✓ Narrativa automática de variaciones presupuestarias
  ✗ Auditoría formal (requiere firma humana)

LEGAL / COMPLIANCE
  ✓ Revisión preliminar de contratos (no vinculante)
  ✓ Síntesis de cambios normativos
  ✗ Consejo legal directo al cliente (riesgo regulatorio)
```

> **Regla práctica:** empieza por tareas donde el error tiene bajo coste y el volumen es alto. Nunca empieces por decisiones críticas e irreversibles.

---

## 1.2.2 Evaluación del Impacto y Priorización de Proyectos

### La Matriz de Priorización IA

Para priorizar qué proyectos acometer primero, evalúa cada iniciativa en dos ejes:

```
              ALTO IMPACTO
                    │
     Cuadrante 2    │    Cuadrante 1 ← EMPIEZA AQUÍ
     (planificar)   │    (quick wins)
                    │
─────────────────── ┼ ─────────────────── ALTA VIABILIDAD
                    │
     Cuadrante 4    │    Cuadrante 3
     (descartar)    │    (investigar)
                    │
              BAJO IMPACTO
```

**Métricas de impacto:**
- Horas/semana liberadas × coste hora
- Reducción de errores × coste por error
- Aceleración del ciclo de decisión

**Métricas de viabilidad:**
- ¿Hay datos disponibles y limpios?
- ¿Existe API o integración posible?
- ¿El equipo puede operar el sistema?

### Fórmula del ROI de IA

```
ROI = (Valor generado - Coste total) / Coste total × 100

Valor generado = (horas_ahorradas × coste_hora) + (errores_evitados × coste_error)
Coste total    = coste_desarrollo + coste_API_mensual + coste_mantenimiento
```

**Ejemplo real — Automatización de informes semanales:**
- Horas ahorradas: 8h/semana × 50€/h = 400€/semana = 20.800€/año
- Coste API (Claude Haiku): ~50€/mes = 600€/año
- Coste desarrollo (10h × 80€): 800€ (one-time)
- **ROI año 1:** (20.800 - 1.400) / 1.400 = **1.385%**

---

## 1.2.3 Niveles de Madurez en Adopción de IA

El modelo de madurez permite saber dónde está la empresa y qué hacer a continuación — no saltar niveles.

```
NIVEL 5 — IA Autónoma
  Agentes toman decisiones operativas sin intervención humana.
  Bucles de feedback continuos. IA mejora sola.

NIVEL 4 — IA Integrada
  IA embebida en procesos core. KPIs medidos en producción.
  Datos propios para fine-tuning o RAG.

NIVEL 3 — IA Departamental
  Varios departamentos con casos de uso en producción.
  Gobernanza básica. Métricas de calidad establecidas.

NIVEL 2 — IA Experimental  ← La mayoría de empresas medianas en 2024
  Pilotos aislados. Uso de herramientas SaaS (Copilot, ChatGPT).
  Sin integración en sistemas core. Sin medición de impacto.

NIVEL 1 — IA Consciente
  Exploración. Formación básica. Ningún proyecto en producción.
  "Sabemos que existe pero no sabemos cómo usarla."
```

**Diagnóstico rápido:** si tus equipos usan ChatGPT de forma individual y sin política, estás en Nivel 2. El salto a Nivel 3 requiere un caso de uso en producción con métricas.

---

## 1.2.4 Cómo Avanzar en el Roadmap de Adopción

### Roadmap tipo 12 meses (de Nivel 2 a Nivel 3-4)

```
MES 1-2:  DIAGNÓSTICO
  → Mapa de procesos candidatos (filtro 4D)
  → Inventario de datos disponibles
  → Evaluación de competencias del equipo

MES 3-4:  QUICK WIN
  → 1 caso de uso simple en producción
  → Métricas base establecidas
  → Aprendizaje del stack técnico

MES 5-6:  EXPANSIÓN
  → 2-3 casos de uso adicionales
  → Política de uso de IA redactada
  → Formación del equipo en prompting

MES 7-9:  INTEGRACIÓN
  → IA conectada a sistemas existentes (CRM, ERP, BI)
  → RAG sobre base documental interna
  → Dashboard de KPIs de IA

MES 10-12: ESCALA
  → Agentes departamentales
  → Medición de ROI por iniciativa
  → Presentación a board con resultados
```

---

## 1.2.5 Barreras Comunes: Cultura, Talento, Datos y Tecnología

### Las 4 barreras y cómo superarlas

**1. Cultura — "No confío en lo que genera la IA"**
- Raíz: falta de comprensión del funcionamiento real
- Solución: demostrar con casos concretos del sector. Formación práctica, no teórica.
- Señal de superación: el equipo usa IA y lo reporta abiertamente

**2. Talento — "No tenemos perfiles técnicos"**
- Raíz: confusión entre usar IA y construir IA
- Solución: el 80% de los casos de uso se implementan con APIs, sin ML nativo.
  Un perfil de operaciones con Python básico y prompting puede construir la mayoría.
- Señal de superación: primer prototipo construido por equipo interno

**3. Datos — "Nuestros datos están en Excel y PDFs"**
- Raíz: subestimar las capacidades de extracción y procesamiento actuales
- Solución: los LLMs leen PDFs, tablas y texto no estructurado nativamente.
  El problema real suele ser privacidad, no formato.
- Señal de superación: primer pipeline de ingesta de documentos internos

**4. Tecnología — "No sabemos qué herramientas elegir"**
- Raíz: el mercado cambia cada 3 meses y hay parálisis por análisis
- Solución: regla del 80/20 — Claude/GPT-4 + un vector store (Chroma/Pinecone) + orquestador (LangChain/n8n) cubre el 80% de casos empresariales.
- Señal de superación: primer stack definido y documentado

---

*Anterior: [1.1 Panorama de la IA](../1.1_panorama_ia/README.md) | Siguiente: [1.3 Construcción del Caso de Negocio](../1.3_caso_negocio/README.md)*
