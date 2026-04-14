"""
LAB 3.1 — Ingeniería de Outputs Corporativos
=============================================
Objetivo: construir un sistema de plantillas de producción y
medir el impacto del diseño del output en la calidad final.

Ejercicios:
  1. Generador de informes ejecutivos con plantilla estructurada
  2. Comparativa: output genérico vs output con ingeniería
  3. Sistema de validación automática de calidad del output

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import re
import time
import json

MODELO = "claude-sonnet-4-6"


def llamar_api(prompt: str, system: str = "", temperatura: float = 0.3,
               max_tokens: int = 500) -> dict:
    try:
        import anthropic
        client = anthropic.Anthropic()
        kwargs = dict(model=MODELO, max_tokens=max_tokens, temperature=temperatura,
                      messages=[{"role": "user", "content": prompt}])
        if system:
            kwargs["system"] = system
        inicio = time.time()
        resp = client.messages.create(**kwargs)
        return {
            "output": resp.content[0].text.strip(),
            "tokens": resp.usage.input_tokens + resp.usage.output_tokens,
            "ms": round((time.time() - inicio) * 1000),
        }
    except ImportError:
        return {"output": "pip install anthropic", "tokens": 0, "ms": 0}
    except Exception as e:
        return {"output": f"Error: {e}", "tokens": 0, "ms": 0}


# ─── PARTE 1: GENERADOR DE INFORMES EJECUTIVOS ───────────────────────────────

SYSTEM_INFORME = """Eres un redactor ejecutivo senior especializado en comunicación corporativa de alto nivel.
Produces informes concisos, directos y orientados a la decisión.
Nunca usas: jerga técnica innecesaria, palabras como 'sinergias', 'innovador', 'disruptivo', 'ecosistema'.
Siempre separas hechos de interpretaciones."""

PLANTILLA_INFORME = """Redacta un informe ejecutivo de máximo 200 palabras sobre el siguiente tema.
Audiencia: {audiencia}
Propósito: tomar una decisión sobre {decision}

Estructura OBLIGATORIA (usa exactamente estos labels):
TITULAR: [la conclusión en 1 frase, no el tema]
CONTEXTO: [2 frases de situación]
HALLAZGOS:
• [dato 1]
• [dato 2]
• [dato 3]
IMPLICACIÓN: [qué significa para el negocio en 2 frases]
RECOMENDACIÓN: [acción concreta] — Criterio de éxito: [métrica]

INFORMACIÓN BASE:
{datos}"""

DATOS_EJEMPLO = """
Proyecto piloto IA en departamento de operaciones — Resultados Q1 2025:
- 3 procesos automatizados: clasificación de incidencias, generación de SOPs, resumen de reuniones
- Tiempo de procesamiento reducido de 4.2h a 0.8h por ciclo (81% de reducción)
- Tasa de error humano en clasificación: bajó de 12% a 2.3%
- Coste del piloto: 8.500€ (desarrollo) + 180€/mes (API)
- Satisfacción del equipo: 7.2/10 (encuesta a 14 personas)
- Adopción efectiva: 9 de 14 personas usan el sistema diariamente
- Bloqueador identificado: 5 personas con dificultad de adaptación necesitan formación adicional
"""


# ─── PARTE 2: COMPARATIVA GENÉRICO VS INGENIERÍA ─────────────────────────────

PROMPT_GENERICO = f"""Resume los resultados del piloto de IA y da una recomendación.

