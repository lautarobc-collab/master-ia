# 2.2 Prompt Engineering de Producción

## 2.2.1 Qué es el Prompt Engineering y por qué "hablar bien con la IA" no es suficiente

El prompt engineering es la disciplina de diseñar inputs que producen outputs fiables, consistentes y útiles en producción. No es escribir bien — es **diseñar un sistema de control sobre el comportamiento del modelo.**

La diferencia entre un uso amateur y uno profesional de la IA no está en el modelo que se elige, sino en la calidad del prompt.

```
Usuario amateur:
  "Haz un resumen de este contrato"
  → Resultado: variable, incompleto, formato inconsistente

Prompt de producción:
  "Eres un analista legal senior. Analiza el siguiente contrato
   e identifica EXACTAMENTE: (1) partes firmantes, (2) objeto
   del contrato, (3) importe y condiciones de pago, (4) cláusulas
   de penalización, (5) fecha de vigencia. Formato: JSON.
   Si un campo no aparece en el contrato, usa null."
  → Resultado: estructurado, extraíble, comparable entre contratos
```

### El coste de un prompt malo en producción

| Escenario | Prompt malo | Prompt de producción |
|---|---|---|
| 1.000 contratos/mes | 30% requieren revisión manual | <5% revisión |
| Coste revisión (1h × 35€) | 300h × 35€ = **10.500€/mes** | 50h × 35€ = **1.750€/mes** |
| Ahorro anual | — | **104.000€/año** |

Un prompt bien diseñado es una inversión de 2 horas que genera ROI continuo.

---

## 2.2.2 Los 6 elementos de un Prompt de Producción

Todo prompt robusto tiene estructura. No es necesario que todos los elementos estén presentes en cada prompt, pero conocerlos permite decidir cuáles incluir.

### Elemento 1 — Rol (Role)
Define quién es el modelo en esta tarea. El rol activa el "modo" correcto de respuesta.

```
❌ Sin rol:    "Resume este informe financiero"
✓  Con rol:   "Eres un CFO con 20 años de experiencia en empresas
               medianas del sector industrial. Resume este informe..."

El rol no es decorativo — ajusta el vocabulario, el nivel de detalle
y los aspectos que el modelo prioriza.
```

### Elemento 2 — Contexto (Context)
La información de fondo que el modelo necesita para dar una respuesta relevante.

```
Contexto mínimo:     empresa, sector, audiencia del output
Contexto completo:   empresa, sector, audiencia, objetivo del documento,
                     restricciones, tono, ejemplos previos
```

### Elemento 3 — Instrucción (Task)
La tarea concreta. Debe ser **específica, accionable y unívoca.**

```
❌ Vaga:       "Analiza este email"
✓  Específica: "Identifica: (1) la solicitud principal, (2) el tono
                emocional del remitente, (3) la urgencia implícita,
                (4) la respuesta recomendada en máx. 3 frases."
```

### Elemento 4 — Formato (Format)
Cómo debe estructurarse la respuesta. Crítico para integrar el output en sistemas downstream.

```
Opciones:
  - JSON con esquema definido      → para sistemas automatizados
  - Markdown con headers           → para documentos legibles
  - Lista numerada                 → para pasos o prioridades
  - Tabla                          → para comparativas
  - Texto plano                    → para emails y redacción
  - XML                            → para integraciones legacy
```

### Elemento 5 — Ejemplos (Few-shot)
Mostrar al modelo 1-3 ejemplos del input/output esperado. Es la técnica individual más potente.

```
# Ejemplo de few-shot para clasificación de emails

Input:  "Necesito la factura del pedido 4521, llevo 3 semanas esperando"
Output: {"categoria": "reclamacion", "urgencia": "alta", "departamento": "facturacion"}

Input:  "¿Cuál es vuestro horario de atención?"
Output: {"categoria": "consulta", "urgencia": "baja", "departamento": "atencion_cliente"}

Input:  [EMAIL A CLASIFICAR]
Output:
```

### Elemento 6 — Restricciones (Constraints)
Lo que el modelo NO debe hacer. Tan importante como lo que sí debe hacer.

