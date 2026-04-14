# 4.1 Fundamentos de RAG

## 4.1.1 El Problema que RAG Resuelve

Los LLMs tienen conocimiento estático: saben lo que aprendieron durante el entrenamiento, pero no saben nada de tus documentos internos, de los cambios normativos del mes pasado ni de los datos de tu ERP.

RAG (Retrieval-Augmented Generation) resuelve este problema sin reentrenar el modelo. En lugar de "enseñar" al modelo tu información, se la buscas en tiempo real y se la entregas con la pregunta.

```
SIN RAG:
  Usuario: "¿Cuál es nuestra política de devoluciones?"
  LLM: "No tengo esa información." (o peor: la inventa)

CON RAG:
  Usuario: "¿Cuál es nuestra política de devoluciones?"
  Sistema: [busca en la base documental] → encuentra el documento
  LLM: "Según vuestra política actualizada en enero de 2025:
        las devoluciones se aceptan en los primeros 30 días..."
```

---

## 4.1.2 Cómo Funciona RAG: los 5 Pasos

```
FASE DE INDEXACIÓN (se hace una vez, se actualiza cuando cambian los docs)

[Documentos] → [Chunking] → [Embedding] → [Vector Store]

Paso 1 — Chunking: dividir los documentos en fragmentos (chunks)
          de 200-500 tokens con solapamiento del 10-20%

Paso 2 — Embedding: convertir cada chunk en un vector numérico
          que captura su significado semántico

Paso 3 — Almacenar los vectores en una base de datos vectorial
          (Chroma, Pinecone, Weaviate, pgvector)

──────────────────────────────────────────────────────────────────

FASE DE CONSULTA (se ejecuta en cada pregunta del usuario)

[Pregunta] → [Embedding] → [Búsqueda] → [Contexto] → [LLM] → [Respuesta]

Paso 4 — Embed la pregunta y busca los chunks más similares
          (similitud coseno entre vectores)

Paso 5 — Incluir los chunks relevantes como contexto en el prompt
          y generar la respuesta citando las fuentes
```

---

## 4.1.3 Chunking: la Decisión más Importante

El chunking es cómo divides tus documentos. Una mala estrategia de chunking arruina el sistema entero aunque el resto esté bien implementado.

### Estrategias de chunking

**Chunking por tamaño fijo** — el más simple
```
Divide cada N tokens con solapamiento de M tokens.
  Ventaja: predecible, fácil de implementar
  Desventaja: puede cortar frases a la mitad, perdiendo contexto

Parámetros recomendados:
  chunk_size = 400 tokens
  chunk_overlap = 60 tokens (15%)
```

**Chunking semántico** — el más preciso
```
Divide en párrafos o secciones naturales del documento.
  Ventaja: preserva el contexto semántico
  Desventaja: chunks de tamaño variable, más difícil de implementar

Cuándo usarlo: documentos con estructura clara (contratos, manuales, SOPs)
```

**Chunking jerárquico** — el más potente
```
Mantiene la jerarquía del documento: capítulo → sección → párrafo.
La búsqueda puede retornar tanto el párrafo específico como
el capítulo completo si necesita más contexto.

Cuándo usarlo: documentación técnica larga, bases de conocimiento
```

### Reglas prácticas de chunking

```
· Nunca cortes en medio de una tabla o lista — el chunk pierde significado
· Incluye siempre el título/header de la sección en cada chunk
· Para contratos: chunk por cláusula, no por tamaño
· Para FAQs: chunk por par pregunta-respuesta
· Para emails: un email = un chunk (salvo emails muy largos)
```

---

## 4.1.4 Embeddings: Qué Son y Cuál Elegir

Un embedding es una representación numérica del significado de un texto. Textos semánticamente similares tienen vectores cercanos en el espacio matemático.

```
"política de devoluciones"    → [0.23, -0.41, 0.87, ...]  ← vectores cercanos
"plazo para devolver productos" → [0.21, -0.38, 0.89, ...]

"temperatura de fusión del acero" → [0.91, 0.12, -0.34, ...] ← vector lejano
```

### Modelos de embedding disponibles

| Modelo | Coste | Dimensiones | Cuándo usarlo |
|---|---|---|---|
| `text-embedding-3-small` (OpenAI) | $0.02/1M tokens | 1.536 | Caso de uso general, coste bajo |
| `text-embedding-3-large` (OpenAI) | $0.13/1M tokens | 3.072 | Mayor precisión semántica |
| `voyage-3` (Anthropic) | $0.06/1M tokens | 1.024 | Optimizado para uso con Claude |
| `nomic-embed` (open source) | Gratis (local) | 768 | On-premise, datos confidenciales |

---

## 4.1.5 Bases de Datos Vectoriales: Cuál Elegir

| Solución | Tipo | Cuándo usarla |
|---|---|---|
| **Chroma** | Open source, local | Prototipos y proyectos pequeños (<100K docs) |
| **pgvector** | Extensión PostgreSQL | Ya tienes Postgres, quieres simplicidad |
| **Pinecone** | Cloud gestionado | Producción sin querer gestionar infra |
| **Weaviate** | Open source / cloud | Búsqueda híbrida (semántica + keyword) |
| **Qdrant** | Open source / cloud | Alto rendimiento, grandes volúmenes |

**Recomendación por fase:**
```
Prototipo:    Chroma (local, sin configuración)
Piloto:       pgvector si ya tienes Postgres, Chroma si no
Producción:   Pinecone o Qdrant según volumen y requisitos de privacidad
```

---

## 4.1.6 Métricas de Calidad de un Sistema RAG

Un sistema RAG puede fallar en dos puntos: en la recuperación (retrieval) o en la generación. Hay que medir ambos.

```
MÉTRICAS DE RETRIEVAL:
  Recall@k:  ¿Cuántas veces el chunk correcto está en los top-k resultados?
             Objetivo: > 85% para k=3
  Precision: ¿Cuántos de los chunks recuperados son realmente relevantes?

MÉTRICAS DE GENERACIÓN:
  Faithfulness:   ¿La respuesta está soportada por los chunks recuperados?
  Answer relevance: ¿La respuesta responde la pregunta del usuario?

MÉTRICA GLOBAL:
  End-to-end accuracy: ¿La respuesta final es correcta?
  (Lo que ve el usuario — el KPI más importante)
```

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Lewis et al. (2020) — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* → [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)
- Liu et al. (2023) — *Lost in the Middle: How Language Models Use Long Contexts* → [arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172)

**Informes de industria:**
- McKinsey (anual) — *The State of AI* → [mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) *(adopción de RAG en empresas y métricas de impacto en sistemas de búsqueda documental)*

**Libros recomendados:**
- Iansiti & Lakhani (2020) — *Competing in the Age of AI* (HBR Press) — cómo los sistemas de recuperación de conocimiento crean ventajas competitivas sostenibles en la empresa

**Documentación oficial:**
- *Anthropic Documentation* → [docs.anthropic.com](https://docs.anthropic.com) *(guía de implementación de RAG con Claude, incluyendo configuración de contexto y citación de fuentes)*

*Anterior: [3.3 Validación y Quality Assurance](../../modulo_3/3.3_quality_assurance/README.md) | Siguiente: [4.2 Curación de Bases Documentales](../4.2_curacion_documental/README.md)*
