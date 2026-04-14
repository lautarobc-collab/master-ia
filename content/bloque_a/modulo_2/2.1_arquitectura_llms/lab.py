"""
LAB 2.1 — Explorador de Arquitectura LLM
==========================================
Objetivo: experimentar directamente con los conceptos del módulo —
tokenización, temperatura, ventana de contexto y alucinaciones —
para construir intuición práctica sobre cómo funcionan los LLMs.

Ejercicios:
  1. Tokenizador — cuenta tokens y entiende el coste real
  2. Experimento de temperatura — mismo prompt, distintos comportamientos
  3. Límites del contexto — qué pasa cuando el modelo no tiene datos
  4. Detector de alucinaciones — técnica de grounding con documentos

Requisitos:
    pip install anthropic tiktoken

Ejecutar:
    python lab.py
"""

import os
import time
import json

# ─── PARTE 1: TOKENIZADOR ─────────────────────────────────────────────────────

def contar_tokens_aproximado(texto: str) -> dict:
    """
    Estimación de tokens sin API externa.
    Regla práctica: ~1 token por 4 caracteres en inglés, ~1.3 en español.
    """
    chars = len(texto)
    palabras = len(texto.split())
    tokens_estimados = round(chars / 3.8)  # estimación para español

    # Coste aproximado (Claude Haiku input: $0.80/1M tokens)
    coste_haiku_usd   = (tokens_estimados / 1_000_000) * 0.80
    coste_sonnet_usd  = (tokens_estimados / 1_000_000) * 3.00
    coste_opus_usd    = (tokens_estimados / 1_000_000) * 15.00

    return {
        "caracteres":       chars,
        "palabras":         palabras,
        "tokens_estimados": tokens_estimados,
        "ratio_tokens_palabra": round(tokens_estimados / palabras, 2) if palabras else 0,
        "coste_haiku_usd":  round(coste_haiku_usd, 6),
        "coste_sonnet_usd": round(coste_sonnet_usd, 6),
        "coste_opus_usd":   round(coste_opus_usd, 6),
    }


TEXTOS_EJEMPLO = {
    "corporativo_es": "La transformación digital implica la integración de tecnologías digitales en todas las áreas de una empresa.",
    "tecnico_en":     "The attention mechanism allows each token to attend to all other tokens in the sequence.",
    "numeros":        "El ROI fue del 1.385% con un payback de 0.8 meses y un beneficio neto de 19.400€.",
    "palabras_raras": "La anticonstitucionalidad del precepto jurisprudencial fue cuestionada en el tribunal.",
    "codigo":         "def calcular_roi(beneficio, inversion): return (beneficio - inversion) / inversion * 100",
}


# ─── PARTE 2: EXPERIMENTO DE TEMPERATURA ─────────────────────────────────────

def experimento_temperatura(prompt: str, temperaturas: list, modelo: str = "claude-haiku-4-5-20251001") -> list:
    """
    Ejecuta el mismo prompt con distintas temperaturas y muestra
    cómo varía la respuesta. Ilustra el efecto del sampling.
    """
    try:
        import anthropic
        client = anthropic.Anthropic()
        resultados = []

        for temp in temperaturas:
            inicio = time.time()
            resp = client.messages.create(
                model=modelo,
                max_tokens=120,
                temperature=temp,
                messages=[{"role": "user", "content": prompt}]
            )
            latencia = round((time.time() - inicio) * 1000)
            resultados.append({
                "temperatura": temp,
                "respuesta": resp.content[0].text.strip(),
                "tokens": resp.usage.output_tokens,
                "latencia_ms": latencia,
            })

        return resultados

    except ImportError:
        return [{"error": "pip install anthropic"}]
    except Exception as e:
        return [{"error": str(e)}]


# ─── PARTE 3: LÍMITES DEL CONOCIMIENTO (ALUCINACIÓN CONTROLADA) ──────────────