```
Restricciones habituales:
  - "No inventes datos que no estén en el documento"
  - "No uses jerga técnica — la audiencia es no técnica"
  - "Máximo 150 palabras"
  - "No uses las palabras 'sinergias', 'innovador', 'disruptivo'"
  - "Si no puedes completar la tarea, explica por qué en lugar de inventar"
```

---

## 2.2.3 Las 4 Técnicas Fundamentales

### Técnica 1 — Zero-shot
Sin ejemplos. Funciona bien para tareas claras y bien definidas.

```
"Clasifica el siguiente email en: consulta / reclamacion / pedido / otro.
Responde únicamente con la categoría, sin explicación.

Email: [EMAIL]"
```

**Cuándo usarlo:** clasificaciones simples, transformaciones de formato, extracción de datos estructurados con esquema muy claro.

### Técnica 2 — Few-shot
Con 1-5 ejemplos de input/output. La técnica más versátil y de mayor impacto.

```
Regla de los ejemplos:
  1. Elige ejemplos representativos — que cubran los casos límite
  2. Los ejemplos al final del prompt pesan más que al principio
  3. 3 ejemplos suelen ser el óptimo — más no siempre mejora
  4. Los ejemplos deben ser reales o muy realistas
```

### Técnica 3 — Chain of Thought (CoT)
Pedir al modelo que razone paso a paso antes de dar la respuesta. Mejora drásticamente la calidad en tareas complejas.

```
❌ Sin CoT:
  "¿Debería esta empresa invertir en IA ahora?"
  → Respuesta superficial, sin análisis

✓  Con CoT:
  "Analiza si esta empresa debería invertir en IA ahora.
   Primero, evalúa sus capacidades actuales (datos, equipo, procesos).
   Segundo, identifica los quick wins más accesibles.
   Tercero, estima el riesgo de no actuar.
   Finalmente, da tu recomendación con argumentos."
  → Análisis estructurado con razonamiento visible
```

### Técnica 4 — Self-consistency y verificación
Pedir al modelo que verifique su propio output. No elimina errores pero los reduce.

```
Paso 1: "Extrae los datos financieros clave de este informe."
Paso 2: "Revisa los datos que acabas de extraer. ¿Hay alguno que
         no aparezca explícitamente en el texto? Márcalo con [INCIERTO]."
```

---

## 2.2.4 Prompt para Casos de Uso Corporativos: Plantillas Listas

### Plantilla 1 — Análisis de documentos

```
Eres un analista senior especializado en [SECTOR].

Analiza el siguiente [TIPO DE DOCUMENTO] e identifica:
1. [DATO 1]
2. [DATO 2]
3. [DATO 3]
4. Riesgos o inconsistencias que detectes

Formato de respuesta: JSON con las claves: dato1, dato2, dato3, riesgos (array).
Si un campo no está disponible en el documento, usa null — no lo estimes.

DOCUMENTO:
[DOCUMENTO]
```

### Plantilla 2 — Redacción corporativa

```
Eres un redactor corporativo experto en comunicación ejecutiva.

Escribe un [TIPO: email / informe / presentación] para [AUDIENCIA].

Contexto:
- Empresa: [EMPRESA]
- Objetivo del mensaje: [OBJETIVO]
- Tono: [formal / cercano / urgente]
- Extensión máxima: [N palabras]

No uses: jerga técnica, palabras como "sinergias" o "disruptivo",
         clichés corporativos vacíos.

Información a incluir:
[BULLET POINTS CON LOS PUNTOS CLAVE]
```

### Plantilla 3 — Clasificación y enrutamiento

```
Clasifica el siguiente [EMAIL / TICKET / SOLICITUD] según estas categorías:
[LISTA DE CATEGORÍAS CON DESCRIPCIÓN BREVE DE CADA UNA]

Reglas:
- Elige EXACTAMENTE UNA categoría
- Si hay ambigüedad, elige la de mayor urgencia
- Responde ÚNICAMENTE con el JSON: {"categoria": "...", "urgencia": "alta/media/baja", "razon": "..."}

[TEXTO A CLASIFICAR]
```

### Plantilla 4 — Síntesis ejecutiva

