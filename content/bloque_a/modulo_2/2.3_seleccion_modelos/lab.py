"""
LAB 2.3 — Selección Estratégica de Modelos
============================================
Objetivo: implementar un router de modelos, comparar calidad/coste
entre Haiku y Sonnet en tareas reales, y construir un benchmark
propio para validar decisiones de selección.

Ejercicios:
  1. Router automático — clasifica tareas y asigna modelo óptimo
  2. Benchmark calidad/coste — misma tarea en Haiku vs Sonnet
  3. Calculadora de arquitectura híbrida — ROI de optimizar el stack

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import time
import json

MODELO_RAPIDO   = "claude-haiku-4-5-20251001"
MODELO_ESTANDAR = "claude-sonnet-4-6"

# Precios por 1M tokens (input / output) en USD
PRECIOS = {
    "claude-haiku-4-5-20251001": {"input": 0.80,  "output": 4.00},
    "claude-sonnet-4-6":         {"input": 3.00,  "output": 15.00},
    "claude-opus-4-6":           {"input": 15.00, "output": 75.00},
}


# ─── UTILIDADES ───────────────────────────────────────────────────────────────

def llamar_modelo(prompt: str, modelo: str, temperatura: float = 0.1,
                  max_tokens: int = 300) -> dict:
    try:
        import anthropic
        client = anthropic.Anthropic()
        inicio = time.time()
        resp = client.messages.create(
            model=modelo,
            max_tokens=max_tokens,
            temperature=temperatura,
            messages=[{"role": "user", "content": prompt}]
        )
        latencia = round((time.time() - inicio) * 1000)
        p = PRECIOS[modelo]
        coste = (resp.usage.input_tokens * p["input"] + resp.usage.output_tokens * p["output"]) / 1_000_000
        return {
            "modelo":      modelo.split("-")[1],   # "haiku" / "sonnet"
            "output":      resp.content[0].text.strip(),
            "tokens_in":   resp.usage.input_tokens,
            "tokens_out":  resp.usage.output_tokens,
            "latencia_ms": latencia,
            "coste_usd":   round(coste, 6),
        }
    except ImportError:
        return {"modelo": modelo, "output": "pip install anthropic", "tokens_in":0,"tokens_out":0,"latencia_ms":0,"coste_usd":0}
    except Exception as e:
        return {"modelo": modelo, "output": f"Error: {e}", "tokens_in":0,"tokens_out":0,"latencia_ms":0,"coste_usd":0}


# ─── PARTE 1: ROUTER DE MODELOS ───────────────────────────────────────────────

SEÑALES_COMPLEJIDAD_ALTA = [
    "estrategia", "legal", "contrato", "riesgo", "análisis financiero",
    "arquitectura", "decisión crítica", "due diligence", "normativa",
    "compliance", "litigio", "auditoría", "m&a", "fusión", "adquisición"
]

SEÑALES_COMPLEJIDAD_BAJA = [
    "clasifica", "categoriza", "resume en", "extrae", "traduce",
    "etiqueta", "sí o no", "verdadero o falso", "sentiment"
]

def router_modelo(descripcion_tarea: str) -> dict:
    """
    Clasifica la complejidad de una tarea y recomienda el modelo óptimo.
    Heurística basada en palabras clave + longitud de la tarea.
    """
    tarea_lower = descripcion_tarea.lower()

    puntos_alta  = sum(1 for s in SEÑALES_COMPLEJIDAD_ALTA if s in tarea_lower)
    puntos_baja  = sum(1 for s in SEÑALES_COMPLEJIDAD_BAJA if s in tarea_lower)
    longitud_pts = 1 if len(descripcion_tarea) > 200 else 0

    score = puntos_alta - puntos_baja + longitud_pts

    if score >= 2:
        modelo = MODELO_ESTANDAR
        razon  = "Alta complejidad detectada — razonamiento profundo requerido"
    elif score <= -1:
        modelo = MODELO_RAPIDO
        razon  = "Tarea simple/estructurada — Haiku es suficiente"
    else:
        modelo = MODELO_ESTANDAR
        razon  = "Complejidad media — Sonnet por defecto seguro"

    return {"modelo": modelo, "score": score, "razon": razon}


TAREAS_TEST = [
    "Clasifica este email como consulta, reclamación o pedido",
    "Analiza los riesgos legales y financieros de esta cláusula contractual para una due diligence",
    "Resume este ticket de soporte en 1 frase",
    "Desarrolla una estrategia de adopción de IA para una empresa industrial de 200 empleados con baja madurez digital",
    "Extrae el importe total de esta factura",
    "Evalúa si esta arquitectura de datos cumple con los requisitos de compliance del AI Act europeo",
]


# ─── PARTE 2: BENCHMARK CALIDAD/COSTE ────────────────────────────────────────

TAREAS_BENCHMARK = [
    {
        "nombre": "Clasificación email",
        "prompt": 'Clasifica en una palabra: consulta/reclamacion/pedido.\nEmail: "Necesito saber el estado de mi pedido #4521"\nResponde solo con la categoría.',
    },
    {
        "nombre": "Extracción de datos",
        "prompt": 'Extrae: {"empresa": null, "importe_eur": null, "fecha": null}\nTexto: "Factura de Suministros Ibéricos S.L. por 3.450€, emitida el 15 de marzo de 2025."\nResponde solo con el JSON.',
    },
    {
        "nombre": "Resumen ejecutivo",
        "prompt": "Resume en máximo 50 palabras para un directivo:\nEl proyecto de transformación digital ha alcanzado el 65% de sus objetivos en el primer semestre. Se han automatizado 3 procesos clave en el departamento de operaciones, reduciendo el tiempo de procesamiento en un 40%. Sin embargo, la adopción en RRHH está por debajo del objetivo (30% vs 60% previsto) debido a resistencia al cambio del equipo.",
    },
    {
        "nombre": "Análisis de riesgo",
        "prompt": "Identifica los 3 principales riesgos de negocio en este escenario y puntúa cada uno (alto/medio/bajo):\nEmpresa de logística con 80% de contratos concentrados en 2 clientes, sistema ERP con 8 años de antigüedad sin soporte, y equipo directivo sin experiencia en transformación digital.",
    },
]


# ─── PARTE 3: CALCULADORA DE ARQUITECTURA HÍBRIDA ────────────────────────────

def calcular_ahorro_hibrido(
    llamadas_mes: int,
    pct_tareas_simples: float,
    tokens_promedio_input: int,
    tokens_promedio_output: int
) -> dict:
    """
    Calcula el ahorro de usar arquitectura híbrida vs todo-Sonnet.

    pct_tareas_simples: fracción de llamadas que Haiku puede resolver (0-1)
    """
    tokens_in_mes  = llamadas_mes * tokens_promedio_input
    tokens_out_mes = llamadas_mes * tokens_promedio_output

    # Coste todo-Sonnet
    p_sonnet = PRECIOS["claude-sonnet-4-6"]
    coste_todo_sonnet = (tokens_in_mes * p_sonnet["input"] +
                         tokens_out_mes * p_sonnet["output"]) / 1_000_000

    # Coste híbrido
    llamadas_haiku  = int(llamadas_mes * pct_tareas_simples)
    llamadas_sonnet = llamadas_mes - llamadas_haiku

    p_haiku = PRECIOS["claude-haiku-4-5-20251001"]
    coste_haiku  = (llamadas_haiku * tokens_promedio_input  * p_haiku["input"] +
                    llamadas_haiku * tokens_promedio_output * p_haiku["output"]) / 1_000_000
    coste_sonnet = (llamadas_sonnet * tokens_promedio_input  * p_sonnet["input"] +
                    llamadas_sonnet * tokens_promedio_output * p_sonnet["output"]) / 1_000_000
    coste_hibrido = coste_haiku + coste_sonnet

    ahorro_mes = coste_todo_sonnet - coste_hibrido
    ahorro_año = ahorro_mes * 12
    pct_ahorro = (ahorro_mes / coste_todo_sonnet * 100) if coste_todo_sonnet > 0 else 0

    return {
        "llamadas_mes":        llamadas_mes,
        "coste_todo_sonnet":   round(coste_todo_sonnet, 2),
        "coste_hibrido":       round(coste_hibrido, 2),
        "ahorro_mensual_usd":  round(ahorro_mes, 2),
        "ahorro_anual_usd":    round(ahorro_año, 2),
        "pct_ahorro":          round(pct_ahorro, 1),
    }


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 64)
    print("LAB 2.3 — Selección Estratégica de Modelos")
    print("=" * 64)

    tiene_api = bool(os.getenv("ANTHROPIC_API_KEY"))

    # ── EJERCICIO 1: Router ──────────────────────────────────────────────────
    print("\n[1] ROUTER DE MODELOS")
    print("-" * 64)
    for tarea in TAREAS_TEST:
        r = router_modelo(tarea)
        modelo_corto = "Haiku" if "haiku" in r["modelo"] else "Sonnet"
        print(f"\n  Tarea: {tarea[:65]}{'...' if len(tarea)>65 else ''}")
        print(f"  → {modelo_corto} (score={r['score']:+d}) — {r['razon']}")

    # ── EJERCICIO 2: Benchmark ───────────────────────────────────────────────
    print("\n\n[2] BENCHMARK HAIKU vs SONNET")
    print("-" * 64)

    if tiene_api:
        print(f"\n{'Tarea':<25} {'Modelo':>8} {'Tokens':>8} {'Latencia':>10} {'Coste':>10}")
        print("-" * 64)
        for tarea in TAREAS_BENCHMARK:
            for modelo in [MODELO_RAPIDO, MODELO_ESTANDAR]:
                r = llamar_modelo(tarea["prompt"], modelo)
                nombre_m = "Haiku" if "haiku" in modelo else "Sonnet"
                print(f"  {tarea['nombre']:<23} {nombre_m:>8} "
                      f"{r['tokens_in']+r['tokens_out']:>7}t "
                      f"{r['latencia_ms']:>8}ms "
                      f"${r['coste_usd']:>8.5f}")
            print()
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY para ejecutar el benchmark.")
        print("  Resultado esperado: Haiku ~3-5x más rápido, ~5x más barato.")
        print("  Calidad: equivalente en clasificación/extracción, inferior en análisis complejo.")

    # ── EJERCICIO 3: Calculadora híbrida ────────────────────────────────────
    print("\n\n[3] CALCULADORA DE ARQUITECTURA HÍBRIDA")
    print("-" * 64)

    escenarios = [
        {"llamadas": 10_000,  "pct_simple": 0.60, "label": "Empresa pequeña (10K llamadas/mes)"},
        {"llamadas": 100_000, "pct_simple": 0.65, "label": "Empresa mediana (100K llamadas/mes)"},
        {"llamadas": 500_000, "pct_simple": 0.70, "label": "Empresa grande (500K llamadas/mes)"},
    ]

    print(f"\n{'Escenario':<38} {'Todo-Sonnet':>12} {'Híbrido':>10} {'Ahorro/año':>12} {'%':>6}")
    print("-" * 82)
    for e in escenarios:
        r = calcular_ahorro_hibrido(
            llamadas_mes=e["llamadas"],
            pct_tareas_simples=e["pct_simple"],
            tokens_promedio_input=500,
            tokens_promedio_output=150,
        )
        print(f"  {e['label']:<36} ${r['coste_todo_sonnet']:>10,.2f} "
              f"${r['coste_hibrido']:>8,.2f} "
              f"${r['ahorro_anual_usd']:>10,.0f} "
              f"{r['pct_ahorro']:>5}%")

    print("\n→ El 65-70% de las tareas corporativas son clasificación/extracción → Haiku.")
    print("→ El ahorro escala linealmente con el volumen.")
    print("→ Implementar el router tiene sentido a partir de ~50K llamadas/mes.")

    print("\n[FIN DEL LAB 2.3]")
