# 2.3 Selección Estratégica de Modelos

## 2.3.1 El Error Más Común: Usar Siempre el Modelo Más Potente

La mayoría de empresas que empiezan con IA usan GPT-4 o Claude Opus para absolutamente todo. Es el equivalente a contratar a un cirujano para poner tiritas — funciona, pero es un desperdicio sistemático.

La selección de modelo es una decisión de ingeniería con impacto directo en costes, velocidad y calidad. Un sistema bien diseñado usa **el modelo mínimo suficiente para cada tarea**.

```
Coste de procesar 1.000.000 tokens de input:
  Claude Haiku:   $0.80
  Claude Sonnet:  $3.00
  Claude Opus:    $15.00

Para una empresa con 500.000 tokens/día (volumen moderado):
  Todo en Opus:    $7.500/mes
  Optimizado:      $800-1.200/mes
  Ahorro:          ~$75.000/año
```

---

## 2.3.2 El Framework de Selección: 4 Ejes

### Eje 1 — Complejidad de la tarea

```
BAJA COMPLEJIDAD → modelos pequeños/rápidos
  · Clasificación de texto (spam, categoría, sentimiento)
  · Extracción de campos estructurados
  · Resumen de documentos cortos (<2.000 palabras)
  · Traducción estándar

MEDIA COMPLEJIDAD → modelos equilibrados
  · Redacción corporativa con estilo definido
  · Análisis de documentos medianos
  · Pipeline de preguntas sobre base documental
  · Generación de código estándar

ALTA COMPLEJIDAD → modelos avanzados
  · Razonamiento multi-paso con datos contradictorios
  · Análisis estratégico con múltiples variables
  · Código complejo con arquitectura no trivial
  · Negociación de instrucciones ambiguas y largas
```

### Eje 2 — Volumen y coste

```
< 10.000 llamadas/mes     → el coste del modelo es irrelevante, elige calidad
10.000 - 100.000/mes      → empieza a importar, evalúa Sonnet vs Haiku
> 100.000/mes             → el coste es un KPI, arquitectura híbrida obligatoria
```

### Eje 3 — Latencia requerida

```
Interactivo (<2s)   → Haiku, Sonnet — nunca Opus para respuesta en tiempo real
Batch (minutos)     → cualquier modelo, prioriza calidad sobre velocidad
Asíncrono (horas)   → Opus si la tarea lo justifica, batch API para volumen
```

### Eje 4 — Privacidad y localización

```
Datos públicos o anonimizados → cualquier API cloud
Datos sensibles (PII, salud)  → modelos on-premise (Llama, Mistral) o
                                 APIs con DPA y acuerdo de no-retención
Datos clasificados             → air-gapped, modelos locales únicamente
```

---

## 2.3.3 Comparativa Práctica: Cuándo Usar Cada Modelo

### Claude Haiku — El caballo de batalla

**Ideal para:**
- Clasificación y etiquetado a escala
- Extracción de datos de formularios y facturas
- Respuestas cortas en chatbots de soporte
- Resúmenes de tickets y emails
- Primer paso en pipelines de filtrado

**No usar para:**
- Razonamiento jurídico o financiero complejo
- Documentos con instrucciones ambiguas y largas
- Generación de código crítico sin revisión

### Claude Sonnet — El equilibrio óptimo

**Ideal para:**
- Redacción de documentos corporativos
- Análisis de contratos y reporting
- Asistentes conversacionales con contexto moderado
- Generación y revisión de código
- 80% de los casos de uso empresariales

**No usar para:**
- Tareas ultra-simples que Haiku resuelve igual
- Análisis estratégico de máxima profundidad (usa Opus puntualmente)

### Claude Opus — El especialista

**Ideal para:**
- Análisis estratégico con consecuencias altas
- Revisión de documentos legales o financieros críticos
- Razonamiento complejo con muchas variables
- Generación de contenido fundacional (syllabus, frameworks)

**No usar para:**
- Volumen alto — el coste lo hace inviable
- Tareas simples — no aporta valor adicional

---

## 2.3.4 Arquitectura Híbrida: el Patrón de Producción

La arquitectura más eficiente en producción no usa un solo modelo — usa una cascada.

```
PATRÓN CASCADA (Router → Worker → Validator)

Entrada
   │
   ▼
[ROUTER — Haiku]
  ¿Tarea simple o compleja?
   │                    │
   ▼                    ▼
[WORKER A           [WORKER B
 Haiku              Sonnet/Opus
 tareas simples]    tareas complejas]
   │                    │
   └────────┬───────────┘
            ▼
     [VALIDATOR — Haiku]
      ¿El output cumple el formato?
      ¿Hay campos null inesperados?
            │
            ▼
         Salida

Resultado: calidad de Opus donde importa, coste de Haiku en el 70% del volumen.
```

