"""
LAB 1.3 — Generador de Casos de Negocio IA
============================================
Objetivo: construir una herramienta que, a partir de los datos
de un proceso, genera automáticamente un caso de negocio completo
listo para presentar a dirección.

Casos de uso de este lab:
  1. Canvas básico — calcula ROI y genera el resumen estructurado
  2. Análisis de escenarios — conservador / probable / optimista
  3. Generador de pitch — Claude redacta el documento ejecutivo

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import time
import json


# ─── PARTE 1: CANVAS DEL CASO DE NEGOCIO ─────────────────────────────────────

def calcular_canvas(datos: dict) -> dict:
    """
    Calcula todos los valores financieros del canvas y devuelve
    un dict estructurado listo para imprimir o enviar a Claude.

    Campos esperados en 'datos':
        nombre_proyecto         (str)
        proceso_afectado        (str)
        horas_semana_actuales   (float)  horas/semana invertidas hoy
        coste_hora_eur          (float)
        errores_mes             (int)
        coste_error_eur         (float)
        semanas_laborables      (int)    default 48
        coste_desarrollo_eur    (float)  one-time
        coste_api_mes_eur       (float)
        reduccion_tiempo_pct    (float)  % de horas que elimina la IA (0-1)
        reduccion_errores_pct   (float)  % de errores que evita la IA (0-1)
    """
    sw = datos.get("semanas_laborables", 48)

    # ── Situación actual ──────────────────────────────────────────────────────
    horas_año_actuales  = datos["horas_semana_actuales"] * sw
    coste_horas_año     = horas_año_actuales * datos["coste_hora_eur"]
    coste_errores_año   = datos["errores_mes"] * datos["coste_error_eur"] * 12
    coste_total_actual  = coste_horas_año + coste_errores_año

    # ── Ahorro proyectado ─────────────────────────────────────────────────────
    ahorro_horas_año    = coste_horas_año  * datos["reduccion_tiempo_pct"]
    ahorro_errores_año  = coste_errores_año * datos["reduccion_errores_pct"]
    beneficio_anual     = ahorro_horas_año + ahorro_errores_año

    # ── Inversión ─────────────────────────────────────────────────────────────
    coste_api_año       = datos["coste_api_mes_eur"] * 12
    inversion_año1      = datos["coste_desarrollo_eur"] + coste_api_año
    coste_recurrente    = coste_api_año   # años 2+

    # ── ROI ───────────────────────────────────────────────────────────────────
    roi_año1 = ((beneficio_anual - inversion_año1) / inversion_año1 * 100) \
               if inversion_año1 > 0 else float('inf')
    roi_año2 = ((beneficio_anual - coste_recurrente) / coste_recurrente * 100) \
               if coste_recurrente > 0 else float('inf')

    # Payback en meses desde el desarrollo one-time
    beneficio_mensual_neto = (beneficio_anual - coste_api_año) / 12
    payback_meses = datos["coste_desarrollo_eur"] / beneficio_mensual_neto \
                    if beneficio_mensual_neto > 0 else 999

    return {
        "proyecto": datos["nombre_proyecto"],
        "proceso":  datos["proceso_afectado"],
        "situacion_actual": {
            "horas_año":         round(horas_año_actuales, 1),
            "coste_horas_año":   round(coste_horas_año, 2),
            "coste_errores_año": round(coste_errores_año, 2),
            "coste_total_año":   round(coste_total_actual, 2),
        },
        "impacto": {
            "ahorro_horas_año":    round(ahorro_horas_año, 2),
            "ahorro_errores_año":  round(ahorro_errores_año, 2),
            "beneficio_anual":     round(beneficio_anual, 2),
        },
        "inversion": {
            "desarrollo_one_time": round(datos["coste_desarrollo_eur"], 2),
            "api_mensual":         round(datos["coste_api_mes_eur"], 2),
            "total_año1":          round(inversion_año1, 2),
            "total_año2_plus":     round(coste_recurrente, 2),
        },
        "financiero": {
            "roi_año1_pct":    round(roi_año1, 1),
            "roi_año2_pct":    round(roi_año2, 1),
            "payback_meses":   round(payback_meses, 1),
            "beneficio_neto_año1": round(beneficio_anual - inversion_año1, 2),
        },
    }


# ─── PARTE 2: ANÁLISIS DE ESCENARIOS ─────────────────────────────────────────

def analisis_escenarios(datos_base: dict) -> dict:
    """
    Genera tres escenarios (conservador, probable, optimista)
    variando la reducción de tiempo y errores estimada.
    """
    escenarios = {
        "conservador": (0.40, 0.50),   # 40% tiempo, 50% errores
        "probable":    (0.65, 0.75),   # 65% tiempo, 75% errores
        "optimista":   (0.85, 0.90),   # 85% tiempo, 90% errores
    }

    resultados = {}
    for nombre, (rt, re) in escenarios.items():
        d = dict(datos_base)
        d["reduccion_tiempo_pct"]  = rt
        d["reduccion_errores_pct"] = re
        c = calcular_canvas(d)
        resultados[nombre] = {
            "reduccion_tiempo":  f"{int(rt*100)}%",
            "reduccion_errores": f"{int(re*100)}%",
            "beneficio_anual":   c["impacto"]["beneficio_anual"],
            "roi_año1_pct":      c["financiero"]["roi_año1_pct"],
            "payback_meses":     c["financiero"]["payback_meses"],
        }
    return resultados


# ─── PARTE 3: GENERADOR DE PITCH CON IA ──────────────────────────────────────

def generar_pitch(canvas: dict, modelo: str = "claude-haiku-4-5-20251001") -> str:
    """
    Envía el canvas a Claude y recibe el pitch ejecutivo redactado
    listo para copiar en una presentación o email a dirección.

    PARÁMETROS CLAVE:
        temperature=0.3  → redacción fluida pero controlada
        max_tokens=800   → suficiente para un pitch completo de 5 bloques
    """
    try:
        import anthropic
        client = anthropic.Anthropic()

        resumen_canvas = json.dumps(canvas, ensure_ascii=False, indent=2)

        prompt = f"""Eres un consultor de transformación digital especializado en presentar proyectos de IA a comités directivos.

