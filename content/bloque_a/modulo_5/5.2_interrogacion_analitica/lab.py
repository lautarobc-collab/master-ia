"""
LAB 5.2 — Interrogación Analítica con IA
==========================================
Objetivo: construir pipelines de análisis de datos usando IA —
Text-to-SQL, análisis de texto libre y narrativa ejecutiva.

Ejercicios:
  1. Text-to-SQL — consultas en lenguaje natural sobre un schema
  2. Análisis de reseñas — sentimiento, temas y priorización
  3. Narrativa ejecutiva — convierte datos en párrafos para dirección

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json
import time

MODELO = "claude-haiku-4-5-20251001"


def llamar_api(prompt, system="", temperatura=0.1, max_tokens=500):
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


# ─── PARTE 1: TEXT-TO-SQL ────────────────────────────────────────────────────

SCHEMA = """
Tablas disponibles:
  pedidos (id INT, cliente_id INT, fecha DATE, importe_eur FLOAT, estado VARCHAR, producto_id INT)
  clientes (id INT, nombre VARCHAR, sector VARCHAR, ciudad VARCHAR, fecha_alta DATE)
  productos (id INT, nombre VARCHAR, categoria VARCHAR, precio_base FLOAT)
"""

SYSTEM_SQL = """Eres un experto en SQL. Generas SOLO código SQL válido para MySQL.
Sin explicaciones. Sin markdown. Solo la consulta SQL."""

PREGUNTAS_SQL = [
    "¿Cuál es el total de ventas por sector en el último trimestre?",
    "Dame los 5 clientes con mayor volumen de compra este año",
    "¿Cuántos pedidos pendientes hay por ciudad?",
    "¿Cuál es el producto más vendido en cada categoría?",
]


# ─── PARTE 2: ANÁLISIS DE TEXTO ───────────────────────────────────────────────

RESEÑAS = [
    "Excelente servicio, el producto llegó antes de lo esperado. Muy recomendable.",
    "El producto es bueno pero el envío tardó 2 semanas. La atención al cliente no resolvió mi consulta.",
    "PÉSIMO. Llevo 3 semanas esperando y nadie me da respuesta. Quiero el reembolso.",
    "Relación calidad-precio muy buena. El embalaje podría mejorar pero el producto funciona perfectamente.",
    "Segunda vez que compro y siempre satisfecho. Proceso de devolución muy sencillo.",
    "El producto no coincidía con la descripción. Tuve que devolverlo.",
]

PROMPT_ANALISIS_RESENAS = """Analiza estas reseñas de clientes y devuelve JSON con:
{{
  "sentimiento_general": "positivo/neutro/negativo",
  "puntuacion_media": número del 1 al 10,
  "temas_positivos": ["lista"],
  "temas_negativos": ["lista"],
  "urgente": ["reseñas que requieren acción inmediata"],
  "recomendacion": "1 acción prioritaria para el equipo de operaciones"
}}

RESEÑAS:
{resenas}"""


# ─── PARTE 3: NARRATIVA EJECUTIVA ────────────────────────────────────────────

KPIS_ABRIL = {
    "ventas_totales_eur": 287400,
    "vs_mes_anterior_pct": -8.3,
    "vs_mismo_mes_año_anterior_pct": 12.1,
    "pedidos_totales": 1847,
    "ticket_medio_eur": 155.6,
    "tasa_conversion_web_pct": 3.2,
    "nps_clientes": 42,
    "reclamaciones": 23,
    "reclamaciones_vs_anterior": -34,
}

PROMPT_NARRATIVA = """Eres el director financiero preparando el informe mensual para el Comité de Dirección.
Convierte estos KPIs en un párrafo ejecutivo de exactamente 100-120 palabras.
Destaca los 3 datos más importantes para la toma de decisiones.
No incluyas todos los números — selecciona los que cuenten la historia más relevante.
Tono: directo, ejecutivo. Termina con una implicación o recomendación.

KPIs de abril 2025:
{kpis}"""


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 5.2 — Interrogación Analítica con IA")
    print("=" * 64)

    tiene_api = bool(os.getenv("ANTHROPIC_API_KEY"))

    print("\n[1] TEXT-TO-SQL")
    print("-" * 64)
    if tiene_api:
        for pregunta in PREGUNTAS_SQL:
            prompt = f"Schema de base de datos:\n{SCHEMA}\n\nPregunta: {pregunta}"
            sql = llamar_api(prompt, system=SYSTEM_SQL, temperatura=0.0, max_tokens=200)
            print(f"\n  Q: {pregunta}")
            print(f"  SQL: {sql}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY.")
        print("  Ejemplo esperado para 'ventas por sector':")
        print("  SELECT c.sector, SUM(p.importe_eur) FROM pedidos p JOIN clientes c ON...")

    print("\n\n[2] ANÁLISIS DE RESEÑAS")
    print("-" * 64)
    if tiene_api:
        resenas_str = "\n".join([f"{i+1}. {r}" for i, r in enumerate(RESEÑAS)])
        prompt = PROMPT_ANALISIS_RESENAS.format(resenas=resenas_str)
        resultado = llamar_api(prompt, temperatura=0.2, max_tokens=400)
        print(f"\n{resultado}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY.")

    print("\n\n[3] NARRATIVA EJECUTIVA")
    print("-" * 64)
    if tiene_api:
        kpis_str = json.dumps(KPIS_ABRIL, ensure_ascii=False, indent=2)
        prompt = PROMPT_NARRATIVA.format(kpis=kpis_str)
        narrativa = llamar_api(prompt, temperatura=0.4, max_tokens=300)
        print(f"\n{narrativa}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY.")
        print("  Los KPIs de abril muestran caída mensual (-8.3%) con crecimiento anual (+12.1%).")

    print("\n[FIN DEL LAB 5.2]")
