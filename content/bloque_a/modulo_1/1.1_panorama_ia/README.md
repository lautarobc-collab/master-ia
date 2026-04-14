# 1.1 Panorama de la IA

## 1.1.1 Sesión de Bienvenida

Bienvenido al **Master en IA Aplicada y Optimización**.

Este programa está diseñado para profesionales que quieren dejar de hablar de IA y empezar a usarla de verdad en su trabajo. No necesitas saber programar para aprovechar el 80% del contenido. Sí necesitas estar dispuesto a cambiar cómo trabajas.

### Qué vas a conseguir al terminar

```
ANTES del master                    DESPUÉS del master
─────────────────────────────────────────────────────────
Usas ChatGPT de forma puntual   →   Diseñas flujos de trabajo con IA
Dependes de IT para automatizar →   Construyes tus propias automatizaciones
Generas documentos uno a uno    →   Produces documentos a escala con calidad
Tomas decisiones con intuición  →   Las apoyas con análisis IA en minutos
Ves la IA como una herramienta  →   La integras como capa de tu operación
```

### Cómo está organizado el master

El programa tiene **dos bloques**:

**Bloque A — Fundamentos y Arquitectura Empresarial** (lo que estás empezando ahora)
9 módulos que cubren desde cómo funcionan los LLMs hasta cómo construir agentes, automatizar con no-code y cumplir con la regulación europea.

**Bloque B — Tracks de Especialización**
5 tracks según tu perfil: productividad, marketing, carrera profesional, análisis financiero o emprendimiento. Cada track aplica lo del Bloque A a tu contexto concreto.

### Cómo sacar el máximo partido

```
1. Lee la teoría de cada sección — entiende el concepto antes de ejecutar
2. Ejecuta el laboratorio — el código es la mejor forma de fijar el conocimiento
3. Aplica a tu trabajo — cada módulo incluye casos de uso reales
4. No te saltes módulos — cada uno construye sobre el anterior
```

### Una nota sobre el ritmo

No hay prisa. Este es un programa autodidacta: tú marcas el ritmo. Lo importante no es terminarlo rápido sino terminar sabiendo hacer cosas nuevas que antes no podías.

---

## 1.1.2 Historia y Evolución: de los Sistemas Expertos a los LLMs

### Línea temporal técnica

```
1956  Conferencia de Dartmouth → nace el término "Inteligencia Artificial"
1970s Sistemas Expertos (MYCIN, DENDRAL) → reglas IF/THEN codificadas a mano
1986  Backpropagation → redes neuronales empiezan a aprender
1997  Deep Blue vence a Kasparov → IA simbólica en su cima
2012  AlexNet → Deep Learning explota con GPU + datos masivos
2017  "Attention Is All You Need" → nace la arquitectura Transformer
2018  BERT (Google), GPT-1 (OpenAI) → pre-entrenamiento + fine-tuning
2020  GPT-3 (175B parámetros) → emergencia del in-context learning
2022  ChatGPT → RLHF convierte LLMs en asistentes conversacionales
2024  Modelos multimodales, razonamiento, agentes autónomos
```

### Por qué el Transformer lo cambió todo

El mecanismo de **atención** permite que cada token del input "mire" a todos los demás simultáneamente. Esto supera las RNNs (procesaban secuencialmente, olvidaban contexto largo) y permite:
- Contextos de 100k+ tokens
- Paralelización masiva en GPU
- Capacidades emergentes no esperadas

---

## 1.1.3 Machine Learning y Deep Learning: Fundamentos

### Taxonomía técnica

| Tipo | Cómo aprende | Ejemplo |
|---|---|---|
| **ML Supervisado** | Ejemplos etiquetados (X → Y) | Clasificar emails spam |
| **ML No Supervisado** | Encuentra patrones sin etiquetas | Segmentación de clientes |
| **Reinforcement Learning** | Recompensas por acciones | RLHF en ChatGPT |
| **Deep Learning** | Redes neuronales profundas (>2 capas) | Visión, lenguaje, audio |

### El flujo de un LLM en producción

```
Input texto
    ↓
Tokenización  →  "Hola mundo" → [15496, 995]  (BPE tokens)
    ↓
Embedding     →  vector de 768-4096 dimensiones por token
    ↓
Transformer   →  N capas de atención + feed-forward
    ↓
Logits        →  probabilidad para cada token del vocabulario (~50k tokens)
    ↓
Sampling      →  temperatura + top-p filtran y seleccionan el siguiente token
    ↓
Output token  →  se repite hasta <EOS>
```

---

## 1.1.4 IA Generativa: Qué Cambia Realmente