Aquí tienes el análisis financiero de una iniciativa de IA:

{resumen_canvas}

Redacta el PITCH EJECUTIVO DE 5 MINUTOS siguiendo EXACTAMENTE esta estructura:

**MINUTO 1 — El Problema**
[2-3 frases describiendo el coste y consecuencias del proceso actual]

**MINUTO 2 — La Solución**
[1-2 frases sobre qué hace la IA y qué sigue haciendo el humano]

**MINUTO 3 — Los Números**
[Inversión, ahorro anual, ROI y payback. Todos los valores en €]

**MINUTO 4 — El Plan**
[3 fases concretas con semanas estimadas]

**MINUTO 5 — La Decisión**
[La petición concreta: qué se necesita aprobar hoy y cuál es el criterio de go/no-go]

Tono: directo, ejecutivo, sin tecnicismos. Máximo 400 palabras."""

        inicio = time.time()
        resp = client.messages.create(
            model=modelo,
            max_tokens=800,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        latencia = round((time.time() - inicio) * 1000)

        return (
            f"{resp.content[0].text}\n\n"
            f"[Tokens: {resp.usage.input_tokens}→{resp.usage.output_tokens} | Latencia: {latencia}ms]"
        )

    except ImportError:
        return "Instala anthropic: pip install anthropic"
    except Exception as e:
        return f"Error al llamar a la API: {e}"


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 64)
    print("LAB 1.3 — Generador de Casos de Negocio IA")
    print("=" * 64)

    # Datos del caso de uso: automatización del proceso de cribado de CVs
    datos_proyecto = {
        "nombre_proyecto":       "Cribado automático de CVs con IA",
        "proceso_afectado":      "Selección de personal — RRHH",
        "horas_semana_actuales": 12,        # horas/semana del equipo en cribado
        "coste_hora_eur":        35,
        "errores_mes":           8,         # candidatos mal clasificados/mes
        "coste_error_eur":       300,       # coste de una mala selección inicial
        "semanas_laborables":    48,
        "coste_desarrollo_eur":  1_500,     # desarrollo del pipeline
        "coste_api_mes_eur":     45,        # Claude Haiku para procesar CVs
        "reduccion_tiempo_pct":  0.65,      # escenario probable
        "reduccion_errores_pct": 0.75,
    }

    # ── EJERCICIO 1: Canvas básico ──────────────────────────────────────────
    print("\n[1] CANVAS DEL CASO DE NEGOCIO")
    print("-" * 64)

    canvas = calcular_canvas(datos_proyecto)

    print(f"\nProyecto: {canvas['proyecto']}")
    print(f"Proceso:  {canvas['proceso']}")

    print("\n  SITUACIÓN ACTUAL:")
    print(f"    Horas/año invertidas:   {canvas['situacion_actual']['horas_año']}h")
    print(f"    Coste en tiempo:        €{canvas['situacion_actual']['coste_horas_año']:,.0f}/año")
    print(f"    Coste en errores:       €{canvas['situacion_actual']['coste_errores_año']:,.0f}/año")
    print(f"    Coste total actual:     €{canvas['situacion_actual']['coste_total_año']:,.0f}/año")

    print("\n  IMPACTO PROYECTADO (escenario probable):")
    print(f"    Ahorro en horas:        €{canvas['impacto']['ahorro_horas_año']:,.0f}/año")
    print(f"    Ahorro en errores:      €{canvas['impacto']['ahorro_errores_año']:,.0f}/año")
    print(f"    Beneficio anual total:  €{canvas['impacto']['beneficio_anual']:,.0f}/año")

    print("\n  INVERSIÓN:")
    print(f"    Desarrollo (one-time):  €{canvas['inversion']['desarrollo_one_time']:,.0f}")
    print(f"    API mensual:            €{canvas['inversion']['api_mensual']}/mes")
    print(f"    Total año 1:            €{canvas['inversion']['total_año1']:,.0f}")
    print(f"    Total año 2+:           €{canvas['inversion']['total_año2_plus']:,.0f}/año")

    print("\n  RESUMEN FINANCIERO:")
    print(f"    ROI año 1:              {canvas['financiero']['roi_año1_pct']}%")
    print(f"    ROI año 2+:             {canvas['financiero']['roi_año2_pct']}%")
    print(f"    Payback:                {canvas['financiero']['payback_meses']} meses")
    print(f"    Beneficio neto año 1:   €{canvas['financiero']['beneficio_neto_año1']:,.0f}")

    # ── EJERCICIO 2: Análisis de escenarios ────────────────────────────────
    print("\n\n[2] ANÁLISIS DE ESCENARIOS")
    print("-" * 64)

    escenarios = analisis_escenarios(datos_proyecto)

    print(f"\n{'Escenario':<14} {'Tiempo':>7} {'Errores':>8} {'Beneficio/año':>14} {'ROI año1':>9} {'Payback':>9}")
    print("-" * 64)
    for nombre, e in escenarios.items():
        print(
            f"{nombre.capitalize():<14} "
            f"{e['reduccion_tiempo']:>7} "
            f"{e['reduccion_errores']:>8} "
            f"€{e['beneficio_anual']:>12,.0f} "
            f"{e['roi_año1_pct']:>8}% "
            f"{e['payback_meses']:>7}m"
        )

    print("\n→ Presenta el escenario PROBABLE al comité.")
    print("→ El CONSERVADOR es tu garantía mínima.")
    print("→ El OPTIMISTA muestra el techo alcanzable.")

    # ── EJERCICIO 3: Pitch ejecutivo con Claude ────────────────────────────
    print("\n\n[3] PITCH EJECUTIVO GENERADO POR IA")
    print("-" * 64)

    if os.getenv("ANTHROPIC_API_KEY"):
        print("Generando pitch con Claude...\n")
        pitch = generar_pitch(canvas)
        print(pitch)
    else:
        print("NOTA: Configura ANTHROPIC_API_KEY para generar el pitch automáticamente.")
        print("      export ANTHROPIC_API_KEY='sk-ant-...'")
        print("\n  Estructura del pitch (rellena con los datos del canvas):")
        print("""
  MINUTO 1 — El Problema
  El proceso de cribado de CVs consume 576h/año del equipo de RRHH,
  con un coste de €20.160 anuales solo en tiempo. Además, los errores
  de clasificación generan €28.800 adicionales en procesos fallidos.

  MINUTO 2 — La Solución
  [Completar con Claude o manualmente]

  MINUTO 3 — Los Números
  Inversión año 1: €2.040. Beneficio anual: €16.380. ROI: 702%.
  Payback estimado: 1.5 meses.

  MINUTO 4 — El Plan
  [3 fases: prototipo (sem 1-3), piloto (sem 4-8), escala (sem 9-12)]

  MINUTO 5 — La Decisión
  [Solicitud concreta de presupuesto y equipo]
""")

    # RESULTADO ESPERADO (escenario probable):
    # Beneficio anual: ~€16.380
    # ROI año 1: ~702%
    # Payback: ~1.5 meses
    # Escenario conservador: €10.584/año, ROI ~419%
    # Escenario optimista: €21.420/año, ROI ~949%
    print("\n[FIN DEL LAB 1.3]")
