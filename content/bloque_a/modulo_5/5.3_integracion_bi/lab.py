"""
LAB 5.3 — Integración con Business Intelligence
================================================
Objetivo: construir el pipeline de reporting automático —
desde la extracción de datos hasta el envío del informe
con narrativa generada por IA.

Ejercicios:
  1. Extractor y normalizador de KPIs desde datos brutos
  2. Generador de alertas inteligentes
  3. Pipeline completo de informe semanal automatizado

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json
import time
from datetime import datetime, timedelta

MODELO = "claude-sonnet-4-6"


def llamar_api(prompt, system="", temperatura=0.3, max_tokens=600):
    try:
        import anthropic
        client = anthropic.Anthropic()
        kwargs = dict(model=MODELO, max_tokens=max_tokens, temperature=temperatura,
                      messages=[{"role":"user","content":prompt}])
        if system:
            kwargs["system"] = system
        r = client.messages.create(**kwargs)
        return r.content[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


# ─── DATOS SIMULADOS ──────────────────────────────────────────────────────────

KPIS_ESTA_SEMANA = {
    "ventas_eur":         142300,
    "pedidos":            923,
    "ticket_medio":       154.2,
    "nuevos_clientes":    47,
    "tasa_conversion_pct": 3.1,
    "reclamaciones":      18,
    "nps":                44,
    "tiempo_entrega_dias": 3.8,
}

KPIS_SEMANA_ANTERIOR = {
    "ventas_eur":         156800,
    "pedidos":            1012,
    "ticket_medio":       154.9,
    "nuevos_clientes":    52,
    "tasa_conversion_pct": 3.4,
    "reclamaciones":      31,
    "nps":                38,
    "tiempo_entrega_dias": 4.2,
}

OBJETIVOS = {
    "ventas_eur":         150000,
    "pedidos":            950,
    "nuevos_clientes":    50,
    "reclamaciones":      20,
    "nps":                40,
}


# ─── PARTE 1: PROCESADOR DE KPIS ─────────────────────────────────────────────

def calcular_variaciones(actual: dict, anterior: dict, objetivos: dict) -> list:
    resultado = []
    for kpi, valor_actual in actual.items():
        valor_anterior = anterior.get(kpi, valor_actual)
        objetivo       = objetivos.get(kpi)
        variacion_pct  = ((valor_actual - valor_anterior) / valor_anterior * 100) if valor_anterior else 0
        vs_objetivo    = ((valor_actual - objetivo) / objetivo * 100) if objetivo else None
        # Determinar si la variación es positiva (depende del KPI)
        invertido = kpi in ("reclamaciones", "tiempo_entrega_dias")
        positivo  = variacion_pct < 0 if invertido else variacion_pct > 0
        resultado.append({
            "kpi":           kpi,
            "valor":         valor_actual,
            "variacion_pct": round(variacion_pct, 1),
            "vs_objetivo_pct": round(vs_objetivo, 1) if vs_objetivo is not None else None,
            "tendencia":     "↑" if positivo else "↓",
            "semaforo":      "🟢" if (abs(variacion_pct) < 5 or positivo) else "🔴" if abs(variacion_pct) > 15 else "🟡",
        })
    return resultado


# ─── PARTE 2: GENERADOR DE ALERTAS ───────────────────────────────────────────

def detectar_alertas(variaciones: list, umbral_pct: float = 10.0) -> list:
    alertas = []
    for v in variaciones:
        if abs(v["variacion_pct"]) >= umbral_pct:
            alertas.append({
                "kpi":       v["kpi"],
                "cambio":    f"{v['variacion_pct']:+.1f}%",
                "valor":     v["valor"],
                "semaforo":  v["semaforo"],
            })
    return sorted(alertas, key=lambda x: abs(float(x["cambio"].replace("%",""))), reverse=True)


PROMPT_ALERTAS = """Analiza estas variaciones de KPIs de negocio y genera un resumen de alertas para el equipo directivo.
Para cada alerta, explica brevemente el posible impacto y la acción recomendada.
Máximo 3 alertas. Tono directo y ejecutivo.
Responde en texto plano, sin markdown.

KPIs con variación significativa (vs semana anterior):
{alertas}

Contexto: empresa de distribución, semana del {fecha}."""


# ─── PARTE 3: PIPELINE COMPLETO ───────────────────────────────────────────────

PROMPT_INFORME = """Genera el resumen ejecutivo semanal de ventas para el Comité de Dirección.
Máximo 150 palabras. Conclusión primero. Menciona solo los 3 KPIs más relevantes.
Incluye: qué fue bien, qué preocupa, y una recomendación concreta.

KPIs de la semana (con variación vs semana anterior y vs objetivo):
{kpis}

Alertas identificadas:
{alertas}"""


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 5.3 — Integración con Business Intelligence")
    print("=" * 64)

    tiene_api = bool(os.getenv("ANTHROPIC_API_KEY"))
    fecha_semana = (datetime.now() - timedelta(days=7)).strftime("%d/%m/%Y")

    print("\n[1] PROCESADOR DE KPIS")
    print("-" * 64)
    variaciones = calcular_variaciones(KPIS_ESTA_SEMANA, KPIS_SEMANA_ANTERIOR, OBJETIVOS)
    print(f"\n  {'KPI':<28} {'Valor':>10} {'Var%':>7} {'Vs Obj%':>8} {'':>3}")
    print("  " + "-" * 58)
    for v in variaciones:
        obj_str = f"{v['vs_objetivo_pct']:+.1f}%" if v['vs_objetivo_pct'] is not None else "  —  "
        print(f"  {v['kpi']:<28} {v['valor']:>10,.1f} {v['variacion_pct']:>+6.1f}% {obj_str:>8} {v['semaforo']}")

    print("\n\n[2] ALERTAS INTELIGENTES")
    print("-" * 64)
    alertas = detectar_alertas(variaciones, umbral_pct=10.0)
    print(f"\n  Alertas detectadas (variación > 10%): {len(alertas)}")
    for a in alertas:
        print(f"  {a['semaforo']} {a['kpi']}: {a['cambio']} (valor: {a['valor']:,.1f})")

    if tiene_api and alertas:
        alertas_str = json.dumps(alertas, ensure_ascii=False, indent=2)
        comentario = llamar_api(
            PROMPT_ALERTAS.format(alertas=alertas_str, fecha=fecha_semana),
            temperatura=0.3, max_tokens=300
        )
        print(f"\n  Análisis IA:\n{comentario}")

    print("\n\n[3] PIPELINE: INFORME SEMANAL COMPLETO")
    print("-" * 64)
    if tiene_api:
        kpis_str    = json.dumps(variaciones, ensure_ascii=False, indent=2)
        alertas_str = json.dumps(alertas[:3], ensure_ascii=False, indent=2)
        informe = llamar_api(
            PROMPT_INFORME.format(kpis=kpis_str, alertas=alertas_str),
            temperatura=0.3, max_tokens=400
        )
        print(f"\n{'═'*60}")
        print(f"RESUMEN EJECUTIVO — Semana del {fecha_semana}")
        print('═'*60)
        print(informe)
        print('═'*60)
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY para generar el informe completo.")

    print("\n[FIN DEL LAB 5.3]")
