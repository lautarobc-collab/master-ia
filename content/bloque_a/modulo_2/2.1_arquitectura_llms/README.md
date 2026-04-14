# 2.1 Arquitectura Conceptual de los LLMs

## 2.1.1 Qué es un LLM y por qué importa entender cómo funciona

Un Large Language Model (LLM) es un sistema de predicción estadística entrenado sobre cantidades masivas de texto. No "piensa" ni "entiende" en sentido humano — aprende patrones de co-ocurrencia entre tokens y los usa para generar continuaciones probables de un texto dado.

Entender esto no es trivia técnica: **cambia cómo construyes prompts, cómo evalúas outputs y cómo diseñas sistemas fiables.**

### La analogía del autocomplete extremo

```
Tu teléfono predice la siguiente palabra.
Un LLM predice el siguiente token en secuencias de miles de tokens,
habiendo visto billones de ejemplos, con 70.000 millones de parámetros
ajustados para que esa predicción sea útil.

La diferencia no es cualitativa — es de escala.
Y la escala produce comportamientos emergentes que la escala pequeña no tiene.
```

### Por qué esto importa para un directivo

| Si crees que el LLM... | Harás... | Resultado |
|---|---|---|
| "Sabe" la respuesta correcta | Confiarás en el output sin validar | Errores costosos |
| Inventa datos al azar | No lo usarás para análisis | Perderás el 80% del valor |
| Funciona igual siempre | No optimizarás el prompt | Outputs mediocres |
| Predice tokens con contexto | Diseñarás contexto rico y validación | Resultados fiables |

---

## 2.1.2 Los 4 componentes del funcionamiento de un LLM

### Componente 1 — Tokenización

El modelo no lee palabras sino **tokens** — fragmentos de texto que pueden ser una palabra, parte de una palabra o un símbolo.

```
"transformación digital" → ["transform", "ación", " digital"]
"ROI"                   → ["ROI"]  (token único, es frecuente)
"anticonstitucional"    → ["anti", "const", "itucion", "al"]
```

**Implicación práctica:**
- Los tokens cuestan dinero (precios de API en tokens, no palabras)
- Palabras raras o técnicas consumen más tokens por sílaba
- Los números se tokenizen mal → los LLMs hacen aritmética con dificultad
- El límite de contexto es en tokens, no en palabras (~1.3 palabras/token en español)

### Componente 2 — Embeddings y espacio semántico

Cada token se convierte en un vector de alta dimensión (embedding). Tokens semánticamente similares quedan cerca en ese espacio:

```
espacio vectorial (simplificado a 2D):

        "CEO"
         ●
    "directivo" ●      ● "manager"
         
                         
    "factura" ●    ● "albarán"
    
"código" ●
              ● "script"
```

Esto explica por qué el modelo entiende sinónimos, analogías y contexto sin que se lo expliques explícitamente.

### Componente 3 — Atención (Transformer)

El mecanismo de atención permite que cada token "mire" a todos los demás tokens del contexto y pese su relevancia. Es lo que hace que el modelo pueda:

- Resolver pronombres ("el informe que *él* escribió" → quién es "él")
- Mantener coherencia en textos largos
- Seguir instrucciones complejas dadas al principio del prompt

```
Prompt: "Eres un analista financiero experto. Revisa este contrato
         y señala los riesgos para la empresa compradora. [contrato]"

El modelo atiende a "analista financiero" y "empresa compradora"
a lo largo de TODO el contrato, no solo en el párrafo actual.
```

### Componente 4 — Temperatura y sampling

Al generar el siguiente token, el modelo calcula una distribución de probabilidad sobre todo el vocabulario. La temperatura controla cuánto se aplana esa distribución:

```
Temperatura 0.0:  elige siempre el token más probable → determinista, repetitivo
Temperatura 0.5:  equilibrio → coherente con variedad controlada
Temperatura 1.0:  distribución original → creativo pero puede desviarse
Temperatura 2.0:  distribución aplanada → caótico, alucinaciones frecuentes

REGLAS PRÁCTICAS:
  Análisis / extracción de datos  → temperature 0.0 - 0.2
  Redacción corporativa           → temperature 0.3 - 0.5
  Brainstorming / creatividad     → temperature 0.7 - 1.0
```

---

## 2.1.3 Preentrenamiento, Fine-Tuning e Instrucción: las 3 fases

Un modelo como Claude o GPT-4 no llega al usuario en una sola fase. Pasa por tres etapas que determinan su comportamiento final.

### Fase 1 — Preentrenamiento (Base Model)
El modelo lee billones de tokens de internet, libros y código. Aprende gramática, hechos, razonamiento y estilo. No sigue instrucciones — solo continúa texto.

```
Input:  "La capital de Francia es"
Output: " París, una ciudad conocida por..."
```

### Fase 2 — Fine-tuning por instrucción (Instruction Tuning)
Se entrena con ejemplos de pares (instrucción → respuesta ideal). El modelo aprende a seguir órdenes, responder preguntas y usar formatos específicos.

```
Input:  "¿Cuál es la capital de Francia?"
Output: "La capital de Francia es París."
```

### Fase 3 — RLHF (Reinforcement Learning from Human Feedback)
Humanos evalúan pares de respuestas. Un modelo de recompensa aprende qué prefieren los humanos. El LLM se optimiza para maximizar esa recompensa.

