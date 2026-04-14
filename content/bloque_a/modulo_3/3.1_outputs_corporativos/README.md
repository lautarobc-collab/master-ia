# 3.1 Ingeniería de Outputs Corporativos

## 3.1.1 El Problema de los Outputs Genéricos

El mayor coste oculto de la IA corporativa no es la API — es el tiempo que el equipo invierte en reescribir lo que la IA genera. Si cada output requiere una revisión profunda, no hay automatización real: solo has cambiado quién hace el borrador.

La ingeniería de outputs es la disciplina de diseñar el sistema para que el primer borrador de la IA sea el 90% del producto final, no el 40%.

```
Sin ingeniería de outputs:
  IA genera → humano reescribe 60% → 45 minutos de trabajo
  Ahorro real: 15 minutos (25% del proceso)

Con ingeniería de outputs:
  IA genera con plantilla + ejemplos → humano valida y ajusta 10%
  Ahorro real: 90 minutos (75% del proceso)

La diferencia es el diseño del prompt y del formato de salida.
```

---

## 3.1.2 Los 5 Tipos de Output Corporativo y Cómo Diseñarlos

### Tipo 1 — Informes ejecutivos

El informe ejecutivo tiene una estructura rígida no negociable: el lector tardará 90 segundos en leerlo y necesita poder tomar una decisión.

**Estructura estándar:**
```
1. Titular (1 frase) — la conclusión, no el tema
2. Contexto (2-3 frases) — qué pasó y por qué importa
3. Hallazgos clave (3 bullets) — datos, no interpretaciones
4. Implicaciones (2-3 frases) — qué significa para el negocio
5. Recomendación (1 frase + criterio de éxito)
```

**Prompt para informe ejecutivo:**
```
Redacta un informe ejecutivo de máximo 200 palabras sobre [TEMA].
Audiencia: [ROL] que tomará una decisión en los próximos [PLAZO].
Estructura obligatoria:
  TITULAR: [conclusión, no el tema]
  CONTEXTO: [2-3 frases]
  HALLAZGOS: [3 bullets con datos]
  IMPLICACIÓN: [qué significa para el negocio]
  RECOMENDACIÓN: [acción concreta + criterio de éxito]
No uses jerga técnica ni palabras como "sinergias" o "innovador".
```

### Tipo 2 — Comunicaciones internas

Los memos y comunicaciones internas fallan cuando son demasiado largos o demasiado vagos. El estándar de producción:

```
Asunto: [Acción requerida] — [Tema] — [Fecha límite si aplica]

[Párrafo 1: Qué está pasando y por qué importa a esta audiencia]
[Párrafo 2: Lo que se espera de ellos específicamente]
[Párrafo 3: Próximos pasos con responsables y fechas]

¿Preguntas? [Contacto específico, no "el equipo"]
```

### Tipo 3 — Propuestas comerciales

La propuesta comercial generada por IA falla cuando suena a plantilla. El antídoto es inyectar especificidad del cliente en el prompt:

```
Elementos específicos del cliente que DEBEN aparecer:
  · Problema concreto mencionado en la reunión
  · Nombre del interlocutor y su rol
  · Referencia a su sector/empresa
  · Métrica que les importa (no la genérica del mercado)
```

### Tipo 4 — Documentación de procesos (SOPs)

Los SOPs generados por IA son habitualmente superficiales. Para hacerlos operativos:

```
El SOP debe responder, en orden:
  1. Cuándo se ejecuta este proceso (trigger)
  2. Quién es el responsable y quién es notificado
  3. Pasos numerados con el actor en cada paso
  4. Qué hacer si el paso falla (excepción)
  5. Criterio de éxito — cómo sé que está bien hecho
  6. Tiempo estimado total
```

### Tipo 5 — Análisis y reportes de datos

El output de análisis de datos debe separar siempre los hechos de la interpretación:

```
Estructura de análisis fiable:
  DATOS (lo que dice el número)
  CONTEXTO (con qué comparamos)
  INTERPRETACIÓN (qué puede significar — con grado de certeza)
  LIMITACIÓN (qué no sabemos o podría sesgar)
  ACCIÓN SUGERIDA (si aplica)
```

---

## 3.1.3 Formato como Contrato: JSON, Markdown y Texto Plano

El formato de salida no es estético — es funcional. Define cómo el output se integra en el sistema siguiente.

### Cuándo usar JSON
- El output es input de otro sistema (CRM, ERP, base de datos)
- Necesitas comparar outputs entre sí
- El formato debe ser idéntico en cada ejecución

```json
{
  "tipo": "reclamacion",
  "urgencia": "alta",
  "departamento": "facturacion",
  "accion_recomendada": "contactar cliente en < 4h",
  "confianza": 0.92
}
```

### Cuándo usar Markdown
- El output va a ser leído por humanos en una interfaz web o Notion
- Necesitas jerarquía visual (headers, listas, tablas)
- El documento tiene múltiples secciones

### Cuándo usar texto plano
- El output va directamente a un email
- Se imprime o se incluye en un PDF
- La audiencia usa herramientas sin renderizado de Markdown

---

## 3.1.4 Consistencia a Escala: el Sistema de Plantillas

Un sistema de plantillas bien construido garantiza que 10 personas usando la IA produzcan outputs indistinguibles en formato y calidad.

### Anatomía de una plantilla de producción

```
[NOMBRE_PLANTILLA] v[VERSION]
Propósito: [una frase]
Modelo recomendado: [Haiku/Sonnet/Opus]
Temperatura: [valor]
Max tokens: [valor]
Última actualización: [fecha] — [qué cambió]

─── SYSTEM PROMPT ───────────────────────────────
[Rol, restricciones permanentes, formato base]

─── USER PROMPT ─────────────────────────────────
[Instrucción con variables marcadas entre {LLAVES}]

─── VARIABLES ───────────────────────────────────
{EMPRESA}: nombre de la empresa cliente
{SECTOR}: sector de actividad
{AUDIENCIA}: rol del lector final
{DATOS}: los datos o documento de referencia

─── EJEMPLO DE OUTPUT ESPERADO ──────────────────
[Un ejemplo real de output aceptable]

─── CRITERIO DE CALIDAD ─────────────────────────
☐ No hay campos vacíos sin justificación
☐ El tono es apropiado para {AUDIENCIA}
☐ La longitud está dentro del rango definido
☐ No hay afirmaciones sin base en {DATOS}
```

---

## 3.1.5 Métricas de Calidad del Output

No puedes mejorar lo que no mides. Estas son las métricas operativas para evaluar la calidad de outputs en producción:

| Métrica | Definición | Objetivo |
|---|---|---|
| **Tasa de aprobación directa** | % outputs usados sin edición | > 70% |
| **Tasa de rechazo** | % outputs descartados totalmente | < 5% |
| **Tiempo de revisión medio** | Minutos de edición por output | < 5 min |
| **Tasa de alucinación** | % outputs con dato inventado | < 1% |
| **Consistencia de formato** | % outputs con formato correcto | > 98% |

> Implementa una revisión mensual de 20 outputs aleatorios. Si la tasa de aprobación directa baja del 70%, el prompt necesita revisión.

---

*Anterior: [2.3 Selección Estratégica de Modelos](../../modulo_2/2.3_seleccion_modelos/README.md) | Siguiente: [3.2 Identidad Comunicativa y Tono](../3.2_identidad_comunicativa/README.md)*
