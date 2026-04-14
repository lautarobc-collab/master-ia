# 5.3 Integración con Business Intelligence

## 5.3.1 IA + BI: Dos Capas Complementarias

Las herramientas de BI (Power BI, Tableau, Looker) son excelentes para visualizar datos estructurados y generar dashboards. Tienen un límite: requieren que el usuario sepa dónde mirar y qué pregunta hacer.

La IA añade la capa de lenguaje natural y síntesis: responde preguntas que no están predefinidas en el dashboard, genera la narrativa del informe y alerta proactivamente cuando algo merece atención.

```
BI SIN IA:
  · Dashboard estático de KPIs
  · El usuario decide qué mirar
  · Requiere cultura de datos en el equipo
  · Analista interpreta y redacta el informe manualmente

BI CON IA:
  · Dashboard + capa de conversación natural
  · La IA alerta sobre anomalías sin que nadie lo pida
  · Cualquiera puede preguntar sin saber SQL
  · Narrativa del informe generada automáticamente
```

---

## 5.3.2 Patrones de Integración

### Patrón 1 — Narrador de Dashboard
La IA lee los datos del dashboard (exportados como JSON o CSV) y genera el comentario ejecutivo.

```python
# Proceso:
# 1. Exportar datos del dashboard a CSV/JSON
# 2. Enviar a Claude con prompt de narrativa
# 3. Insertar el texto generado en el informe

datos_dashboard = exportar_kpis_semana()
narrativa = claude.generar_narrativa(datos_dashboard, audiencia="dirección")
informe.insertar_seccion("Resumen ejecutivo", narrativa)
```

### Patrón 2 — Alertas inteligentes
Un job programado analiza los KPIs cada día/semana y genera alertas solo cuando hay algo relevante.

```python
# Proceso:
# 1. Comparar KPIs actuales vs baseline (semana anterior, media histórica)
# 2. Enviar desviaciones a Claude con umbral definido
# 3. Claude determina si la desviación es relevante y por qué
# 4. Enviar resumen solo si hay algo que merece atención

def analizar_kpis_diarios(kpis_hoy, kpis_ayer):
    desviaciones = calcular_desviaciones(kpis_hoy, kpis_ayer)
    if max(abs(d) for d in desviaciones.values()) > 0.10:  # > 10% de desviación
        return claude.evaluar_alertas(desviaciones)
    return None  # sin alertas
```

### Patrón 3 — Asistente de BI conversacional
El usuario hace preguntas en lenguaje natural sobre el dashboard desde un chat integrado.

```
Arquitectura:
  [Chat UI] → [Claude con schema + contexto] → [SQL/API call] → [Resultado] → [Narrativa]
```

### Patrón 4 — Generador de informes periódicos
Combina datos del BI con plantillas para generar informes semanales/mensuales automáticamente.

---

## 5.3.3 Integración Técnica con las Principales Herramientas

### Power BI
```
Opción A — API REST: exportar datos con la API de Power BI → procesar con Claude → publicar de vuelta
Opción B — Power Automate: flow que lee el dataset, llama a Claude y envía el resumen por email
Opción C — Python connector: pandas lee el dataset → Claude analiza → resultado a Power BI
```

### Google Sheets / Looker
```
Google Sheets: Apps Script llama a Claude API → inserta narrativa en la hoja
Looker: integración via Looker Marketplace o extensión custom con la API
```

### Tableau
```
Python integration (TabPy): función Python en Tableau que llama a Claude
Tableau Pulse: ya incluye generación de insights con IA (limitado)
```

---

## 5.3.4 Diseño del Pipeline de Reporting Automático

```
PIPELINE SEMANAL AUTOMATIZADO:

Lunes 08:00
  [Job] extrae KPIs de BD → CSV
  [Claude] analiza vs semana anterior → genera narrativa
  [Claude] identifica top 3 alertas
  [Sistema] genera PDF del informe
  [Email] envía a lista de distribución

Contenido del informe automatizado:
  · Resumen ejecutivo (narrativa Claude — 150 palabras)
  · Dashboard de KPIs con semáforos
  · Top 3 alertas con contexto y recomendación
  · Comparativa vs objetivo y vs período anterior
  · Próximos hitos relevantes
```

---

## 5.3.5 Limitaciones y Consideraciones de Gobernanza

```
QUÉ VIGILAR EN BI + IA:

Precisión de los datos fuente:
  La IA no detecta si los datos del BI son incorrectos en origen.
  Garbage in, garbage out también aplica aquí.

Interpretaciones incorrectas:
  La IA puede generar narrativas plausibles pero equivocadas.
  Un analista debe revisar los informes críticos antes de distribuirlos.

Privacidad:
  Los datos enviados a la API de Claude pueden contener información
  sensible. Evaluar: anonimizar, usar acuerdo DPA, o procesar on-premise.

Dependencia de API:
  Si la API no está disponible, el reporting falla.
  Tener siempre un fallback al informe manual.
```

---

*Anterior: [5.2 Interrogación Analítica con IA](../5.2_interrogacion_analitica/README.md) | Siguiente: [6.1 Fundamentos No-Code](../../modulo_6/6.1_fundamentos_nocode/README.md)*
