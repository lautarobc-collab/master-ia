# 9.2 Políticas de IA Generativa en la Empresa

## 9.2.1 Por Qué Necesita Tu Empresa una Política de IA

Sin una política de IA, los empleados improvisan. Algunos usarán la IA de forma productiva; otros compartirán datos de clientes con servicios en la nube sin autorización; otros rechazarán usarla por miedo. La política de IA no es burocracia — es el marco que permite usar la IA con confianza.

```
CONSECUENCIAS DE NO TENER POLÍTICA DE IA:

  SIN POLÍTICA                        CON POLÍTICA
  ─────────────────────────────────   ─────────────────────────────────
  • Datos de clientes en ChatGPT      • Saben qué datos pueden usar
  • Contratos confidenciales en       • Herramientas aprobadas para
    herramientas de terceros            cada tipo de dato
  • Código interno en LLMs públicos   • Proceso para validar outputs
  • Cada departamento usa             • Consistencia en el uso
    herramientas diferentes           • Auditoría posible
  • Outputs sin validar               • Responsabilidad clara
  • Nadie sabe si el output es IA     • Etiquetado de contenido IA
  • Regulatorio: GDPR + AI Act        • Cumplimiento documentado
    sin gestionar
```

Una política efectiva no debe ser un documento de 50 páginas que nadie lee. Debe ser concreta, comprensible y accesible: ¿qué puedo hacer? ¿qué no puedo hacer? ¿con qué herramienta? ¿cómo valido el resultado?

---

## 9.2.2 Estructura de una Política de IA Corporativa

```
ESTRUCTURA RECOMENDADA — POLÍTICA DE IA GENERATIVA:

  SECCIÓN 1: PROPÓSITO Y ALCANCE
  ────────────────────────────────────────────────────────────
  • Por qué existe esta política
  • A quién aplica (todos los empleados, proveedores, terceros)
  • Qué cubre (IA generativa: LLMs, generadores de imagen, etc.)
  • Fecha de vigencia y proceso de revisión (semestral recomendado)

  SECCIÓN 2: HERRAMIENTAS APROBADAS
  ────────────────────────────────────────────────────────────
  • Lista de herramientas autorizadas con nivel de aprobación
  • Herramientas prohibidas (y por qué)
  • Proceso para solicitar aprobación de herramienta nueva
  • Herramientas en evaluación (estado)

  SECCIÓN 3: CLASIFICACIÓN DE DATOS Y USO PERMITIDO
  ────────────────────────────────────────────────────────────
  • Qué datos pueden entrar en herramientas de IA
  • Qué datos NO pueden salir de la empresa (lista)
  • Cómo anonimizar antes de usar IA con datos sensibles

  SECCIÓN 4: VALIDACIÓN DE OUTPUTS
  ────────────────────────────────────────────────────────────
  • Quién es responsable de validar el output antes de usarlo
  • Qué tipo de validación se requiere por caso de uso
  • Cómo etiquetar el contenido generado por IA

  SECCIÓN 5: USOS PROHIBIDOS
  ────────────────────────────────────────────────────────────
  • Lista explícita de lo que está prohibido

  SECCIÓN 6: GOBERNANZA Y RESPONSABILIDAD
  ────────────────────────────────────────────────────────────
  • Quién aprueba nuevas herramientas y casos de uso
  • Proceso de reporte de incidentes
  • Consecuencias del incumplimiento

  SECCIÓN 7: FORMACIÓN Y SOPORTE
  ────────────────────────────────────────────────────────────
  • Formación obligatoria para uso de IA
  • Recursos de ayuda (canal de preguntas, AI Champion del área)
```

---

## 9.2.3 Clasificación de Datos para IA — El Núcleo de la Política

La clasificación de datos es la decisión más importante de la política. Si no está clara, todo lo demás falla.

```
CLASIFICACIÓN DE DATOS — 4 NIVELES:

  NIVEL 1 — PÚBLICO
  ┌──────────────────────────────────────────────────────────────┐
  │  Puede usarse sin restricción en cualquier herramienta IA.  │
  │  Ejemplos:                                                   │
  │  • Información ya publicada en la web de la empresa          │
  │  • Datos estadísticos agregados sin identificación           │
  │  • Materiales de marketing aprobados y publicados            │
  └──────────────────────────────────────────────────────────────┘

  NIVEL 2 — INTERNO
  ┌──────────────────────────────────────────────────────────────┐
  │  Solo herramientas aprobadas con DPA firmado.                │
  │  Ejemplos:                                                   │
  │  • Emails internos sin datos de clientes                     │
  │  • Documentos de proceso no confidenciales                   │
  │  • Presentaciones internas de resultados genéricos           │
  └──────────────────────────────────────────────────────────────┘

  NIVEL 3 — CONFIDENCIAL
  ┌──────────────────────────────────────────────────────────────┐
  │  Solo herramientas on-premise o con contrato específico.     │
  │  Datos personales de clientes/empleados o datos de negocio. │
  │  Ejemplos:                                                   │
  │  • Datos personales de clientes (nombre, email, teléfono)    │
  │  • Datos financieros de la empresa (P&L, previsiones)        │
  │  • Contratos y acuerdos comerciales                          │
  │  • Información de M&A o estrategia confidencial              │
  │  → Opción: anonimizar antes de usar IA externa               │
  └──────────────────────────────────────────────────────────────┘

  NIVEL 4 — RESTRINGIDO
  ┌──────────────────────────────────────────────────────────────┐
  │  NUNCA sale de la empresa. Ni siquiera a herramientas        │
  │  con DPA. Solo procesamiento local estrictamente controlado. │
  │  Ejemplos:                                                   │
  │  • Datos de categoría especial (salud, religión, sindicato)  │
  │  • Secretos industriales o código fuente propietario crítico │
  │  • Datos de menores                                          │
  │  • Información clasificada por contrato (NDA)                │
  └──────────────────────────────────────────────────────────────┘
```

