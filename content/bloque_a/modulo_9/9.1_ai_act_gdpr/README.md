# 9.1 AI Act Europeo y GDPR

## 9.1.1 El AI Act — El Marco Regulatorio de la IA en Europa

El AI Act (Reglamento de IA de la Unión Europea) es la primera legislación integral sobre inteligencia artificial en el mundo, aprobado en 2024 y con aplicación progresiva hasta 2026. Afecta a toda empresa que opere en la UE, aunque su sede esté fuera de Europa.

```
CRONOGRAMA DE APLICACIÓN DEL AI ACT:

  Agosto 2024      → Entrada en vigor del Reglamento
  Febrero 2025     → Prohibiciones de IA de riesgo inaceptable (Título II)
  Agosto 2025      → Obligaciones de modelos de IA de uso general (GPAI)
  Agosto 2026      → Aplicación plena para sistemas de IA de alto riesgo
  Agosto 2027      → Sistemas ya en uso antes del Reglamento (excepción)

  ÁMBITO DE APLICACIÓN:
  ✓ Proveedores de sistemas IA que operen en la UE
  ✓ Usuarios de sistemas IA establecidos en la UE
  ✓ Proveedores y usuarios fuera de la UE si el output
    afecta a personas dentro de la UE
  ✗ IA para uso militar y defensa nacional (excluida)
  ✗ IA para investigación científica pura (excluida)
```

**Para directivos**: el AI Act no prohíbe la IA, la regula según el riesgo que genera. La mayoría de los casos de uso empresariales caen en la categoría de riesgo limitado o mínimo, con obligaciones asumibles.

---

## 9.1.2 Los Cuatro Niveles de Riesgo

El AI Act clasifica los sistemas de IA en cuatro categorías según el riesgo potencial para las personas:

```
PIRÁMIDE DE RIESGO — AI ACT:

        ████████████████
        █  INACEPTABLE  █  ← PROHIBIDOS
        ████████████████
              │
              │ Manipulación conductual subliminal
              │ Puntuación social por autoridades públicas
              │ Identificación biométrica en tiempo real en espacios públicos
              │ Explotación de vulnerabilidades de grupos específicos

        ████████████████████████
        █     ALTO RIESGO      █  ← Obligaciones estrictas
        ████████████████████████
              │
              │ Infraestructuras críticas
              │ Educación (acceso, evaluación)
              │ Empleo (selección, gestión de personas)
              │ Servicios públicos esenciales (crédito, seguros, salud)
              │ Cumplimiento de la ley
              │ Administración de justicia
              │ Gestión de fronteras

        ████████████████████████████████
        █     RIESGO LIMITADO          █  ← Obligaciones de transparencia
        ████████████████████████████████
              │
              │ Chatbots (deben identificarse como IA)
              │ Contenido generado por IA (debe identificarse)
              │ Sistemas de deepfake

        ████████████████████████████████████████
        █          RIESGO MÍNIMO               █  ← Sin obligaciones específicas
        ████████████████████████████████████████
              │
              │ Filtros de spam
              │ IA en videojuegos
              │ Herramientas de productividad
              │ Mayoría de herramientas empresariales internas
```

---

## 9.1.3 Obligaciones por Categoría

### Sistemas de Alto Riesgo — Checklist Completo

```
OBLIGACIONES PARA SISTEMAS IA DE ALTO RIESGO:

  ANTES DE PONER EN USO:
  ☐ Evaluación de conformidad (interna o por tercero notificado)
  ☐ Documentación técnica completa del sistema
  ☐ Registro en base de datos de la UE (para algunos casos)
  ☐ Marcado CE (para sistemas que requieran conformidad UE)

  DISEÑO DEL SISTEMA:
  ☐ Sistema de gestión de riesgos documentado y actualizado
  ☐ Datos de entrenamiento de calidad y sin sesgos inaceptables
  ☐ Supervisión humana real y efectiva (no solo nominal)
  ☐ Robustez, precisión y ciberseguridad verificadas

  DURANTE LA OPERACIÓN:
  ☐ Logs automáticos de funcionamiento (con fecha y hora)
  ☐ Mecanismo de parada de emergencia
  ☐ Información clara al usuario de que interactúa con IA
  ☐ Plan de gestión post-mercado (mejoras, incidencias)

  PARA EL USUARIO DEL SISTEMA (si no es el proveedor):
  ☐ Usar el sistema según las instrucciones del proveedor
  ☐ Supervisión humana durante el uso
  ☐ Informar al proveedor de incidencias graves
  ☐ Monitoreo del funcionamiento
```

### Sistemas de Riesgo Limitado — Transparencia Obligatoria

```
OBLIGACIONES DE TRANSPARENCIA:

  Chatbots con IA:
  → Deben indicar que son IA cuando el usuario lo pregunta
  → No pueden hacerse pasar por humanos de forma engañosa

  Contenido generado por IA (imágenes, audio, video, texto):
  → Debe estar marcado como generado por IA
  → Aplica especialmente a deepfakes y contenido audiovisual

  Sistemas de reconocimiento de emociones / biométrico:
  → Informar a las personas que están siendo analizadas
```

---

## 9.1.4 Compatibilidad AI Act — GDPR

El AI Act y el GDPR se solapan en varios puntos. Cumplir uno no garantiza cumplir el otro — hay que gestionar ambos:

