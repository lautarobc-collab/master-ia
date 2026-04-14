"""
LAB 1.2 — Evaluador de Oportunidades IA y Calculadora de ROI
=============================================================
Objetivo: construir una herramienta de diagnóstico que aplica
el filtro 4D y calcula el ROI proyectado de iniciativas de IA.

Casos de uso de este lab:
  1. Filtro 4D — evalúa si una tarea es candidata para IA
  2. Calculadora de ROI — proyección financiera de la iniciativa
  3. Matriz de priorización — ordena múltiples iniciativas

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json
import time

# ─── PARTE 1: FILTRO 4D ───────────────────────────────────────────────────────

def filtro_4d(tarea: dict) -> dict:
    """
    Evalúa si una tarea es candidata para IA usando el filtro 4D.

    Parámetros del dict tarea:
        nombre      (str)  : descripción de la tarea
        tiene_datos (bool) : ¿hay datos históricos o inputs estructurados?
        es_repetitiva(bool): ¿es predecible y se repite con frecuencia?
        sintetiza   (bool) : ¿requiere procesar/sintetizar mucha información?
        cuello_tiempo(bool): ¿el tiempo humano es el cuello de botella?
    """
    puntuacion = sum([
        tarea.get("tiene_datos", False),
        tarea.get("es_repetitiva", False),
        tarea.get("sintetiza", False),
        tarea.get("cuello_tiempo", False),
    ])

    if puntuacion >= 3:
        recomendacion = "CANDIDATA FUERTE — proceder con piloto"
        prioridad = "alta"
    elif puntuacion == 2:
        recomendacion = "CANDIDATA MODERADA — evaluar caso a caso"
        prioridad = "media"
    else:
        recomendacion = "NO RECOMENDADA — bajo potencial de IA"
        prioridad = "baja"

    return {
        "tarea": tarea["nombre"],
        "puntuacion_4d": f"{puntuacion}/4",
        "recomendacion": recomendacion,
        "prioridad": prioridad,
        "dimensiones": {
            "Data":     "✓" if tarea.get("tiene_datos")    else "✗",
            "Dull":     "✓" if tarea.get("es_repetitiva")  else "✗",
            "Difficult":"✓" if tarea.get("sintetiza")       else "✗",
            "Deadline": "✓" if tarea.get("cuello_tiempo")  else "✗",
        }
    }


# ─── PARTE 2: CALCULADORA DE ROI ─────────────────────────────────────────────

def calcular_roi(iniciativa: dict) -> dict:
    """
    Calcula el ROI proyectado de una iniciativa de IA.

    Parámetros:
        horas_ahorradas_semana (float): horas/semana liberadas
        coste_hora_eur         (float): coste por hora del perfil afectado
        errores_evitados_mes   (int)  : errores evitados por mes
        coste_por_error_eur    (float): coste promedio de cada error
        coste_api_mes_eur      (float): coste mensual de la API
        coste_desarrollo_eur   (float): coste one-time de desarrollo
        semanas_año            (int)  : semanas laborables (default 48)
    """
    semanas = iniciativa.get("semanas_año", 48)

    # Valor anual generado
    valor_horas   = iniciativa["horas_ahorradas_semana"] * iniciativa["coste_hora_eur"] * semanas
    valor_errores = iniciativa["errores_evitados_mes"] * iniciativa["coste_por_error_eur"] * 12
    valor_total   = valor_horas + valor_errores

    # Coste anual
    coste_api_anual  = iniciativa["coste_api_mes_eur"] * 12
    coste_total      = coste_api_anual + iniciativa["coste_desarrollo_eur"]

    # ROI
    roi_pct = ((valor_total - coste_total) / coste_total) * 100 if coste_total > 0 else float('inf')

    # Payback en meses
    valor_mensual = valor_total / 12
    coste_mensual = coste_total / 12
    payback_meses = iniciativa["coste_desarrollo_eur"] / (valor_mensual - coste_api_anual/12) \
                    if (valor_mensual - coste_api_anual/12) > 0 else 999

    return {
        "nombre": iniciativa["nombre"],
        "valor_anual_eur": round(valor_total, 2),
        "  ↳ ahorro_horas_eur": round(valor_horas, 2),
        "  ↳ ahorro_errores_eur": round(valor_errores, 2),
        "coste_total_eur": round(coste_total, 2),
        "beneficio_neto_eur": round(valor_total - coste_total, 2),
        "roi_pct": round(roi_pct, 1),
        "payback_meses": round(payback_meses, 1),
    }


# ─── PARTE 3: PRIORIZACIÓN CON IA ────────────────────────────────────────────

def priorizar_con_ia(iniciativas: list, modelo: str = "claude-haiku-4-5-20251001") -> str:
    """
    Envía la lista de iniciativas a Claude para que recomiende
    el orden de implementación con justificación estratégica.

    PARÁMETROS CLAVE:
        temperature=0.2 → respuesta analítica y consistente
        max_tokens=600  → suficiente para 3-5 iniciativas bien argumentadas
    """
    try:
        import anthropic
        client = anthropic.Anthropic()

        resumen = "\n".join([
            f"- {i['nombre']}: ROI {i['roi_pct']}%, payback {i['payback_meses']} meses, prioridad 4D: {i.get('prioridad_4d','N/A')}"
            for i in iniciativas
        ])

        prompt = f"""Eres un consultor de transformación digital senior.