Resultado: modelos que no solo son correctos sino **útiles, seguros y alineados** con lo que el usuario necesita.

> **Para el directivo:** cuando dices "el modelo de hoy es mejor que hace 6 meses", normalmente el salto viene de mejoras en RLHF, no en el preentrenamiento. La calidad del feedback humano es más determinante que el tamaño del modelo.

---

## 2.1.4 La Ventana de Contexto: qué es y cómo afecta tu uso

La ventana de contexto es la memoria operativa del modelo — todo lo que "ve" en un momento dado: el system prompt, el historial de conversación y el mensaje actual.

```
VENTANA DE CONTEXTO (ejemplo 200.000 tokens ≈ 150.000 palabras)

┌─────────────────────────────────────────────────────────┐
│ System prompt       │ 500 tokens   (~375 palabras)      │
│ Historial previo    │ 15.000 tokens                     │
│ Documento adjunto   │ 80.000 tokens (~60.000 palabras)  │
│ Mensaje actual      │ 200 tokens                        │
│ ─────────────────────────────────────────────────────── │
│ DISPONIBLE          │ 104.300 tokens restantes          │
└─────────────────────────────────────────────────────────┘
```

### Lo que debes saber sobre el contexto

**El modelo atiende mejor lo que está al principio y al final.** El "lost in the middle" es un fenómeno real: instrucciones críticas en medio de un contexto largo se ignoran más.

```
Buena práctica:
  [Instrucción principal] → al principio
  [Documento largo]       → en el medio
  [Recordatorio clave]    → al final

Mala práctica:
  [Documento largo] → [Instrucción enterrada] → [Más documento]
```

**El contexto no es memoria persistente.** Cada llamada a la API es independiente. Si necesitas que el modelo "recuerde" algo entre sesiones, debes incluirlo explícitamente en el prompt (RAG, resumen de conversación anterior, etc.).

---

## 2.1.5 Alucinaciones: por qué ocurren y cómo mitigarlas

Una alucinación es cuando el modelo genera información factualmente incorrecta con el mismo nivel de confianza que la correcta. Es una consecuencia directa de cómo funciona: el modelo predice texto plausible, no verdadero.

### Los 3 tipos de alucinación más comunes

| Tipo | Ejemplo | Contexto frecuente |
|---|---|---|
| **Factual** | Cita una ley que no existe | Preguntas sobre normativa específica |
| **Estadística** | Inventa datos de mercado | Análisis sin datos de referencia |
| **Referencial** | Cita un paper que no existe | Peticiones de fuentes y bibliografía |

### Por qué ocurren

```
El modelo ha visto patrones como:
  "Según el artículo X del BOE, las empresas deben..."
  "El estudio de McKinsey (2023) indica que..."

Cuando no conoce el dato exacto, genera la continuación
más estadísticamente probable — que puede ser inventada.

No "sabe" que está alucinando. No tiene mecanismo de duda.
```

### Estrategias de mitigación

**1. Grounding — ancla el modelo a datos reales:**
```
❌ "¿Cuál es el ROI medio de proyectos de IA?"
✓  "Dado este informe [adjunto], ¿cuál es el ROI medio reportado?"
```

**2. Instruye al modelo a reconocer la incertidumbre:**
```
"Si no tienes certeza sobre un dato, di explícitamente
 'No tengo información fiable sobre esto' en lugar de estimarlo."
```

**3. Pide fuentes y verifica:**
```
"Cita las secciones específicas del documento en que basas cada afirmación."
```

**4. Usa temperature baja para tareas factuales:**
```
temperature=0.0 no elimina alucinaciones pero las reduce
en tareas de extracción y análisis sobre documentos conocidos.
```

> **Regla de producción:** nunca despliegues un sistema de IA que presente datos factuales externos (leyes, estadísticas, precios) sin un paso de verificación humana o un sistema RAG con fuentes verificadas.

---

## 2.1.6 Comparativa de Arquitecturas: qué diferencia a los modelos actuales

No todos los LLMs son iguales. Las diferencias técnicas tienen consecuencias prácticas directas para elegir el modelo correcto (tema del módulo 2.3).

```
FAMILIA         FORTALEZA                    LIMITACIÓN
──────────────────────────────────────────────────────────
Claude (Opus)   Razonamiento complejo,       Más caro, más lento
                seguimiento de instrucciones
                largas, escritura matizada

Claude (Haiku)  Velocidad, coste bajo,       Razonamiento menos profundo
                tareas de clasificación

GPT-4o          Multimodal nativo (visión),  Contexto más limitado
                ecosistema amplio

Gemini 1.5      Contexto 1M tokens,          Menos preciso en instrucciones
                documentos muy largos        complejas

Llama 3 (open)  Sin coste de API,            Requiere infra propia,
                datos propios on-premise     peor en instrucción
```

> La elección de modelo es una decisión de ingeniería y negocio, no solo técnica. El módulo 2.3 desarrolla el framework de selección completo.

---

*Anterior: [1.3 Construcción del Caso de Negocio](../../modulo_1/1.3_caso_negocio/README.md) | Siguiente: [2.2 Prompt Engineering de Producción](../2.2_prompt_engineering/README.md)*
