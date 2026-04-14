# 6.2 IA como Motor de Decisión

## 6.2.1 Del Juicio Humano a la Decisión Automatizada

Durante décadas, las decisiones de negocio críticas — conceder un crédito, aprobar una devolución, priorizar una oportunidad — han dependido exclusivamente del juicio humano. Los sistemas de reglas (IF-THEN) fueron el primer intento de automatización, pero resultaron frágiles ante la complejidad del mundo real.

La IA como motor de decisión combina lo mejor de ambos mundos: la consistencia y velocidad de las reglas con la capacidad de los modelos de lenguaje para leer contexto, detectar matices y explicar su razonamiento.

```
EVOLUCIÓN DE LOS SISTEMAS DE DECISIÓN:

  GENERACIÓN 1 — REGLAS PURAS (1980-2000)
  ┌─────────────────────────────────────────────────────────┐
  │  IF ingresos > 3000 AND historial == "limpio"           │
  │    THEN aprobar crédito                                 │
  │  Ventaja: predecible, auditable                         │
  │  Problema: frágil, no captura matices                   │
  └─────────────────────────────────────────────────────────┘

  GENERACIÓN 2 — ML CLÁSICO (2000-2020)
  ┌─────────────────────────────────────────────────────────┐
  │  Modelos: regresión logística, random forest, XGBoost   │
  │  Ventaja: aprende de datos, más preciso                 │
  │  Problema: caja negra, requiere datos etiquetados       │
  └─────────────────────────────────────────────────────────┘

  GENERACIÓN 3 — IA + LLM (2023→)
  ┌─────────────────────────────────────────────────────────┐
  │  Reglas duras + scoring ML + razonamiento LLM           │
  │  Ventaja: contexto completo, explicable, adaptable      │
  │  Problema: latencia, coste por llamada, trazabilidad    │
  └─────────────────────────────────────────────────────────┘
```

La clave para directivos: **la IA no elimina las reglas de negocio, las enriquece**. El árbol de decisión corporativo sigue existiendo; la IA actúa como un analista experto que evalúa los casos en los que las reglas solas no son suficientes.

---

## 6.2.2 Arquitectura de un Motor de Decisión con IA

Un motor de decisión bien diseñado tiene tres capas:

```
ARQUITECTURA — MOTOR DE DECISIÓN CON IA:

  ┌────────────────────────────────────────────────────────────────┐
  │  CAPA 1 — FILTROS DUROS (reglas inmutables)                   │
  │  ─────────────────────────────────────────────────────────     │
  │  • Requisitos legales: mayor de edad, no sancionado            │
  │  • Límites de negocio: importe máximo, zona geográfica         │
  │  • Bloqueos automáticos: fraude confirmado, impago activo      │
  │                                                                │
  │  Si NO pasa → RECHAZO AUTOMÁTICO (sin IA)                     │
  └──────────────────────────┬─────────────────────────────────────┘
                             │ Pasa filtros
                             ▼
  ┌────────────────────────────────────────────────────────────────┐
  │  CAPA 2 — SCORING NUMÉRICO (modelos ML / reglas ponderadas)   │
  │  ─────────────────────────────────────────────────────────     │
  │  • Puntuación 0–100 basada en atributos cuantitativos          │
  │  • Zona verde (>75): aprobación automática                     │
  │  • Zona roja (<30): rechazo automático                         │
  │  • Zona gris (30–75): pasa a revisión IA                       │
  └──────────────────────────┬─────────────────────────────────────┘
                             │ Zona gris
                             ▼
  ┌────────────────────────────────────────────────────────────────┐
  │  CAPA 3 — RAZONAMIENTO IA (LLM con contexto completo)         │
  │  ─────────────────────────────────────────────────────────     │
  │  • Analiza contexto cualitativo (notas, historial, incidencias)│
  │  • Aplica política corporativa en lenguaje natural             │
  │  • Devuelve: decisión + puntuación ajustada + justificación    │
  │  • Casos complejos → escala a humano con resumen               │
  └──────────────────────────────────────────────────────────────────┘
```

### El principio del "Semáforo de Decisión"