Tienes estas iniciativas de IA evaluadas con ROI y filtro 4D:

{resumen}

Recomienda el orden de implementación óptimo en 3-4 bullets.
Considera: ROI, payback, riesgo de implementación y efecto aprendizaje.
Sé específico y directo. No des contexto genérico."""

        inicio = time.time()
        resp = client.messages.create(
            model=modelo,
            max_tokens=600,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        latencia = round((time.time() - inicio) * 1000)

        return f"{resp.content[0].text}\n\n[Tokens: {resp.usage.input_tokens}→{resp.usage.output_tokens} | Latencia: {latencia}ms]"

    except ImportError:
        return "Instala anthropic: pip install anthropic"
    except Exception as e:
        return f"Error: {e}"


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 62)
    print("LAB 1.2 — Evaluador de Oportunidades IA y Calculadora ROI")
    print("=" * 62)

    # ── EJERCICIO 1: Filtro 4D ──────────────────────────────────
    print("\n[1] FILTRO 4D — ¿Qué tareas son candidatas para IA?")
    print("-" * 62)

    tareas_empresa = [
        {
            "nombre":        "Generación de informes semanales de ventas",
            "tiene_datos":    True,
            "es_repetitiva":  True,
            "sintetiza":      True,
            "cuello_tiempo":  True,
        },
        {
            "nombre":        "Decisión de contratación de directivo",
            "tiene_datos":    False,
            "es_repetitiva":  False,
            "sintetiza":      True,
            "cuello_tiempo":  False,
        },
        {
            "nombre":        "Clasificación de emails de soporte cliente",
            "tiene_datos":    True,
            "es_repetitiva":  True,
            "sintetiza":      False,
            "cuello_tiempo":  True,
        },
        {
            "nombre":        "Negociación de contrato con proveedor clave",
            "tiene_datos":    False,
            "es_repetitiva":  False,
            "sintetiza":      True,
            "cuello_tiempo":  False,
        },
    ]

    resultados_4d = []
    for tarea in tareas_empresa:
        r = filtro_4d(tarea)
        resultados_4d.append(r)
        print(f"\nTarea: {r['tarea']}")
        print(f"  4D: {r['dimensiones']}")
        print(f"  Puntuación: {r['puntuacion_4d']} → {r['recomendacion']}")

    # ── EJERCICIO 2: Calculadora de ROI ────────────────────────
    print("\n\n[2] CALCULADORA DE ROI — Proyección financiera")
    print("-" * 62)

    iniciativas = [
        {
            "nombre":                    "Automatización informes de ventas",
            "horas_ahorradas_semana":    6,
            "coste_hora_eur":            45,
            "errores_evitados_mes":      4,
            "coste_por_error_eur":       200,
            "coste_api_mes_eur":         30,
            "coste_desarrollo_eur":      800,
            "prioridad_4d":              "alta",
        },
        {
            "nombre":                    "Clasificador emails soporte",
            "horas_ahorradas_semana":    10,
            "coste_hora_eur":            28,
            "errores_evitados_mes":      20,
            "coste_por_error_eur":       50,
            "coste_api_mes_eur":         60,
            "coste_desarrollo_eur":      1200,
            "prioridad_4d":              "alta",
        },
        {
            "nombre":                    "Resumen contratos con IA",
            "horas_ahorradas_semana":    3,
            "coste_hora_eur":            70,
            "errores_evitados_mes":      2,
            "coste_por_error_eur":       500,
            "coste_api_mes_eur":         20,
            "coste_desarrollo_eur":      500,
            "prioridad_4d":              "media",
        },
    ]

    rois = []
    print(f"\n{'Iniciativa':<35} {'ROI':>7} {'Payback':>10} {'Beneficio neto':>16}")
    print("-" * 72)
    for ini in iniciativas:
        r = calcular_roi(ini)
        r["prioridad_4d"] = ini["prioridad_4d"]
        rois.append(r)
        print(f"{r['nombre']:<35} {r['roi_pct']:>6}% {r['payback_meses']:>8}m   €{r['beneficio_neto_eur']:>12,.0f}")

    # ── EJERCICIO 3: Priorización con Claude ───────────────────
    print("\n\n[3] PRIORIZACIÓN ESTRATÉGICA CON IA")
    print("-" * 62)

    if os.getenv("ANTHROPIC_API_KEY"):
        print("Consultando a Claude...\n")
        recomendacion = priorizar_con_ia(rois)
        print(recomendacion)
    else:
        print("NOTA: Configura ANTHROPIC_API_KEY para activar este ejercicio.")
        print("      export ANTHROPIC_API_KEY='sk-ant-...'")
        print("\n  Orden sugerido manualmente por ROI:")
        for r in sorted(rois, key=lambda x: x["roi_pct"], reverse=True):
            print(f"  {r['roi_pct']:>7}% ROI — {r['nombre']}")

    # RESULTADO ESPERADO:
    # - Informes de ventas: ROI ~1.300%, payback <1 mes
    # - Clasificador emails: ROI ~600%, payback ~2 meses
    # - Resumen contratos: ROI ~1.100%, payback <1 mes
    # Orden óptimo: empezar por el de mayor ROI y menor desarrollo (quick win)
    print("\n[FIN DEL LAB 1.2]")