{DATOS_EJEMPLO}"""

PROMPT_INGENIERADO = PLANTILLA_INFORME.format(
    audiencia="Comité de Dirección — decidirá si escalar el proyecto a toda la empresa",
    decision="escalar o pausar el proyecto de IA en operaciones",
    datos=DATOS_EJEMPLO
)


# ─── PARTE 3: VALIDADOR DE CALIDAD ───────────────────────────────────────────

def validar_informe_ejecutivo(texto: str) -> dict:
    """
    Valida que un informe ejecutivo cumple los criterios de calidad
    sin llamar a la API — validación heurística local.
    """
    checks = {}

    # Estructura obligatoria
    checks["tiene_titular"]       = "TITULAR:" in texto.upper()
    checks["tiene_contexto"]      = "CONTEXTO:" in texto.upper()
    checks["tiene_hallazgos"]     = "HALLAZGOS" in texto.upper()
    checks["tiene_implicacion"]   = "IMPLICACI" in texto.upper()
    checks["tiene_recomendacion"] = "RECOMENDACI" in texto.upper()

    # Longitud
    palabras = len(texto.split())
    checks["longitud_ok"] = 50 <= palabras <= 220

    # Palabras prohibidas
    prohibidas = ["sinergias", "innovador", "disruptivo", "ecosistema", "paradigma"]
    checks["sin_palabras_prohibidas"] = not any(p in texto.lower() for p in prohibidas)

    # Bullets (al menos 2)
    bullets = len(re.findall(r"[•\-\*]\s", texto))
    checks["tiene_bullets"] = bullets >= 2

    puntuacion = sum(checks.values())
    total      = len(checks)

    return {
        "checks":     checks,
        "puntuacion": f"{puntuacion}/{total}",
        "aprobado":   puntuacion >= total - 1,
        "palabras":   palabras,
    }


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 64)
    print("LAB 3.1 — Ingeniería de Outputs Corporativos")
    print("=" * 64)

    tiene_api = bool(os.getenv("ANTHROPIC_API_KEY"))

    # ── EJERCICIO 1: Generador de informes ──────────────────────────────────
    print("\n[1] GENERADOR DE INFORME EJECUTIVO")
    print("-" * 64)

    if tiene_api:
        print("\n  Generando con plantilla estructurada...")
        r = llamar_api(PROMPT_INGENIERADO, system=SYSTEM_INFORME, temperatura=0.3, max_tokens=400)
        print(f"\n{r['output']}")
        print(f"\n  → {r['tokens']} tokens | {r['ms']}ms")

        print("\n  Validando calidad del output...")
        v = validar_informe_ejecutivo(r['output'])
        print(f"\n  Puntuación: {v['puntuacion']} | Palabras: {v['palabras']}")
        for check, ok in v["checks"].items():
            print(f"  {'✓' if ok else '✗'} {check.replace('_', ' ')}")
        print(f"\n  {'✅ APROBADO' if v['aprobado'] else '❌ REVISAR PROMPT'}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY para ejecutar.")

    # ── EJERCICIO 2: Comparativa ────────────────────────────────────────────
    print("\n\n[2] COMPARATIVA: PROMPT GENÉRICO vs INGENIERADO")
    print("-" * 64)

    if tiene_api:
        print("\n  [Genérico]")
        r_gen = llamar_api(PROMPT_GENERICO, temperatura=0.3, max_tokens=400)
        print(r_gen['output'][:600] + ("..." if len(r_gen['output']) > 600 else ""))
        v_gen = validar_informe_ejecutivo(r_gen['output'])
        print(f"\n  Calidad genérico: {v_gen['puntuacion']}")

        print("\n  [Ingenierado]")
        r_ing = llamar_api(PROMPT_INGENIERADO, system=SYSTEM_INFORME, temperatura=0.3, max_tokens=400)
        print(r_ing['output'][:600] + ("..." if len(r_ing['output']) > 600 else ""))
        v_ing = validar_informe_ejecutivo(r_ing['output'])
        print(f"\n  Calidad ingenierado: {v_ing['puntuacion']}")

        diff_tokens = r_ing['tokens'] - r_gen['tokens']
        print(f"\n  Diferencia de tokens: +{diff_tokens} (coste del diseño)")
        print("  → El prompt ingenierado consume más tokens pero elimina la revisión manual.")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY para la comparativa.")

    # ── EJERCICIO 3: Validador standalone ───────────────────────────────────
    print("\n\n[3] VALIDADOR DE CALIDAD (sin API)")
    print("-" * 64)

    informe_test = """
TITULAR: El piloto de IA en operaciones logra 81% de reducción de tiempo y justifica escalar.
CONTEXTO: Durante Q1 2025 se automatizaron 3 procesos clave con un coste de 8.500€. Los resultados superan los objetivos iniciales en eficiencia pero muestran una brecha de adopción.
HALLAZGOS:
• Tiempo de procesamiento: de 4.2h a 0.8h por ciclo (81% reducción)
• Tasa de error: bajó de 12% a 2.3% en clasificación de incidencias
• Adopción: 9/14 personas usan el sistema diariamente; 5 necesitan formación adicional
IMPLICACIÓN: El ROI técnico es sólido y el sistema está listo para escalar. El riesgo principal es la adopción humana, no la tecnología.
RECOMENDACIÓN: Escalar a operaciones completas en Q2 con plan de formación paralelo para los 5 usuarios rezagados. — Criterio de éxito: adopción > 90% en 60 días.
"""

    v = validar_informe_ejecutivo(informe_test)
    print(f"\n  Puntuación: {v['puntuacion']} | Palabras: {v['palabras']}")
    for check, ok in v["checks"].items():
        print(f"  {'✓' if ok else '✗'} {check.replace('_', ' ')}")
    print(f"\n  {'✅ APROBADO' if v['aprobado'] else '❌ REVISAR'}")

    print("\n[FIN DEL LAB 3.1]")
