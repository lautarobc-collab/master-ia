# 5.2 Interrogación Analítica con IA

## 5.2.1 Del Dato a la Decisión: el Rol de la IA en el Análisis

El análisis de datos tradicional requiere saber SQL, Python o Excel avanzado. La IA permite que cualquier persona con criterio de negocio pueda interrogar los datos en lenguaje natural — y que los analistas generen análisis 10 veces más rápido.

Pero la IA no reemplaza el criterio analítico: lo amplifica. Sigue siendo el analista quien define las preguntas correctas, interpreta los resultados en contexto y detecta cuando un número no tiene sentido.

---

## 5.2.2 Los 4 Modos de Interrogación Analítica con IA

### Modo 1 — Resumen descriptivo
La IA lee el dataset y describe qué ve: tendencias, outliers, distribuciones.

```
Prompt: "Analiza estos datos de ventas del Q1 2025 e identifica:
  (1) los 3 patrones más relevantes,
  (2) los outliers que merecen investigación,
  (3) qué pregunta adicional harías para entender mejor los datos."
```

### Modo 2 — Consulta en lenguaje natural
El usuario pregunta en español, la IA genera el código o la consulta SQL.

```
Usuario: "¿Cuál es el cliente con mayor crecimiento en los últimos 3 meses?"
IA: genera SQL → "SELECT cliente, SUM(importe) FROM pedidos
                  WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
                  GROUP BY cliente ORDER BY SUM(importe) DESC LIMIT 5"
```

### Modo 3 — Hipótesis y causalidad
La IA propone hipótesis sobre por qué están ocurriendo los patrones que ve.

```
Prompt: "Las ventas de la categoría X bajaron un 23% en febrero.
  ¿Cuáles son las 5 hipótesis más probables? Para cada una,
  qué dato necesitaría para confirmarla o descartarla."
```

### Modo 4 — Narrativa ejecutiva
La IA convierte tablas de números en narrativa comprensible para dirección.

```
Prompt: "Convierte esta tabla de KPIs en un párrafo de 100 palabras
  para el informe de dirección. Destaca lo más relevante para
  la toma de decisiones. No repitas todos los números — selecciona
  los 3 más importantes y explica qué implican."
```

---

## 5.2.3 Text-to-SQL: Consultas en Lenguaje Natural

La generación de SQL desde lenguaje natural es una de las aplicaciones más maduras y con mayor ROI en analítica empresarial.

### Cómo diseñar el prompt de Text-to-SQL

```
SISTEMA: Eres un experto en SQL. Solo generas código SQL válido.
  No ejecutas nada — solo generas la consulta.
  Si la pregunta es ambigua, elige la interpretación más conservadora.

CONTEXTO (incluir en el prompt):
  Tablas disponibles:
    pedidos (id, cliente_id, fecha, importe_eur, estado, producto_id)
    clientes (id, nombre, sector, ciudad, fecha_alta)
    productos (id, nombre, categoria, precio_base)

PREGUNTA DEL USUARIO: {pregunta}

Genera SOLO la consulta SQL, sin explicaciones.
```

### Limitaciones a conocer

```
Text-to-SQL es fiable para:
  · Consultas de agregación simples (SUM, COUNT, AVG)
  · Filtros por fecha, categoría, rango
  · Joins entre 2-3 tablas bien definidas

Text-to-SQL es menos fiable para:
  · Lógica de negocio compleja no documentada en el schema
  · Cálculos temporales avanzados (cohortes, retención)
  · Múltiples subqueries anidadas
  → Siempre valida el SQL generado antes de ejecutar en producción
```

---

## 5.2.4 Análisis de Texto No Estructurado

Enormes cantidades de información empresarial están en texto libre: emails, reseñas, notas de reuniones, comentarios de soporte. La IA puede analizarlos a escala.

### Casos de uso

```
ANÁLISIS DE SENTIMIENTO:
  → Clasificar satisfacción de clientes en emails/reseñas
  → Detectar tendencias en el feedback

EXTRACCIÓN DE TEMAS:
  → Qué piden los clientes con más frecuencia
  → Cuáles son los problemas recurrentes en soporte

CLASIFICACIÓN:
  → Priorizar tickets por urgencia e impacto
  → Categorizar leads por intención de compra

RESUMEN DE REUNIONES:
  → Extraer acuerdos, responsables y fechas de transcripciones
```

---

## 5.2.5 Interpretación: Lo que la IA no Puede Hacer por Ti

La IA genera números y patrones. La interpretación de negocio es responsabilidad humana.

```
LA IA PUEDE:                           EL ANALISTA DEBE:
──────────────────────────────────────────────────────────
Detectar que las ventas bajaron 23%    Saber si ese % es alarmante
                                       en el contexto de la empresa

Generar 5 hipótesis                    Saber cuál es plausible
                                       dado el contexto del mercado

Extraer que el cliente X               Saber si X es estratégico
tiene la mayor caída                   y qué hacer al respecto

Calcular la correlación                Saber si la correlación
entre A y B                            implica causalidad
```

---

*Anterior: [5.1 Preparación de Datos](../5.1_preparacion_datos/README.md) | Siguiente: [5.3 Integración con Business Intelligence](../5.3_integracion_bi/README.md)*