def test_alucinacion(pregunta_sin_contexto: str, pregunta_con_contexto: str,
                     contexto: str, modelo: str = "claude-haiku-4-5-20251001") -> dict:
    """
    Compara la respuesta del modelo CON y SIN contexto de referencia.
    Demuestra cómo el grounding reduce las alucinaciones.
    """
    try:
        import anthropic
        client = anthropic.Anthropic()

        # Sin contexto — terreno fértil para alucinaciones
        resp_sin = client.messages.create(
            model=modelo,
            max_tokens=200,
            temperature=0.0,
            messages=[{
                "role": "user",
                "content": pregunta_sin_contexto + "\nResponde con datos concretos."
            }]
        )

        # Con contexto — grounding sobre documento real
        resp_con = client.messages.create(
            model=modelo,
            max_tokens=200,
            temperature=0.0,
            messages=[{
                "role": "user",
                "content": f"Basándote ÚNICAMENTE en el siguiente texto, responde la pregunta. "
                           f"Si la respuesta no está en el texto, di 'No disponible en el documento'.\n\n"
                           f"TEXTO:\n{contexto}\n\n"
                           f"PREGUNTA: {pregunta_con_contexto}"
            }]
        )

        return {
            "sin_contexto": resp_sin.content[0].text.strip(),
            "con_contexto": resp_con.content[0].text.strip(),
        }

    except ImportError:
        return {"error": "pip install anthropic"}
    except Exception as e:
        return {"error": str(e)}


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 64)
    print("LAB 2.1 — Explorador de Arquitectura LLM")
    print("=" * 64)

    # ── EJERCICIO 1: Tokenizador ─────────────────────────────────────────────
    print("\n[1] TOKENIZADOR — Coste real de tus textos")
    print("-" * 64)

    for nombre, texto in TEXTOS_EJEMPLO.items():
        t = contar_tokens_aproximado(texto)
        print(f"\n  '{nombre}'")
        print(f"    Palabras: {t['palabras']} | Tokens ≈ {t['tokens_estimados']} "
              f"(ratio {t['ratio_tokens_palabra']} t/palabra)")
        print(f"    Coste input: Haiku ${t['coste_haiku_usd']} | "
              f"Sonnet ${t['coste_sonnet_usd']} | Opus ${t['coste_opus_usd']}")

    print("\n  ESCALA: 10.000 llamadas con prompt de 500 tokens:")
    tokens_total = 500 * 10_000
    print(f"    Haiku:  ${tokens_total / 1_000_000 * 0.80:.2f}")
    print(f"    Sonnet: ${tokens_total / 1_000_000 * 3.00:.2f}")
    print(f"    Opus:   ${tokens_total / 1_000_000 * 15.0:.2f}")

    # ── EJERCICIO 2: Temperatura ─────────────────────────────────────────────
    print("\n\n[2] EXPERIMENTO DE TEMPERATURA")
    print("-" * 64)

    PROMPT_TEMPERATURA = (
        "En una frase, describe cómo la IA está transformando el trabajo de los directivos."
    )

    if os.getenv("ANTHROPIC_API_KEY"):
        print(f"\n  Prompt: '{PROMPT_TEMPERATURA}'")
        print("  Ejecutando con temperaturas 0.0, 0.5 y 1.0...\n")

        resultados = experimento_temperatura(PROMPT_TEMPERATURA, [0.0, 0.5, 1.0])
        for r in resultados:
            if "error" in r:
                print(f"  Error: {r['error']}")
                break
            print(f"  Temp {r['temperatura']}: {r['respuesta']}")
            print(f"           [{r['tokens']} tokens | {r['latencia_ms']}ms]\n")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY para ejecutar este ejercicio.")
        print("  Resultado esperado: temp=0.0 produce respuestas consistentes y similares")
        print("  entre ejecuciones; temp=1.0 produce variaciones más creativas.")

    # ── EJERCICIO 3: Alucinación vs Grounding ───────────────────────────────
    print("\n\n[3] ALUCINACIÓN vs GROUNDING")
    print("-" * 64)

    # Datos ficticios de una empresa ficticia — el modelo no los conoce
    CONTEXTO_EMPRESA = """
    Informe Q3 2024 — Empresa Distribuciones Norte S.L.
    Facturación Q3: 2.340.000€ (+12% vs Q3 2023)
    Margen bruto: 34,2%
    Empleados: 87 (3 incorporaciones en julio)
    Proyecto IA en curso: automatización de pedidos, inversión 45.000€, go-live previsto Q1 2025
    Incidencias logísticas: 23 en Q3 (bajada desde 41 en Q2)
    """

    PREGUNTA_SIN = "¿Cuál fue la facturación de Distribuciones Norte S.L. en Q3 2024?"
    PREGUNTA_CON = "¿Cuál fue la facturación en Q3 2024 y cuántas incidencias logísticas hubo?"

    if os.getenv("ANTHROPIC_API_KEY"):
        print("\n  Probando misma empresa con y sin contexto...\n")
        resultado = test_alucinacion(PREGUNTA_SIN, PREGUNTA_CON, CONTEXTO_EMPRESA)

        if "error" in resultado:
            print(f"  Error: {resultado['error']}")
        else:
            print(f"  SIN contexto: {resultado['sin_contexto']}")
            print(f"\n  CON contexto: {resultado['con_contexto']}")
            print("\n  → Sin contexto el modelo inventa datos plausibles.")
            print("  → Con contexto responde con los datos reales o reconoce que no sabe.")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY para ejecutar este ejercicio.")
        print("  Sin contexto → el modelo generará datos inventados pero plausibles.")
        print("  Con contexto → el modelo usa los datos del documento o dice 'No disponible'.")

    # RESULTADO ESPERADO:
    # 1. Tokens: texto técnico en inglés ~1.2 t/palabra, español ~1.5-1.7 t/palabra
    # 2. Temperatura: respuestas más deterministas a 0.0, más variadas a 1.0
    # 3. Grounding: sin contexto → invención plausible, con contexto → dato exacto
    print("\n[FIN DEL LAB 2.1]")
