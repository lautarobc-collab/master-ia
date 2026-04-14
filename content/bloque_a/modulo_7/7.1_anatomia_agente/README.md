# 7.1 Anatomía de un Agente IA

## 7.1.1 Agente vs. Chatbot — La Diferencia Fundamental

La palabra "agente" se usa tanto en IA que ha perdido precisión. Para este módulo, utilizaremos una definición clara y operativa:

```
ESPECTRO DE AUTONOMÍA IA:

  CHATBOT SIMPLE                              AGENTE AUTÓNOMO
  ─────────────────────────────────────────────────────────────
  "Responde esta          "Analiza la situación,    "Ejecuta el proyecto
   pregunta"              decide qué hacer, hazlo    completo: investiga,
                          y reporta el resultado"    planifica, actúa"

  • 1 turno               • Múltiples pasos          • Objetivo de alto nivel
  • Sin memoria           • Usa herramientas         • Toma decisiones
  • Sin acciones          • Persiste estado           • Colabora con otros agentes
  • Reactivo              • Semi-proactivo           • Proactivo

  EJEMPLOS:               EJEMPLOS:                  EJEMPLOS:
  FAQ bot                 Asistente de reuniones     Agente de investigación
  Generador de texto      Procesador de facturas     Agente de ventas
  Clasificador            Agente de soporte          Agente de planificación
```

**Definición operativa para directivos**: un agente IA es un sistema que, dado un objetivo, puede *planificar* los pasos necesarios, *ejecutar* acciones (consultar sistemas, enviar emails, crear documentos) y *adaptar* su plan en función de los resultados que obtiene, hasta alcanzar el objetivo o pedir ayuda humana.

---

## 7.1.2 El Bucle Percepción–Razonamiento–Acción

Todo agente IA sigue este ciclo de forma iterativa hasta completar la tarea o alcanzar un límite:

```
BUCLE DEL AGENTE (ReAct: Reasoning + Acting):

  ┌──────────────────────────────────────────────────────────┐
  │                    OBJETIVO / TAREA                      │
  └────────────────────────────┬─────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │    PERCEPCIÓN       │
                    │  ─────────────────  │
                    │  ¿Qué sé ahora?     │
                    │  • Objetivo inicial │
                    │  • Resultados prev. │
                    │  • Estado del mundo │
                    │  • Contexto/memoria │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │    RAZONAMIENTO     │
                    │  ─────────────────  │
                    │  ¿Qué debo hacer?   │
                    │  • Pensar en voz    │
                    │    alta (chain of   │
                    │    thought)         │
                    │  • Elegir acción    │
                    │  • Preparar params  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │      ACCIÓN         │
                    │  ─────────────────  │
                    │  • Llamar herram.   │
                    │  • Escribir output  │
                    │  • Pedir aprobación │
                    │  • Esperar resultado│
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   ¿OBJETIVO         │
                    │   ALCANZADO?        │
                    └──────┬──────┬───────┘
                           │ NO   │ SÍ
                           │      └──→ FIN: entregar resultado
                           └──→ volver a PERCEPCIÓN
```

### Ejemplo paso a paso — Agente de investigación de proveedor

```
TAREA: "Investiga a CloudServ S.L. y prepara un informe de due diligence"

CICLO 1:
  Percepción: Tengo el nombre de la empresa. No sé nada más.
  Razonamiento: Debo buscar información pública. Usaré la herramienta web_search.
  Acción: web_search("CloudServ S.L. España empresa tecnología")
  Resultado: 5 artículos, web corporativa, perfil LinkedIn

CICLO 2:
  Percepción: Sé que es una empresa de 80 empleados, fundada en 2019, con sede en Madrid.
  Razonamiento: Debo verificar si tiene litigios o noticias negativas.
  Acción: web_search("CloudServ S.L. demanda escándalo incidente")
  Resultado: Sin resultados preocupantes

CICLO 3:
  Percepción: Tengo datos suficientes para redactar el informe.
  Razonamiento: Objetivo alcanzado. Formataré el informe.
  Acción: create_document(título, contenido estructurado)
  Resultado: Documento creado en la carpeta de Due Diligence

FIN: Informe listo. Notificar al usuario.
```

---

## 7.1.3 Memoria de Agente — Los Cuatro Tipos

La memoria determina qué sabe el agente y por cuánto tiempo. Es crucial para diseñar agentes que no "olviden" contexto crítico.

```
TIPOS DE MEMORIA EN AGENTES IA:

  ┌─────────────────────┬──────────────────────────────────────────┐
  │ TIPO                │ DESCRIPCIÓN Y EJEMPLO                    │
  ├─────────────────────┼──────────────────────────────────────────┤
  │ Memoria en contexto │ Lo que está en la ventana de conversación │
  │ (Working memory)    │ actual. Dura mientras dura la sesión.    │
  │                     │ Ej: el hilo de una tarea en curso        │
  ├─────────────────────┼──────────────────────────────────────────┤
  │ Memoria episódica   │ Registro de acciones y resultados        │
  │ (logs/historial)    │ pasados, almacenada en BD o archivos.    │
  │                     │ Ej: "la semana pasada procesé 47 facturas"│
  ├─────────────────────┼──────────────────────────────────────────┤
  │ Memoria semántica   │ Conocimiento del dominio: la empresa,    │
  │ (base de conoc.)    │ sus productos, clientes, políticas.      │
  │                     │ Ej: RAG sobre documentos corporativos    │
  ├─────────────────────┼──────────────────────────────────────────┤
  │ Memoria procedural  │ Las instrucciones y herramientas que     │
  │ (system prompt)     │ definen cómo actuar. Permanente.         │
  │                     │ Ej: el system prompt del agente          │
  └─────────────────────┴──────────────────────────────────────────┘
```