| Zona | Score | Acción | Tiempo de respuesta |
|------|-------|--------|-------------------|
| Verde | > 75 | Aprobación automática | < 1 segundo |
| Amarillo | 30–75 | Revisión por IA → decisión justificada | 2–5 segundos |
| Rojo | < 30 | Rechazo automático con código de razón | < 1 segundo |
| Negro | Flags especiales | Escalada inmediata a analista humano | Tiempo humano |

---

## 6.2.3 Scoring Automatizado — Diseño Práctico

El scoring es el corazón cuantitativo del motor. Antes de involucrar a la IA, conviene calcular una puntuación numérica que capture los factores objetivos.

```
EJEMPLO — SCORING DE SOLICITUD DE CRÉDITO:

  Factor                          Peso    Cálculo
  ─────────────────────────────────────────────────────────
  Antigüedad como cliente          20%    años × 4 (máx 20)
  Ratio deuda/ingresos             25%    (1 - ratio) × 25
  Historial de pagos               25%    pagos_a_tiempo/total × 25
  Sector del negocio               15%    tabla de riesgo sectorial
  Importe solicitado vs. límite    15%    (1 - importe/límite) × 15
  ─────────────────────────────────────────────────────────
  TOTAL                           100%    0 — 100 puntos

  Ajustes automáticos:
    -20 pts → impago en los últimos 6 meses
    -15 pts → cambio de sector en los últimos 3 meses
    +10 pts → cliente premium (volumen > 50K€/año)
    +5  pts → recomendado por cliente existente
```

**Cómo define el negocio los umbrales**: los umbrales (30, 75) no son mágicos. Se calibran mirando el histórico de decisiones humanas y el resultado posterior (¿cuántos créditos con score 70 resultaron en impago?). Revisión semestral obligatoria.

```python
# Ejemplo de función de scoring en Python
def calcular_score(cliente):
    score = 0
    # Antigüedad (máx 20 pts)
    score += min(cliente["anos_cliente"] * 4, 20)
    # Ratio deuda/ingresos (máx 25 pts)
    ratio = cliente["deuda_total"] / max(cliente["ingresos_anuales"], 1)
    score += max(0, (1 - ratio) * 25)
    # Historial pagos (máx 25 pts)
    if cliente["total_pagos"] > 0:
        score += (cliente["pagos_a_tiempo"] / cliente["total_pagos"]) * 25
    # Penalizaciones
    if cliente["impago_reciente"]:
        score -= 20
    # Bonus
    if cliente["cliente_premium"]:
        score += 10
    return round(max(0, min(100, score)), 1)
```

---

## 6.2.4 Árbol de Decisión con IA — Casos Reales

La IA añade más valor en los casos que las reglas no pueden resolver bien: contexto narrativo, excepciones justificadas, combinaciones atípicas de factores.

```
ÁRBOL DE DECISIÓN — APROBACIÓN DE DEVOLUCIÓN (e-commerce):

  ¿Producto recibido?
  ├─ NO → Investigar incidencia logística → Reenvío automático
  └─ SÍ
     ├─ ¿Dentro del plazo de devolución (30 días)?
     │  ├─ SÍ → ¿Motivo?
     │  │       ├─ Defecto de fábrica → Devolución inmediata ✓
     │  │       ├─ No cumple expectativas → Score cliente
     │  │       │   ├─ Score > 60 → Aprobación automática
     │  │       │   └─ Score ≤ 60 → Revisión IA con contexto
     │  │       └─ Arrepentimiento → Política estándar
     │  └─ NO → ¿Fuera de plazo?
     │          ├─ < 45 días + cliente VIP → IA evalúa excepción
     │          └─ > 45 días → Rechazo con alternativa (cupón)
     └─ ¿Historial de abusos?
        ├─ > 3 devoluciones/año → Flag → Revisión humana
        └─ Normal → Flujo estándar
```

### Prompt de decisión IA (ejemplo real)

```
Eres el motor de decisión de devoluciones de [Empresa].
Política: hasta 30 días sin preguntas para clientes con score ≥ 60.

Caso:
- Cliente: 2 años, 47 pedidos, 2 devoluciones previas (ambas legítimas)
- Solicitud: devolución día 38 (fuera de plazo 8 días)
- Motivo declarado: "el producto llegó dañado, tardé en abrir el paquete"
- Adjunta foto de daño

Analiza y decide:
1. DECISIÓN: [APROBAR / RECHAZAR / ESCALAR]
2. JUSTIFICACIÓN: (máx. 2 frases)
3. ACCIÓN: acción concreta a ejecutar
4. NOTA_CLIENTE: mensaje para enviar al cliente (tono empático)
```