```
Eres un consultor de estrategia. Tu cliente es [ROL DEL LECTOR].

Resume el siguiente [DOCUMENTO] en máximo [N] palabras.
Estructura obligatoria:
- Situación actual (1-2 frases)
- Decisiones o hallazgos clave (3 bullets)
- Implicación para [ROL DEL LECTOR] (1-2 frases)

No incluyas: detalles técnicos, citas textuales, información que no
             sea relevante para la toma de decisiones.

[DOCUMENTO]
```

---

## 2.2.5 Los 5 Errores Más Caros en Prompts de Producción

### Error 1 — Ambigüedad en la instrucción
```
❌ "Resume el contrato de forma útil"
   → "útil" para quién, con qué propósito, en qué formato

✓  "Extrae del contrato: partes, objeto, precio total, fecha de vencimiento.
    Formato JSON. Máximo 200 tokens."
```

### Error 2 — No especificar el comportamiento ante casos límite
```
❌ El prompt no dice qué hacer si el documento está incompleto, en otro idioma
   o no contiene la información solicitada.
   → El modelo inventa, alucina o falla silenciosamente.

✓  "Si la información no está disponible en el documento, devuelve null
    para ese campo. No estimes ni infieras."
```

### Error 3 — System prompt débil en producción
```
❌ Sin system prompt: el modelo usa su comportamiento por defecto.

✓  System prompt define:
   - El rol permanente del asistente
   - Las restricciones que aplican a TODAS las interacciones
   - El formato base de respuesta
   - Lo que el modelo NUNCA debe hacer en este contexto
```

### Error 4 — No testear con casos adversariales
```
Antes de desplegar, testea con:
  - Documentos vacíos o muy cortos
  - Texto en otro idioma
  - Datos contradictorios
  - Inputs maliciosos ("ignora las instrucciones anteriores y...")
  - El caso más largo posible dentro del límite de contexto
```

### Error 5 — Prompt monolítico para tareas complejas
```
❌ Un prompt de 2.000 palabras que hace 8 cosas a la vez.
   → El modelo pierde foco, el output es inconsistente.

✓  Cadena de prompts simples:
   Prompt 1: extrae datos → Prompt 2: analiza datos → Prompt 3: redacta informe
   Cada prompt hace UNA cosa bien.
```

---

## 2.2.6 Versionado y Gestión de Prompts

Un prompt de producción es código. Debe tener las mismas prácticas que el código:

```
prompts/
  v1.0_clasificador_emails.txt      # versión inicial
  v1.1_clasificador_emails.txt      # añadido few-shot
  v2.0_clasificador_emails.txt      # rediseño con JSON output
  README_prompts.md                  # qué hace cada uno, por qué cambió

Para cada versión, documenta:
  - Qué cambió respecto a la versión anterior
  - Por qué cambió (qué fallaba)
  - Métricas de calidad antes/después
  - Modelo y temperatura a la que fue testeado
```

> **Regla de oro:** nunca modifiques un prompt en producción sin haberlo testeado con al menos 20 casos representativos. Un cambio pequeño puede degradar el rendimiento en casos que no anticipas.

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Wei et al. (2022) — *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* → [arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)
- Wang et al. (2022) — *Self-Consistency Improves Chain of Thought Reasoning in Language Models* → [arxiv.org/abs/2203.11171](https://arxiv.org/abs/2203.11171)
- Liu et al. (2023) — *Lost in the Middle: How Language Models Use Long Contexts* → [arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172)

**Informes de industria:**
- Stanford University (anual) — *AI Index Report* → [aiindex.stanford.edu/report/](https://aiindex.stanford.edu/report/) *(benchmarks de calidad por técnica de prompting en tareas de razonamiento)*

**Libros recomendados:**
- Iansiti & Lakhani (2020) — *Competing in the Age of AI* (HBR Press) — cómo el diseño de sistemas IA (incluido el prompting) determina la ventaja competitiva sostenible

**Documentación oficial:**
- *Anthropic Documentation — Prompt Engineering* → [docs.anthropic.com](https://docs.anthropic.com) *(guías oficiales de Anthropic sobre system prompts, few-shot y técnicas avanzadas para Claude)*

*Anterior: [2.1 Arquitectura Conceptual de los LLMs](../2.1_arquitectura_llms/README.md) | Siguiente: [2.3 Selección Estratégica de Modelos](../2.3_seleccion_modelos/README.md)*