```
INTERSECCIONES AI ACT — GDPR:

  DATOS PERSONALES EN ENTRENAMIENTO
  ─────────────────────────────────────────────────────────────
  AI Act: datos de entrenamiento deben ser de calidad
  GDPR:   datos personales requieren base legal + principios
          (minimización, limitación de finalidad)
  → Acción: auditar los datos usados para entrenar/ajustar
    modelos internos y documentar la base legal

  DECISIONES AUTOMATIZADAS
  ─────────────────────────────────────────────────────────────
  AI Act: sistemas de alto riesgo requieren supervisión humana
  GDPR:   Art. 22 — derecho a no ser objeto de decisión
          totalmente automatizada con efectos significativos
          (con excepciones: contrato, ley, consentimiento explícito)
  → Acción: para crédito, empleo, seguros — garantizar revisión
    humana efectiva y derecho de recurso documentado

  TRANSPARENCIA E INFORMACIÓN
  ─────────────────────────────────────────────────────────────
  AI Act: sistemas de riesgo limitado deben identificarse
  GDPR:   Art. 13/14 — informar del uso de IA en decisiones
  → Acción: actualizar avisos de privacidad para mencionar
    el uso de IA y cómo afecta a los interesados

  PROTECCIÓN DESDE EL DISEÑO
  ─────────────────────────────────────────────────────────────
  AI Act: gestión de riesgos desde el diseño
  GDPR:   privacy by design (Art. 25)
  → Acción: integrar evaluación de impacto (EIPD/DPIA) en
    el proceso de desarrollo de sistemas IA con datos personales
```

---

## 9.1.5 Clasificación Práctica — ¿Dónde Cae Tu Sistema?

Una guía rápida para clasificar los sistemas IA más comunes en empresa:

| Sistema IA | Categoría probable | Obligación principal |
|------------|-------------------|---------------------|
| Chatbot de atención al cliente | Riesgo limitado | Identificarse como IA |
| Motor de decisión de crédito | Alto riesgo | Conformidad completa + supervisión humana |
| Herramienta interna de resúmenes | Mínimo | Sin obligaciones específicas |
| Sistema de selección de CVs | Alto riesgo | Conformidad completa + no discriminación |
| Clasificador de emails internos | Mínimo | Sin obligaciones específicas |
| Análisis de sentimiento de empleados | Alto riesgo | Conformidad + evaluación impacto |
| Generador de contenido de marketing | Riesgo limitado | Marcar como IA si procede |
| Motor de pricing dinámico | Mínimo-limitado | Transparencia si afecta a consumidores |

```
ÁRBOL DE DECISIÓN — CLASIFICACIÓN DE RIESGO:

  ¿El sistema toma decisiones con efectos significativos
  sobre personas (empleo, crédito, salud, educación)?
  ├─ SÍ → ALTO RIESGO (obligaciones estrictas)
  └─ NO
     ├─ ¿El sistema interactúa con personas haciéndose
     │   pasar por humano o generando contenido engañoso?
     │   ├─ SÍ → RIESGO LIMITADO (transparencia)
     │   └─ NO → RIESGO MÍNIMO (sin obligaciones específicas)
     └─ ¿Manipula conductas de personas sin su conocimiento
         o aprovecha vulnerabilidades?
         ├─ SÍ → INACEPTABLE (prohibido)
         └─ NO → MÍNIMO o LIMITADO
```

**Checklist de evaluación inicial para directivos**:

```
CHECKLIST DE EVALUACIÓN — ¿NECESITO CUMPLIR EL AI ACT?

  ☐ ¿La empresa usa o proporciona sistemas de IA?
  ☐ ¿Opera en mercados de la UE o afecta a ciudadanos de la UE?
  ☐ ¿Algún sistema toma decisiones sobre personas (empleo, crédito)?
  ☐ ¿Los chatbots se identifican como IA?
  ☐ ¿El contenido IA se etiqueta?
  ☐ ¿Existe supervisión humana real en decisiones importantes?
  ☐ ¿Los avisos de privacidad mencionan el uso de IA?
  ☐ ¿Hay un responsable interno de cumplimiento IA?
```

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Bai et al. / Anthropic (2022) — *Constitutional AI: Harmlessness from AI Feedback* → [arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)

**Informes de industria:**
- Stanford University (anual) — *AI Index Report* → [aiindex.stanford.edu/report/](https://aiindex.stanford.edu/report/) *(análisis comparativo de marcos regulatorios de IA a nivel global)*
- McKinsey (anual) — *The State of AI* → [mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) *(impacto del AI Act en la adopción empresarial y el cumplimiento)*

**Libros recomendados:**
- Christl & Spiekermann (2016) — *Networks of Control* — análisis de los mecanismos de vigilancia y control de datos que subyacen a la regulación GDPR y el AI Act

**Documentación oficial:**
- *EU AI Act (texto oficial en español)* → [eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689)
- *GDPR (texto oficial)* → [gdpr-info.eu](https://gdpr-info.eu)
- *NIST AI Risk Management Framework* → [nist.gov/artificial-intelligence/ai-risk-management-framework](https://www.nist.gov/artificial-intelligence/ai-risk-management-framework)

*Anterior: [8.3 Pipelines Multimodales](../../modulo_8/8.3_pipelines_multimodales/README.md) | Siguiente: [9.2 Políticas de IA Generativa en la Empresa](../9.2_politicas_ia/README.md)*