### El cambio de paradigma

**Antes:** programas con reglas explícitas → frágiles, no escalan  
**Ahora:** modelos aprenden la distribución estadística del lenguaje humano

La IA generativa no "entiende" — **predice el siguiente token más probable** dado un contexto. Lo que parece razonamiento es la capacidad de comprimir y recombinar patrones de billones de textos.

### Impacto real en operaciones

| Área | Antes (automación clásica) | Ahora (IA Generativa) |
|---|---|---|
| Documentación | Templates rígidos | Generación adaptativa de contexto |
| Análisis | Dashboard estático | Conversación con datos |
| Decisiones | Reglas IF/THEN | Razonamiento sobre contexto complejo |
| Atención | FAQs predefinidas | Comprensión semántica real |

---

## 1.1.5 Mapa Actual de la Industria

### Proveedores de Modelos Fundacionales (Foundation Models)

```
┌─────────────────────────────────────────────────────────┐
│  FRONTIER MODELS (máxima capacidad)                     │
│  • OpenAI: GPT-4o, o1, o3                               │
│  • Anthropic: Claude 3.5 Sonnet, Claude 4               │
│  • Google: Gemini 1.5 Pro / Ultra                       │
│  • Meta: Llama 3.1 405B (open weights)                  │
├─────────────────────────────────────────────────────────┤
│  MODELOS ESPECIALIZADOS                                  │
│  • Mistral (Europa, eficiencia)                         │
│  • Cohere (enterprise RAG)                              │
│  • DeepSeek (razonamiento, bajo coste)                  │
├─────────────────────────────────────────────────────────┤
│  CAPA DE APLICACIÓN                                     │
│  • LangChain / LlamaIndex (orquestación)                │
│  • ChromaDB / Pinecone / Weaviate (vector stores)       │
│  • Weights & Biases (observabilidad y evaluación)       │
└─────────────────────────────────────────────────────────┘
```

### Criterios de selección en producción

| Criterio | Prioridad Alta | Modelo recomendado |
|---|---|---|
| Máxima calidad | Análisis complejo | Claude Opus / GPT-4o |
| Coste/velocidad | Alto volumen | Claude Haiku / GPT-4o-mini |
| Privacidad total | Datos sensibles | Llama 3 (on-premise) |
| Código | Desarrollo software | Claude Sonnet / DeepSeek Coder |

---

## 1.1.6 Tendencias que Redefinen la IA (2024-2025)

1. **Razonamiento extendido (o1/o3):** los modelos "piensan" antes de responder → mayor precisión en problemas complejos a costa de latencia
2. **Agentes autónomos:** LLMs + herramientas + memoria → ejecutan tareas de múltiples pasos sin intervención humana
3. **Multimodalidad nativa:** visión, audio y texto en un mismo modelo
4. **Context windows largas:** 128k-1M tokens → documentos completos en memoria
5. **Edge AI:** modelos pequeños (<7B) en dispositivos locales (privacidad + latencia cero)

---

## Conceptos Clave a Dominar

- **Token:** unidad mínima de texto que procesa el LLM (≈ 0.75 palabras en español)
- **Embedding:** representación vectorial del significado semántico
- **Fine-tuning:** ajustar un modelo pre-entrenado con datos propios
- **RLHF:** Reinforcement Learning from Human Feedback → alinea el modelo con preferencias humanas
- **Hallucination:** el modelo genera contenido plausible pero incorrecto

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Vaswani et al. (2017) — *Attention Is All You Need* → [arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
- OpenAI (2023) — *GPT-4 Technical Report* → [arxiv.org/abs/2303.08774](https://arxiv.org/abs/2303.08774)

**Informes de industria:**
- McKinsey (anual) — *The State of AI* → [mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) *(adopción empresarial, tendencias y ROI de IA a nivel global)*
- Stanford University (anual) — *AI Index Report* → [aiindex.stanford.edu/report/](https://aiindex.stanford.edu/report/) *(métricas anuales de progreso, inversión y adopción de IA)*

**Libros recomendados:**
- Iansiti & Lakhani (2020) — *Competing in the Age of AI* (HBR Press) — marco estratégico para entender cómo la IA redefine ventajas competitivas y modelos operativos
- Russell (2019) — *Human Compatible: AI and the Problem of Control* (Viking) — visión crítica sobre el desarrollo de la IA y sus implicaciones para el futuro

**Documentación oficial:**
- *Anthropic Documentation* → [docs.anthropic.com](https://docs.anthropic.com)

*Siguiente: [1.2 IA como Palanca Estratégica](../1.2_IA_Palanca_Estrategica/README.md)*