**Implicación práctica**: cuando un agente "se equivoca" en algo que ya sabe, generalmente es un fallo de memoria. O la información no está en contexto, o no está en la base de conocimiento, o el system prompt no incluye esa regla.

---

## 7.1.4 Tipos de Agentes Empresariales

En el entorno corporativo, los agentes más comunes responden a estos patrones:

```
TAXONOMÍA DE AGENTES EMPRESARIALES:

  1. AGENTE DE PROCESO (el más común)
  ─────────────────────────────────────────────────────────────
  Automatiza un proceso lineal con pasos definidos.
  No improvisa — sigue un flujo establecido por el negocio.
  
  Ejemplos:
    • Agente de onboarding: incorpora un nuevo empleado (crea cuenta,
      asigna equipos, envía manuales, agenda sesiones de bienvenida)
    • Agente de facturación: descarga factura, extrae datos, valida
      contra pedido, registra en ERP, paga o escala
  
  Complejidad: baja-media | Riesgo: bajo

  2. AGENTE DE INVESTIGACIÓN (el más potente para conocimiento)
  ─────────────────────────────────────────────────────────────
  Dado un objetivo de información, navega, recopila y sintetiza.
  
  Ejemplos:
    • Análisis de mercado: investiga competidores, precios, tendencias
    • Due diligence: recopila información pública sobre empresa/persona
    • Monitoreo de prensa: detecta menciones relevantes y alerta
  
  Complejidad: media | Riesgo: medio (calidad de fuentes)

  3. AGENTE DE DECISIÓN (el más regulado)
  ─────────────────────────────────────────────────────────────
  Evalúa situaciones y toma o recomienda decisiones.
  Siempre debe tener human-in-the-loop para decisiones con impacto.
  
  Ejemplos:
    • Agente de scoring: evalúa solicitudes de crédito (ver módulo 6.2)
    • Agente de riesgo: clasifica y prioriza incidencias de seguridad
    • Agente de pricing: ajusta precios dinámicamente
  
  Complejidad: alta | Riesgo: alto (auditoría obligatoria)

  4. AGENTE MULTI-AGENTE (el más avanzado)
  ─────────────────────────────────────────────────────────────
  Un agente orquestador coordina a otros agentes especializados.
  
  Ejemplo:
    Agente CEO (orquestador)
    ├── Agente Investigación → datos del mercado
    ├── Agente Análisis → interpreta los datos
    └── Agente Redacción → escribe el informe final
  
  Complejidad: muy alta | Riesgo: variable (depende de los sub-agentes)
```

---

## 7.1.5 Cuándo (No) Usar Agentes

Los agentes son poderosos pero no siempre son la solución correcta. Este cuadro ayuda a decidir:

```
¿DEBO USAR UN AGENTE?

  SÍ, considerar agente cuando:
  ✓ La tarea requiere múltiples pasos no predecibles de antemano
  ✓ Se necesita consultar o actuar sobre varios sistemas externos
  ✓ El proceso tiene ramificaciones según los resultados intermedios
  ✓ El volumen justifica la inversión en diseño y seguridad
  ✓ Un humano tarda > 30 min en hacer la tarea manualmente

  NO usar agente (usar solución más simple) cuando:
  ✗ La tarea es siempre la misma secuencia de pasos (usar workflow)
  ✗ Solo es transformar texto (usar LLM directo sin herramientas)
  ✗ El tiempo de respuesta debe ser < 1 segundo (agentes son lentos)
  ✗ La tarea es tan crítica que cualquier error es inaceptable
  ✗ El equipo no tiene capacidad de mantener el sistema

  SEÑALES DE ALARMA:
  ⚠ "El agente hace lo que quiere" → falta de guardrails
  ⚠ "El agente nunca termina" → ciclos sin condición de salida
  ⚠ "El agente inventa datos" → falta de grounding en fuentes reales
  ⚠ "Nadie sabe qué hace el agente" → falta de logging
```

**Consejo para directivos**: empezad por automatizar UN proceso bien delimitado con un agente de proceso (tipo 1). Los resultados son más predecibles, el riesgo es menor y el aprendizaje se transfiere a proyectos más ambiciosos.

---

*Anterior: [6.3 Monitoreo y Resiliencia](../../modulo_6/6.3_monitoreo_resiliencia/README.md) | Siguiente: [7.2 Tool-Calling y Herramientas](../7.2_tool_calling/README.md)*
