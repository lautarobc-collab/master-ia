# 3.2 Identidad Comunicativa y Tono

## 3.2.1 Por qué la IA Suena a IA (y Cómo Evitarlo)

Los outputs de IA no estructurados tienen una firma reconocible: frases largas con múltiples cláusulas subordinadas, uso excesivo de "en primer lugar / en segundo lugar", conclusiones que repiten la pregunta, y un entusiasmo corporativo vacío ("¡Excelente pregunta!"). Este patrón destruye la credibilidad del sistema en cuanto el lector lo detecta.

La identidad comunicativa es el conjunto de reglas que hacen que los outputs de IA suenen a *tu empresa*, no a ChatGPT.

```
Sin identidad comunicativa:
  "En primer lugar, es importante destacar que la implementación de
   soluciones de inteligencia artificial representa una oportunidad
   extraordinaria para optimizar los procesos empresariales y generar
   valor añadido en toda la cadena de valor."

Con identidad comunicativa (empresa directa, sector industrial):
  "Automatizar el proceso de clasificación de incidencias reduce el
   tiempo de respuesta de 4 horas a 20 minutos. Con el volumen actual,
   eso son 6.400 horas al año."
```

---

## 3.2.2 Los 4 Ejes del Tono Corporativo

### Eje 1 — Formalidad (escala 1-5)
```
1 — Muy informal:  "Oye, mira lo que encontré"
3 — Neutro:        "A continuación, los resultados del análisis"
5 — Muy formal:    "En virtud de lo expuesto, se eleva a consideración"

La mayoría de comunicación corporativa eficaz vive en el rango 3-4.
El nivel 5 es para documentos legales y notificaciones regulatorias.
```

### Eje 2 — Densidad informativa
```
ALTA: cada frase aporta un dato o una acción. Sin relleno.
      → Informes ejecutivos, análisis financieros
MEDIA: contexto + datos + interpretación equilibrados
      → Propuestas comerciales, memos internos
BAJA: narrativa con espacio para la reflexión
      → Comunicaciones de cambio, cultura corporativa
```

### Eje 3 — Proximidad al lector
```
DISTANTE: "Los empleados deberán cumplimentar el formulario"
PRÓXIMA:  "Necesitamos que rellenes el formulario antes del viernes"

La comunicación interna suele ser más próxima. La externa varía según el cliente.
```

### Eje 4 — Orientación a la acción
```
DESCRIPTIVA:  "El proyecto ha alcanzado el 70% de los objetivos."
ORIENTADA:    "El proyecto está al 70%. Para llegar al 100% en plazo,
               necesitamos aprobar el recurso adicional esta semana."
```

---

## 3.2.3 Crear la Guía de Estilo para la IA

Una guía de estilo para la IA es el documento que defines una vez y referencias en todos tus prompts. Tiene 5 secciones:

### Sección 1 — Voz de la empresa

```
EMPRESA: Distribuciones Norte S.L.
VOZ: directa, honesta, sin adornos. Damos datos antes que opiniones.
     Reconocemos los problemas abiertamente. No usamos eufemismos.

EJEMPLOS DE VOZ:
  ✓ "El proyecto lleva 2 semanas de retraso por falta de datos limpios."
  ✗ "El proyecto está experimentando algunas demoras en el proceso de maduración."
```

### Sección 2 — Palabras prohibidas y preferidas

```
PROHIBIDAS (genéricas y vacías):
  sinergias, innovador, disruptivo, ecosistema, paradigma,
  solución integral, de vanguardia, best-in-class, best practices,
  potenciar, visibilizar, apalancar

PREFERIDAS (concretas y activas):
  reducir, aumentar, eliminar, medir, implementar, probar,
  el dato, el resultado, el coste, el plazo, la persona responsable
```

### Sección 3 — Estructura por tipo de comunicación

