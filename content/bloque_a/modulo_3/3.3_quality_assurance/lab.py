"""
LAB 3.3 — Validación y Quality Assurance
==========================================
Objetivo: implementar un pipeline de QA de 4 niveles sobre
outputs reales de IA y construir el dashboard de métricas básico.

Ejercicios:
  1. Validador automático de formato (Nivel 1)
  2. Evaluador IA de coherencia (Nivel 2)
  3. Generador con retry automático
  4. Simulador de dashboard de métricas

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import re
import json
import time
import random

MODELO_PRINCIPAL = "claude-haiku-4-5-20251001"
MODELO_EVALUADOR = "claude-haiku-4-5-20251001"


def llamar_api(prompt, system="", temperatura=0.1, max_tokens=300):
    try:
        import anthropic
        client = anthropic.Anthropic()
        kwargs = dict(model=MODELO_PRINCIPAL, max_tokens=max_tokens, temperature=temperatura,
                      messages=[{"role": "user", "content": prompt}])
        if system:
            kwargs["system"] = system
        r = client.messages.create(**kwargs)
        return {"output": r.content[0].text.strip(), "ok": True}
    except Exception as e:
        return {"output": f"Error: {e}", "ok": False}


# ─── NIVEL 1: VALIDADORES DE FORMATO ─────────────────────────────────────────

def validar_json(output: str, campos: list) -> dict:
    try:
        data = json.loads(output)
        campos_presentes = {c: c in data for c in campos}
        return {
            "valido": all(campos_presentes.values()),
            "campos": campos_presentes,
            "error":  None,
        }
    except json.JSONDecodeError as e:
        return {"valido": False, "campos": {}, "error": f"JSON inválido: {e}"}


def validar_estructura_markdown(output: str, secciones: list) -> dict:
    encontradas = {s: bool(re.search(s, output, re.IGNORECASE)) for s in secciones}
    return {
        "valido": all(encontradas.values()),
        "secciones": encontradas,
    }


def validar_longitud(output: str, min_palabras: int, max_palabras: int) -> dict:
    palabras = len(output.split())
    return {
        "valido": min_palabras <= palabras <= max_palabras,
        "palabras": palabras,
        "rango": f"{min_palabras}-{max_palabras}",
    }


# ─── NIVEL 2: EVALUADOR IA ────────────────────────────────────────────────────

PROMPT_EVALUADOR = """Evalúa la calidad de este output de IA. Responde SOLO con JSON válido.

INPUT ORIGINAL: {input}
OUTPUT GENERADO: {output}

