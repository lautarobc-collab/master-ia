# 5.1 Preparación de Datos para Análisis con IA

## 5.1.1 Por qué los Datos Empresariales Rara Vez Están Listos

El 70% del tiempo en cualquier proyecto de analítica con IA no se invierte en el modelo — se invierte en preparar los datos. Esto es así porque los datos empresariales reales son:

```
ESTADO TÍPICO DE LOS DATOS EMPRESARIALES:
  · Fechas en 4 formatos distintos en la misma columna
  · Nombres de empresa con variaciones: "ACME S.L.", "Acme sl", "ACME, S.L."
  · Valores nulos mezclados con "N/A", "-", "0", "desconocido"
  · Columnas numéricas con separadores de miles inconsistentes (1.200 vs 1200 vs 1,200)
  · Datos de personas en texto libre sin estructura
  · Varias tablas con las mismas entidades pero sin clave común
```

La preparación de datos no es trabajo tedioso — es lo que determina si el análisis posterior es fiable.

---

## 5.1.2 El Pipeline de Preparación en 6 Pasos

### Paso 1 — Perfilado inicial
Antes de limpiar, entiende qué tienes:
```
Para cada columna:
  · Tipo de dato (numérico, texto, fecha, booleano)
  · % de valores nulos
  · Número de valores únicos
  · Rango (min, max) para numéricos
  · Valores más frecuentes
  · Ejemplos de valores problemáticos
```

### Paso 2 — Normalización de tipos
```
Fechas:       → ISO 8601 (YYYY-MM-DD) siempre
Números:      → float o int, sin separadores de miles, punto decimal
Texto:        → strip(), lower() para comparaciones, preservar mayúsculas en nombres
Booleanos:    → True/False — eliminar: "sí/no", "1/0", "activo/inactivo"
Categorías:   → definir valores permitidos, mapear variantes
```

### Paso 3 — Tratamiento de valores nulos
```
OPCIONES (elige según el contexto):
  · Eliminar filas con nulos si son < 5% del total y el campo es crítico
  · Imputar con la mediana/moda si el campo es numérico/categórico y hay patrón
  · Imputar con IA si el campo es texto y hay contexto suficiente
  · Crear flag "campo_nulo" y conservar la fila para análisis de ausencia
  · Dejar null si la ausencia es información relevante en sí misma
```

### Paso 4 — Deduplicación
```
Deduplicación exacta:    eliminar filas idénticas
Deduplicación fuzzy:     agrupar registros similares (empresa "ACME" vs "Acme S.L.")
  → Herramientas: pandas drop_duplicates(), fuzzywuzzy, recordlinkage
  → Con IA: pedir al modelo que identifique si dos nombres son la misma entidad
```

### Paso 5 — Enriquecimiento
Añadir columnas derivadas que faciliten el análisis:
```
Ejemplos:
  · "mes" y "trimestre" desde "fecha_pedido"
  · "dias_desde_ultimo_pedido" calculado
  · "segmento_cliente" desde "importe_total_año"
  · "texto_normalizado" para análisis semántico
```

### Paso 6 — Validación del dataset limpio
```
Checks mínimos antes de usar el dataset:
  ☐ 0 duplicados exactos
  ☐ % nulos por columna dentro del umbral aceptado
  ☐ Tipos de dato correctos en todas las columnas
  ☐ Rango de fechas correcto (no fechas futuras donde no aplica)
  ☐ Valores categóricos dentro del conjunto permitido
  ☐ N filas esperadas (± tolerancia)
```

---

## 5.1.3 IA para Preparación de Datos: Cuándo Ayuda

La IA es especialmente útil en las partes de preparación que requieren comprensión semántica:

| Tarea | Sin IA | Con IA |
|---|---|---|
| Deduplicación fuzzy de nombres | Reglas manuales, muchos casos límite | Clasifica si dos nombres son la misma entidad |
| Categorización de texto libre | Definir reglas, entrenar clasificador | Few-shot con ejemplos |
| Extracción de entidades | Regex complejos | Prompt de extracción |
| Imputación de texto | Imposible | Inferencia desde contexto |
| Detección de anomalías | Statistical outliers | Añade el "¿tiene sentido?" semántico |

---

## 5.1.4 Documentación del Dataset

Un dataset bien documentado es un activo reutilizable. La documentación mínima:

```markdown
# Dataset: [NOMBRE]
Fuente: [origen de los datos]
Fecha de extracción: [fecha]
Período que cubre: [rango temporal]
N filas: [número]
N columnas: [número]

## Columnas
| Columna | Tipo | Descripción | % Nulos | Valores permitidos |
|---|---|---|---|---|
| id_cliente | int | Identificador único | 0% | > 0 |
| fecha_pedido | date | Fecha de creación | 0% | 2020-2025 |
| importe_eur | float | Importe sin IVA | 2.3% | 0-50.000 |

## Transformaciones aplicadas
- [lista de cambios realizados respecto al dato bruto]

## Limitaciones conocidas
- [qué no captura este dataset, sesgos conocidos]
```

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Wang et al. (2022) — *Self-Consistency Improves Chain of Thought Reasoning in Language Models* → [arxiv.org/abs/2203.11171](https://arxiv.org/abs/2203.11171)

**Informes de industria:**
- McKinsey (anual) — *The State of AI* → [mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) *(la calidad de datos como factor crítico en el éxito de proyectos de analítica con IA)*
- Stanford University (anual) — *AI Index Report* → [aiindex.stanford.edu/report/](https://aiindex.stanford.edu/report/) *(tendencias en herramientas de preparación y calidad de datos para IA)*

**Libros recomendados:**
- Nussbaumer Knaflic (2015) — *Storytelling with Data* (Wiley) — principios de limpieza y estructuración de datos para que soporten narrativas analíticas precisas

**Documentación oficial:**
- *Pandas Documentation* → [pandas.pydata.org/docs/](https://pandas.pydata.org/docs/) *(referencia técnica para las operaciones de limpieza y transformación de datos descritas en el módulo)*

*Anterior: [4.3 Diseño de Asistentes Seguros](../../modulo_4/4.3_asistentes_seguros/README.md) | Siguiente: [5.2 Interrogación Analítica con IA](../5.2_interrogacion_analitica/README.md)*
