# 3.3 Validación y Quality Assurance

## 3.3.1 Por qué el QA de IA es Diferente al QA de Software

En software tradicional, un test pasa o falla de forma binaria. En IA, la salida es probabilística: el mismo prompt puede dar resultados distintos en cada ejecución, y "correcto" depende del contexto y del juicio humano.

Esto no significa que no se pueda medir — significa que hay que medir de forma distinta.

```
QA de software:         assert resultado == valor_esperado   (binario)
QA de IA:               ¿El output cumple los criterios de calidad?  (gradual)
                        ¿El formato es correcto?             (binario — sí se puede)
                        ¿El contenido es factualmente correcto? (requiere verificación)
                        ¿El tono es el adecuado?            (subjetivo — necesita rúbrica)
```

---

## 3.3.2 Los 4 Niveles de Validación

### Nivel 1 — Validación de formato (automática, 100% cobertura)
Comprueba que el output tiene la estructura esperada. No requiere juicio humano.

```python
def validar_formato_json(output: str, campos_requeridos: list) -> bool:
    try:
        data = json.loads(output)
        return all(campo in data for campo in campos_requeridos)
    except:
        return False

# Ejemplo: todo output de clasificación debe tener estos campos
CAMPOS = ["categoria", "urgencia", "confianza"]
```

### Nivel 2 — Validación de contenido con IA (automática, 100% cobertura)
Usa un segundo modelo (evaluador) para verificar que el contenido del output es coherente con el input. Económico si usa Haiku.

```
PROMPT EVALUADOR:
"Dado este input y este output de IA, responde con JSON:
  - coherente (bool): ¿el output responde lo que pregunta el input?
  - completo (bool): ¿están todos los elementos solicitados?
  - inventado (bool): ¿hay información que no estaba en el input?

INPUT: {input}
OUTPUT: {output}"
```

### Nivel 3 — Muestreo humano (semanal, 2-5% del volumen)
Un revisor humano evalúa una muestra aleatoria usando una rúbrica estandarizada. Este nivel detecta problemas que el nivel 2 no ve (calidad del razonamiento, subtleties de tono, errores de dominio).

### Nivel 4 — Feedback en producción (continuo)
Captura señales de calidad del usuario final: ¿editó el output? ¿lo rechazó? ¿lo usó directamente? Estas señales son el ground truth más valioso.

---

## 3.3.3 Rúbrica de Evaluación por Tipo de Output

### Para clasificación y extracción

| Criterio | Peso | Cómo medir |
|---|---|---|
| Formato correcto | 30% | Automático — parse JSON |
| Categoría correcta | 40% | Muestra humana vs ground truth |
| Campos completos | 20% | Automático — null check |
| Confianza calibrada | 10% | Calibration curve si el modelo da score |

### Para redacción corporativa

| Criterio | Peso | Cómo medir |
|---|---|---|
| Estructura correcta | 25% | Automático — regex sobre secciones |
| Datos factuales correctos | 30% | Humano — verificación spot check |
| Tono adecuado | 25% | Evaluador IA + muestra humana |
| Longitud dentro del rango | 10% | Automático — word count |
| Sin palabras prohibidas | 10% | Automático — lista negra |

### Para análisis y razonamiento

| Criterio | Peso | Cómo medir |
|---|---|---|
| Conclusión soportada por los datos | 35% | Humano |
| Identifica correctamente las limitaciones | 20% | Humano |
| Recomendación accionable | 25% | Rúbrica estructurada |
| No inventa datos externos | 20% | Evaluador IA |

---

## 3.3.4 El Pipeline de QA en Producción

```
Flujo de producción con QA integrado:

Input
  │
  ▼
[GENERACIÓN — Modelo principal]
  │
  ▼
[NIVEL 1 — Validación de formato] ──→ FALLO: reintento automático (max 2)
  │                                           │
  │ OK                                        → LOG + alerta si > 3 fallos/hora
  ▼
[NIVEL 2 — Evaluador IA] ──→ FALLO: cola de revisión humana
  │
  │ OK
  ▼
[OUTPUT → Sistema siguiente]
  │
  ▼
[NIVEL 4 — Feedback captura] → Dashboard de métricas
```

### Implementación del reintento automático

```python
def generar_con_retry(prompt: str, validador, max_intentos: int = 3) -> dict:
    for intento in range(max_intentos):
        resultado = llamar_api(prompt)
        if validador(resultado["output"]):
            resultado["intentos"] = intento + 1
            return resultado
        # Si falla, añade instrucción correctiva al prompt
        prompt += f"\n\nINTENTO {intento+1} FALLIDO: el output anterior no cumplía el formato.\nAsegúrate de devolver JSON válido con los campos requeridos."
    return {"output": None, "error": "Max reintentos alcanzado", "intentos": max_intentos}
```

---

## 3.3.5 Dashboard de Métricas de Calidad

Las métricas mínimas a monitorizar en producción:

```
MÉTRICAS DIARIAS (automatizables):
  · Tasa de formato correcto       (objetivo: > 98%)
  · Tasa de reintento              (objetivo: < 3%)
  · Tasa de cola humana            (objetivo: < 5%)
  · Latencia media                 (alerta si > 2x la baseline)
  · Coste por output               (alerta si > 1.5x la baseline)

MÉTRICAS SEMANALES (requieren revisión):
  · Tasa de aprobación directa     (objetivo: > 70%)
  · Tasa de alucinación en muestra (objetivo: < 1%)
  · NPS del usuario interno        (objetivo: > 7/10)

MÉTRICAS MENSUALES (estratégicas):
  · Deriva de calidad (¿está empeorando el modelo?)
  · Cobertura de casos límite en test suite
  · ROI ajustado por calidad
```

> Un pipeline de IA sin métricas de calidad es un sistema que se degrada en silencio. Implementa el dashboard en el momento del lanzamiento, no después.

---

---

## Fuentes y Referencias

**Papers y estudios:**
- Es et al. (2023) — *RAGAS: Automated Evaluation of Retrieval Augmented Generation* — framework de evaluación de sistemas RAG con métricas de faithfulness y relevancia (disponible en arxiv.org, buscar "RAGAS evaluation")
- Wang et al. (2022) — *Self-Consistency Improves Chain of Thought Reasoning in Language Models* → [arxiv.org/abs/2203.11171](https://arxiv.org/abs/2203.11171)

**Informes de industria:**
- McKinsey (anual) — *The State of AI* → [mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) *(métricas de calidad y tasas de error aceptables en despliegues IA empresariales)*
- Gartner — *Hype Cycle for Artificial Intelligence* → [gartner.com](https://www.gartner.com) *(estándares de madurez para evaluación y QA de sistemas IA en producción)*

**Libros recomendados:**
- Iansiti & Lakhani (2020) — *Competing in the Age of AI* (HBR Press) — cómo las empresas líderes estructuran la supervisión de calidad en sistemas de decisión automatizados

**Documentación oficial:**
- *Anthropic Documentation* → [docs.anthropic.com](https://docs.anthropic.com) *(patrones recomendados para evaluación de outputs y configuración de validadores con Claude)*

*Anterior: [3.2 Identidad Comunicativa y Tono](../3.2_identidad_comunicativa/README.md) | Siguiente: [4.1 Fundamentos de RAG](../../modulo_4/4.1_fundamentos_rag/README.md)*