```
EMAIL INTERNO:
  Asunto: [Acción] — [Tema] — [Fecha si urgente]
  Párrafo 1: qué y por qué importa (3 líneas máx)
  Párrafo 2: qué necesito de ti (específico)
  Párrafo 3: próximos pasos con fecha

INFORME A CLIENTE:
  Resumen ejecutivo (1 pág) → Hallazgos → Metodología → Anexos
  Siempre empieza por la conclusión, no por el contexto.

PRESENTACIÓN INTERNA:
  Máx. 8 diapositivas. Cada diapositiva = 1 idea.
  Título de diapositiva = la conclusión, no el tema.
```

### Sección 4 — Longitudes objetivo

```
Email interno urgente:    < 100 palabras
Email interno estándar:   100-200 palabras
Informe ejecutivo:        150-250 palabras
Propuesta comercial:      800-1.200 palabras
SOP de proceso:           300-600 palabras
```

### Sección 5 — Tratamiento de datos y cifras

```
REGLAS:
  · Redondear a 2 decimales máximo en contextos ejecutivos
  · Usar % cuando la ratio importa, cifras absolutas cuando el volumen importa
  · Siempre incluir el período de referencia: "en Q1 2025", no "recientemente"
  · Comparar contra benchmark: no "el tiempo bajó a 2h", sino "bajó de 6h a 2h (−67%)"
```

---

## 3.2.4 Inyectar la Guía de Estilo en los Prompts

La guía de estilo va en el **system prompt** — así aplica a todas las interacciones sin repetirla en cada prompt de usuario.

```
SYSTEM PROMPT CON ESTILO:

Eres el asistente de comunicación corporativa de [EMPRESA].

VOZ Y TONO:
- Directo y orientado a datos. Cada frase aporta información.
- Formalidad: 3/5. Profesional pero no burocrático.
- Nunca uses: sinergias, innovador, disruptivo, ecosistema, apalancar.
- Siempre incluye cifras comparativas (antes/después, % cambio).

FORMATO POR DEFECTO:
- Emails: asunto en formato [Acción] — [Tema]
- Informes: conclusión primero, contexto después
- Bullets: máximo 5 por sección

RESTRICCIONES:
- No generes contenido que no tenga base en los datos proporcionados.
- Si falta información, indica qué se necesita para completar el output.
```

---

## 3.2.5 Calibración y Mantenimiento del Tono

Una guía de estilo se degrada si no se actualiza. El proceso de mantenimiento:

```
REVISIÓN MENSUAL (30 minutos):
  1. Toma 5 outputs del mes que el equipo haya editado significativamente
  2. Analiza el patrón: ¿qué cambian siempre?
  3. Si el cambio es consistente → actualiza la guía de estilo
  4. Añade los ejemplos corregidos a la sección de "ejemplos de voz"

SEÑALES DE QUE LA GUÍA NECESITA ACTUALIZACIÓN:
  · Tasa de edición > 30% en outputs del mismo tipo
  · El equipo añade siempre la misma frase o dato
  · Nuevos responsables que no reconocen el tono como propio
```

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Wei et al. (2022) — *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* → [arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)

**Informes de industria:**
- Nielsen Norman Group — *Writing Style and Tone for Digital Communication* → [nngroup.com](https://www.nngroup.com) *(investigación sobre el impacto del tono y la voz de marca en la percepción de credibilidad y confianza)*
- McKinsey (anual) — *The State of AI* → [mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) *(cómo las empresas líderes gestionan la coherencia de comunicación en entornos con IA)*

**Libros recomendados:**
- Nussbaumer Knaflic (2015) — *Storytelling with Data* (Wiley) — principios de coherencia narrativa y visual que fundamentan la identidad comunicativa corporativa
- Iansiti & Lakhani (2020) — *Competing in the Age of AI* (HBR Press) — la identidad de marca como ventaja competitiva en la era de la automatización de contenidos

**Documentación oficial:**
- *Anthropic Documentation — System Prompts* → [docs.anthropic.com](https://docs.anthropic.com) *(cómo implementar guías de estilo y restricciones de tono en el system prompt de Claude)*

*Anterior: [3.1 Ingeniería de Outputs Corporativos](../3.1_outputs_corporativos/README.md) | Siguiente: [3.3 Validación y Quality Assurance](../3.3_quality_assurance/README.md)*
