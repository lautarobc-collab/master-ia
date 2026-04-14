# 4.2 Curación de Bases Documentales

## 4.2.1 Por qué la Calidad de los Documentos Determina la Calidad del Asistente

En RAG, el principio es simple: *garbage in, garbage out*. Un asistente solo puede ser tan bueno como los documentos que tiene disponibles. El 80% de los proyectos RAG fracasan no por problemas técnicos, sino por una base documental mal curada.

```
Problemas típicos en bases documentales empresariales:
  · Documentos duplicados con versiones distintas sin fecha clara
  · PDFs escaneados sin OCR (imagen, no texto)
  · Documentos obsoletos mezclados con los vigentes
  · Información contradictoria entre departamentos
  · Documentos con tablas que el extractor no procesa bien
  · Información sensible que no debería estar en el sistema
```

---

## 4.2.2 El Proceso de Curación en 5 Pasos

### Paso 1 — Inventario
Antes de indexar, mapea qué tienes. Crea un registro con: nombre, tipo, fecha de creación, fecha de última actualización, propietario, estado (vigente/obsoleto/incompleto).

### Paso 2 — Limpieza
```
Limpieza técnica (automatable):
  · Extraer texto de PDFs (pdfplumber, PyMuPDF)
  · Normalizar encoding (UTF-8)
  · Eliminar headers/footers repetitivos
  · Limpiar caracteres especiales y espacios múltiples

Limpieza de contenido (requiere criterio humano):
  · Identificar y eliminar versiones obsoletas
  · Resolver contradicciones entre documentos
  · Marcar información sensible para exclusión
```

### Paso 3 — Enriquecimiento de metadatos
Cada documento debe tener metadatos que el sistema pueda usar para filtrar:
```json
{
  "id": "politica_devoluciones_v3",
  "titulo": "Política de Devoluciones",
  "version": "3.0",
  "fecha_vigencia": "2025-01-01",
  "departamento": "atencion_cliente",
  "tipo": "politica",
  "audiencia": ["clientes", "agentes_soporte"],
  "estado": "vigente"
}
```

### Paso 4 — Estrategia de chunking por tipo de documento

```
TIPO              ESTRATEGIA           CHUNK SIZE
─────────────────────────────────────────────────
Contratos         Por cláusula         200-400 tokens
Políticas         Por sección          300-500 tokens
FAQs              Por par Q&A          100-200 tokens
Emails            Por email            Variable
Informes          Por sección          400-600 tokens
Tablas/datos      Fila por fila        50-100 tokens
```

### Paso 5 — Mantenimiento continuo
```
Frecuencia de actualización por tipo:
  · Políticas internas:     cada vez que cambian (trigger en aprobación)
  · Documentación técnica:  al publicar nueva versión
  · Preguntas frecuentes:   mensual (revisar nuevas preguntas de soporte)
  · Normativa:              al publicarse cambios regulatorios
```

---

## 4.2.3 Tratamiento de Documentos Problemáticos

### PDFs con tablas

Las tablas en PDF son el caso más problemático. El extractor de texto las lineariza y pierde la estructura.

```
Estrategias:
  1. Extraer tablas con pdfplumber (detecta coordenadas de celdas)
  2. Convertir tabla a Markdown antes de indexar
  3. Para tablas críticas: mantener una versión CSV indexada separada
  4. Incluir descripción textual de la tabla como chunk adicional
```

### Documentos con versionado conflictivo

```
Política recomendada:
  · Solo indexar la versión VIGENTE
  · Incluir en metadatos: "sustituye_a": ["v1.0", "v2.0"]
  · Archivar versiones anteriores en carpeta separada (no indexada)
  · Añadir al chunk: "Versión X — vigente desde [fecha]"
```

### Información sensible (RGPD, datos de personas)

```
Datos que NUNCA deben entrar en el RAG:
  · Nombres y datos personales de empleados o clientes
  · Datos financieros individuales
  · Información de salario o evaluaciones personales
  · Credenciales y contraseñas (aunque esté en un documento)

Proceso de sanitización:
  · Pasar por detector de PII antes de indexar
  · Sustituir con [REDACTED] o [NOMBRE_EMPLEADO]
  · Documentar qué se ha redactado y por qué
```

---

## 4.2.4 Arquitectura de la Base Documental

```
ESTRUCTURA DE CARPETAS RECOMENDADA:

base_documental/
├── vigentes/           ← lo que se indexa
│   ├── politicas/
│   ├── procedimientos/
│   ├── productos/
│   └── normativa/
├── archivo/            ← versiones antiguas, no indexadas
├── revision/           ← documentos pendientes de validación
├── excluidos/          ← información sensible, no indexar
└── metadatos.json      ← registro de todos los documentos
```

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Lewis et al. (2020) — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* → [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)
- Liu et al. (2023) — *Lost in the Middle: How Language Models Use Long Contexts* → [arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172)

**Informes de industria:**
- McKinsey (anual) — *The State of AI* → [mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) *(problemas de calidad documental como causa principal de fracaso en proyectos RAG)*

**Libros recomendados:**
- Christl & Spiekermann (2016) — *Networks of Control* — análisis de los riesgos de privacidad en sistemas de gestión documental y bases de datos corporativas

**Documentación oficial:**
- *EU AI Act (texto oficial)* → [eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689) *(requisitos de calidad de datos y documentación en sistemas IA)*
- *GDPR* → [gdpr-info.eu](https://gdpr-info.eu) *(obligaciones sobre datos personales en bases documentales indexadas por sistemas IA)*

*Anterior: [4.1 Fundamentos de RAG](../4.1_fundamentos_rag/README.md) | Siguiente: [4.3 Diseño de Asistentes Seguros](../4.3_asistentes_seguros/README.md)*