---

## 6.2.5 Gobernanza y Auditoría de Decisiones Automatizadas

Automatizar decisiones conlleva responsabilidad. En Europa, el AI Act y el GDPR exigen que las decisiones automatizadas que afectan a personas sean explicables, auditables y con posibilidad de revisión humana.

```
CHECKLIST DE GOBERNANZA — MOTOR DE DECISIÓN IA:

  TRAZABILIDAD
  ☐ Cada decisión almacenada con: timestamp, inputs, score, salida IA, acción
  ☐ Log inmutable (no editable retroactivamente)
  ☐ Retención mínima según normativa (recomendado: 5 años para crédito)

  EXPLICABILIDAD
  ☐ El cliente puede solicitar explicación de una decisión desfavorable
  ☐ La IA siempre genera justificación en lenguaje natural
  ☐ Los factores de scoring son conocidos y publicados

  CONTROL HUMANO
  ☐ Existe proceso de reclamación con revisión humana
  ☐ Los umbrales pueden ser ajustados por el equipo de riesgo
  ☐ Hay alertas cuando la tasa de rechazo se desvía >10% de la media

  SESGO Y FAIRNESS
  ☐ Revisión trimestral de decisiones por segmento (género, edad, zona)
  ☐ Los prompts no contienen variables protegidas (raza, religión...)
  ☐ El modelo no penaliza características correlacionadas con grupos protegidos

  SEGURIDAD
  ☐ Prompt injection no puede alterar la política de decisión
  ☐ Los inputs son sanitizados antes de entrar al prompt
  ☐ Límites de importe/riesgo hardcoded, no modificables por el LLM
```

### Métricas clave a monitorear

| Métrica | Descripción | Alerta si... |
|---------|-------------|--------------|
| Tasa de aprobación | % decisiones positivas | Varía >10% en 7 días |
| Tasa de escalada | % casos enviados a humano | Sube >20% (modelo inseguro) |
| Latencia P95 | Tiempo del percentil 95 | > 5 segundos |
| Override humano | % decisiones IA que el humano cambia | > 15% (modelo desalineado) |
| Tasa de reclamación | % clientes que impugnan | > 2% mensual |

```
FLUJO DE AUDITORÍA MENSUAL:

  1. Extraer muestra aleatoria de 200 decisiones del mes
  2. Revisar manualmente 20 casos límite (score 25–35 y 70–80)
  3. Calcular % de acuerdo humano-IA
  4. Identificar patrones en desacuerdos
  5. Ajustar umbrales o prompts si acuerdo < 85%
  6. Documentar cambios con fecha y responsable
```

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Wei et al. (2022) — *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* → [arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)
- Bai et al. / Anthropic (2022) — *Constitutional AI: Harmlessness from AI Feedback* → [arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)

**Informes de industria:**
- McKinsey (anual) — *The State of AI* → [mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) *(adopción de motores de decisión automatizados en servicios financieros y e-commerce)*
- Gartner — *Hype Cycle for Artificial Intelligence* → [gartner.com](https://www.gartner.com) *(Decision Intelligence como categoría emergente en el mercado de IA empresarial)*

**Libros recomendados:**
- Agrawal, Gans & Goldfarb (2022) — *Power and Prediction* (HBR Press) — marco teórico sobre cómo los sistemas de predicción automatizados redistribuyen el poder de decisión en las organizaciones
- Russell (2019) — *Human Compatible: AI and the Problem of Control* (Viking) — diseño de sistemas de decisión IA que mantienen el control y la supervisión humana efectiva

**Documentación oficial:**
- *EU AI Act (texto oficial)* → [eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689) *(obligaciones de transparencia y supervisión humana en sistemas de decisión automatizada)*

*Anterior: [6.1 Fundamentos No-Code](../6.1_fundamentos_nocode/README.md) | Siguiente: [6.3 Monitoreo y Resiliencia](../6.3_monitoreo_resiliencia/README.md)*