JSON de evaluación:
{{
  "coherente": true/false,
  "completo": true/false,
  "inventa_datos": true/false,
  "razon": "explicación breve en 1 frase"
}}"""


def evaluar_con_ia(input_texto: str, output_texto: str) -> dict:
    prompt = PROMPT_EVALUADOR.format(input=input_texto, output=output_texto)
    r = llamar_api(prompt, temperatura=0.0, max_tokens=150)
    try:
        return json.loads(r["output"])
    except:
        return {"coherente": None, "error": "No se pudo parsear la evaluación"}


# ─── GENERADOR CON RETRY ─────────────────────────────────────────────────────

def generar_con_retry(prompt_base: str, validador, max_intentos: int = 3) -> dict:
    prompt = prompt_base
    for intento in range(max_intentos):
        r = llamar_api(prompt, temperatura=0.1, max_tokens=200)
        v = validador(r["output"])
        if v.get("valido", False):
            return {**r, "intentos": intento + 1, "validacion": v}
        # Añade corrección al prompt
        prompt = prompt_base + f"\n\nEl intento anterior falló la validación: {v.get('error','formato incorrecto')}.\nDevuelve ÚNICAMENTE JSON válido."
    return {"output": None, "intentos": max_intentos, "error": "Max reintentos alcanzado"}


# ─── SIMULADOR DE DASHBOARD ──────────────────────────────────────────────────

def simular_metricas(n_outputs: int = 100) -> dict:
    """Simula métricas de producción para ilustrar el dashboard."""
    random.seed(42)
    formato_ok    = sum(1 for _ in range(n_outputs) if random.random() > 0.03)
    reintentos    = sum(1 for _ in range(n_outputs) if random.random() < 0.04)
    cola_humana   = sum(1 for _ in range(n_outputs) if random.random() < 0.06)
    aprobados     = sum(1 for _ in range(n_outputs) if random.random() > 0.22)
    alucinaciones = sum(1 for _ in range(n_outputs) if random.random() < 0.008)

    return {
        "total_outputs":         n_outputs,
        "formato_ok":            f"{formato_ok}/{n_outputs} ({formato_ok/n_outputs*100:.1f}%)",
        "tasa_reintento":        f"{reintentos/n_outputs*100:.1f}%",
        "cola_revision_humana":  f"{cola_humana/n_outputs*100:.1f}%",
        "aprobacion_directa":    f"{aprobados/n_outputs*100:.1f}%",
        "tasa_alucinacion":      f"{alucinaciones/n_outputs*100:.1f}%",
        "estado": {
            "formato":    "✅" if formato_ok/n_outputs > 0.97 else "⚠️",
            "reintento":  "✅" if reintentos/n_outputs < 0.05 else "⚠️",
            "cola":       "✅" if cola_humana/n_outputs < 0.07 else "⚠️",
            "aprobacion": "✅" if aprobados/n_outputs > 0.70 else "⚠️",
            "alucinacion":"✅" if alucinaciones/n_outputs < 0.01 else "⚠️",
        }
    }


# ─── MAIN ─────────────────────────────────────────────────────────────────────

OUTPUTS_TEST = [
    {"input": "Clasifica este email como consulta/reclamacion/pedido en JSON",
     "output": '{"categoria": "reclamacion", "urgencia": "alta", "confianza": 0.91}',
     "campos": ["categoria", "urgencia", "confianza"]},
    {"input": "Extrae nombre y precio del producto",
     "output": 'El producto es una silla ergonómica que cuesta 299 euros.',
     "campos": ["nombre", "precio"]},
    {"input": "Clasifica con JSON",
     "output": '{"categoria": "consulta"}',
     "campos": ["categoria", "urgencia"]},
]

if __name__ == "__main__":

    print("=" * 64)
    print("LAB 3.3 — Validación y Quality Assurance")
    print("=" * 64)

    tiene_api = bool(os.getenv("ANTHROPIC_API_KEY"))

    # ── EJERCICIO 1: Validadores automáticos ────────────────────────────────
    print("\n[1] VALIDADORES DE FORMATO (sin API)")
    print("-" * 64)

    for i, caso in enumerate(OUTPUTS_TEST):
        v = validar_json(caso["output"], caso["campos"])
        print(f"\n  Caso {i+1}: {'✅ VÁLIDO' if v['valido'] else '❌ INVÁLIDO'}")
        if v["error"]:
            print(f"    Error: {v['error']}")
        else:
            for campo, ok in v["campos"].items():
                print(f"    {'✓' if ok else '✗'} {campo}")

    # ── EJERCICIO 2: Evaluador IA ────────────────────────────────────────────
    print("\n\n[2] EVALUADOR IA DE COHERENCIA (Nivel 2)")
    print("-" * 64)

    if tiene_api:
        for caso in OUTPUTS_TEST[:2]:
            eval_r = evaluar_con_ia(caso["input"], caso["output"])
            print(f"\n  Input:  {caso['input'][:60]}")
            print(f"  Output: {caso['output'][:60]}")
            print(f"  Eval:   {eval_r}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY.")

    # ── EJERCICIO 3: Generador con retry ────────────────────────────────────
    print("\n\n[3] GENERADOR CON RETRY AUTOMÁTICO")
    print("-" * 64)

    if tiene_api:
        PROMPT_CLASIFICACION = """Clasifica este email. Devuelve SOLO JSON con campos: categoria, urgencia, confianza.
Email: "Mi pedido lleva 2 semanas sin llegar y nadie me responde." """

        validador = lambda output: validar_json(output, ["categoria", "urgencia", "confianza"])
        resultado = generar_con_retry(PROMPT_CLASIFICACION, validador)
        print(f"\n  Output: {resultado.get('output')}")
        print(f"  Intentos necesarios: {resultado.get('intentos')}")
        v = resultado.get('validacion', {})
        print(f"  Validación: {'✅ OK' if v.get('valido') else '❌ FALLÓ'}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY.")

    # ── EJERCICIO 4: Dashboard de métricas ──────────────────────────────────
    print("\n\n[4] DASHBOARD DE MÉTRICAS (simulado)")
    print("-" * 64)

    m = simular_metricas(100)
    print(f"\n  Período: última semana | Volumen: {m['total_outputs']} outputs\n")
    print(f"  {m['estado']['formato']}  Formato correcto:       {m['formato_ok']}")
    print(f"  {m['estado']['reintento']}  Tasa de reintento:      {m['tasa_reintento']}")
    print(f"  {m['estado']['cola']}  Cola revisión humana:   {m['cola_revision_humana']}")
    print(f"  {m['estado']['aprobacion']}  Aprobación directa:     {m['aprobacion_directa']}")
    print(f"  {m['estado']['alucinacion']}  Tasa de alucinación:    {m['tasa_alucinacion']}")

    print("\n[FIN DEL LAB 3.3]")