### Implementación del router

```python
def router_modelo(tarea: str) -> str:
    """
    Clasifica la complejidad de una tarea y devuelve el modelo adecuado.
    El propio router usa Haiku — la ironía funciona porque clasificar
    es exactamente la tarea en que Haiku destaca.
    """
    PALABRAS_COMPLEJIDAD_ALTA = [
        "estrategia", "legal", "contrato", "riesgo", "análisis financiero",
        "arquitectura", "decisión crítica", "due diligence"
    ]
    tarea_lower = tarea.lower()
    if any(p in tarea_lower for p in PALABRAS_COMPLEJIDAD_ALTA):
        return "claude-sonnet-4-6"
    return "claude-haiku-4-5-20251001"
```

---

## 2.3.5 Modelos Open Source: Cuándo Tiene Sentido

Los modelos open source (Llama 3, Mistral, Qwen) tienen ventajas reales en contextos específicos:

| Criterio | API Cloud | Open Source |
|---|---|---|
| Coste a escala muy alta | Variable (alto) | Fijo (infra propia) |
| Privacidad total | Depende del DPA | Garantizada |
| Latencia personalizable | No | Sí (hardware propio) |
| Fine-tuning sobre datos propios | Limitado | Total |
| Mantenimiento | Cero | Alto |
| Calidad en tareas generales | Superior | 70-85% de los SOTA |

**Cuándo considerar open source:**
- Volumen > 10M tokens/día (el break-even suele estar aquí)
- Datos que no pueden salir de la empresa por contrato
- Necesidad de fine-tuning con datos propios confidenciales
- Requisito de operación offline o air-gapped

**Cuándo NO:**
- Recursos de DevOps limitados
- Calidad crítica en tareas complejas
- Proyecto en fase de exploración o piloto

---

## 2.3.6 La Decisión en la Práctica: Árbol de Selección

```
¿Los datos son confidenciales y no pueden salir de la empresa?
  SÍ → Modelo on-premise (Llama 3, Mistral)
  NO ↓

¿El volumen es > 500.000 tokens/día?
  SÍ → Arquitectura híbrida con router
  NO ↓

¿La tarea requiere razonamiento complejo o tiene consecuencias altas?
  SÍ → Claude Sonnet (o Opus puntualmente)
  NO ↓

¿Es clasificación, extracción o resumen corto?
  SÍ → Claude Haiku
  NO → Claude Sonnet (por defecto seguro)
```

> **Regla de producción:** empieza con Sonnet para todo. Cuando el sistema funciona bien, identifica qué tareas Haiku resuelve igual de bien y migra esas. Nunca optimices el coste antes de validar la calidad.

---

---

## Fuentes y Referencias

**Papers y estudios:**
- OpenAI (2023) — *GPT-4 Technical Report* → [arxiv.org/abs/2303.08774](https://arxiv.org/abs/2303.08774)
- Liang et al. (2022) — *Holistic Evaluation of Language Models (HELM)* — Stanford CRFM; referencia para benchmarks comparativos de capacidades y fiabilidad entre modelos (disponible en crfm.stanford.edu/helm)

**Informes de industria:**
- Stanford University (anual) — *AI Index Report* → [aiindex.stanford.edu/report/](https://aiindex.stanford.edu/report/) *(comparativas de rendimiento y coste-eficiencia de modelos frontier a lo largo del tiempo)*
- Gartner — *Hype Cycle for Artificial Intelligence* → [gartner.com](https://www.gartner.com) *(posicionamiento de tecnologías LLM en el ciclo de madurez, útil para decisiones de selección)*

**Libros recomendados:**
- Iansiti & Lakhani (2020) — *Competing in the Age of AI* (HBR Press) — principios para tomar decisiones de arquitectura IA alineadas con la estrategia de negocio

**Documentación oficial:**
- *Anthropic Documentation — Models Overview* → [docs.anthropic.com](https://docs.anthropic.com) *(especificaciones, precios y casos de uso recomendados para cada versión de Claude)*

*Anterior: [2.2 Prompt Engineering de Producción](../2.2_prompt_engineering/README.md) | Siguiente: [3.1 Ingeniería de Outputs Corporativos](../../modulo_3/3.1_outputs_corporativos/README.md)*