---

## 9.2.4 Usos Prohibidos — Lista Clara y Sin Ambigüedades

```
LISTA DE USOS PROHIBIDOS — POLÍTICA DE IA:

  ENGAÑO E INTEGRIDAD
  ─────────────────────────────────────────────────────────────
  ✗ Usar IA para crear o difundir información falsa sobre la empresa,
    la competencia o cualquier persona o entidad
  ✗ Presentar como propio contenido generado por IA sin declararlo
    cuando hay obligación de hacerlo (informes regulados, etc.)
  ✗ Hacerse pasar por otra persona usando IA

  DATOS Y PRIVACIDAD
  ─────────────────────────────────────────────────────────────
  ✗ Introducir datos de nivel 3 o 4 en herramientas no autorizadas
  ✗ Usar IA para recopilar datos personales sin base legal
  ✗ Compartir outputs de IA que contengan datos personales
    sin verificar que no hay datos de terceros filtrados

  DISCRIMINACIÓN Y SESGOS
  ─────────────────────────────────────────────────────────────
  ✗ Usar IA en procesos de selección, evaluación o promoción
    sin revisión humana y protocolo anti-sesgo
  ✗ Usar atributos protegidos (género, edad, etnia, religión)
    como inputs en sistemas de decisión automatizada

  SEGURIDAD
  ─────────────────────────────────────────────────────────────
  ✗ Usar IA para generar código malicioso o exploits
  ✗ Usar IA para intentar evadir controles de seguridad internos
  ✗ Compartir credenciales o claves API de herramientas IA

  LEGAL Y PROPIEDAD INTELECTUAL
  ─────────────────────────────────────────────────────────────
  ✗ Usar IA para generar contenido que infrinja derechos de autor
  ✗ Registrar como marca o patentar contenido íntegramente generado
    por IA sin declararlo (en jurisdicciones que lo requieran)
```

---

## 9.2.5 Validación de Outputs — El Paso que Más Se Salta

La IA comete errores. Los "alucinaciones" (hechos falsos presentados con confianza) son el mayor riesgo operativo del uso de IA generativa. La política debe definir qué validación se requiere.

```
NIVELES DE VALIDACIÓN REQUERIDA:

  VALIDACIÓN BÁSICA (uso interno informal)
  ─────────────────────────────────────────────────────────────
  • Leer el output completo antes de usarlo
  • Verificar que no hay datos personales o confidenciales
    en el output (pueden filtrarse del contexto)
  • Ajustar el tono/estilo si es necesario

  VALIDACIÓN ESTÁNDAR (comunicaciones externas)
  ─────────────────────────────────────────────────────────────
  • Verificar todos los hechos y cifras contra fuentes primarias
  • Revisar que refleja la política actual de la empresa
  • Revisión por segunda persona (peer review)
  • Etiquetar como "asistido por IA" si la política lo requiere

  VALIDACIÓN RIGUROSA (documentos regulados o críticos)
  ─────────────────────────────────────────────────────────────
  • Revisión por experto de dominio (jurídico, financiero, técnico)
  • Verificación exhaustiva de todas las referencias
  • Aprobación formal antes de publicación o envío
  • Registro del proceso de validación

  PROHIBIDO SIN VALIDACIÓN RIGUROSA:
  ✗ Informes financieros auditados
  ✗ Documentos contractuales
  ✗ Contenido médico o de seguridad
  ✗ Comunicaciones reguladas (prospectos, folletos financieros)
  ✗ Decisiones automatizadas de alto impacto
```

**Plantilla de etiqueta para contenido IA** (adaptar a la empresa):

```
EJEMPLOS DE ETIQUETADO:

  Uso interno:
  [Borrador generado con asistencia de IA. Validado por: Nombre - Fecha]

  Uso externo (cuando aplica):
  [Contenido elaborado con asistencia de inteligencia artificial
   y revisado por expertos humanos de [Empresa].]

  En código:
  # Generated with AI assistance - reviewed by [engineer name]
```

---

*Anterior: [9.1 AI Act y GDPR](../9.1_ai_act_gdpr/README.md) | Siguiente: [9.3 Fricción Tecnológica y Gestión del Cambio](../9.3_friccion_adopcion/README.md)*
