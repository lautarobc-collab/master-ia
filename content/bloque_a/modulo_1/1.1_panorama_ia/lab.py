"""
LAB 1.1 — Mapa de la Industria IA y Análisis de Tokens
=======================================================
Objetivo: visualizar cómo los LLMs tokenizamos texto y comparar
el coste/latencia de distintos modelos en una decisión real de empresa.

Requisitos:
    pip install anthropic tiktoken pandas tabulate

Ejecutar:
    python lab.py
"""

import time
import json

# ─── PARTE 1: Tokenización ────────────────────────────────────────────────────
# Los LLMs no ven "palabras" — ven tokens (subpalabras).
# Entender tokens es crítico para controlar costes y límites de contexto.

def analizar_tokens(texto: str) -> dict:
    """
    Muestra cómo un tokenizador BPE fragmenta el texto.
    GPT-4 usa cl100k_base; Claude usa su propio tokenizador similar.
    """
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(texto)
        tokens_decodificados = [enc.decode([t]) for t in tokens]
        return {
            "texto_original": texto,
            "num_tokens": len(tokens),
            "tokens_ids": tokens[:20],  # primeros 20
            "tokens_texto": tokens_decodificados[:20],
            "ratio_tokens_palabras": round(len(tokens) / len(texto.split()), 2)
        }
    except ImportError:
        return {"error": "Instala tiktoken: pip install tiktoken"}


# ─── PARTE 2: Comparador de Modelos ──────────────────────────────────────────
# Decisión empresarial: ¿qué modelo usar para cada tarea?

MODELOS_REFERENCIA = {
    "claude-haiku-4-5":   {"coste_input_1M": 0.80,  "coste_output_1M": 4.00,  "contexto_k": 200, "velocidad": "muy alta",  "calidad": "buena"},
    "claude-sonnet-4-5":  {"coste_input_1M": 3.00,  "coste_output_1M": 15.00, "contexto_k": 200, "velocidad": "alta",     "calidad": "muy alta"},
    "claude-opus-4-5":    {"coste_input_1M": 15.00, "coste_output_1M": 75.00, "contexto_k": 200, "velocidad": "media",    "calidad": "máxima"},
    "gpt-4o-mini":        {"coste_input_1M": 0.15,  "coste_output_1M": 0.60,  "contexto_k": 128, "velocidad": "muy alta",  "calidad": "buena"},
    "gpt-4o":             {"coste_input_1M": 5.00,  "coste_output_1M": 15.00, "contexto_k": 128, "velocidad": "alta",     "calidad": "muy alta"},
}

def calcular_coste_mensual(modelo: str, tokens_input_dia: int, tokens_output_dia: int, dias: int = 30) -> dict:
    """
    Calcula el coste mensual real de un modelo dado el volumen de uso.

    Parámetros:
        modelo: nombre del modelo
        tokens_input_dia: tokens de entrada promedio por día
        tokens_output_dia: tokens de salida promedio por día
        dias: días del período
    """
    if modelo not in MODELOS_REFERENCIA:
        return {"error": f"Modelo '{modelo}' no encontrado"}

    m = MODELOS_REFERENCIA[modelo]
    coste_input  = (tokens_input_dia  * dias / 1_000_000) * m["coste_input_1M"]
    coste_output = (tokens_output_dia * dias / 1_000_000) * m["coste_output_1M"]
    total = coste_input + coste_output

    return {
        "modelo": modelo,
        "tokens_procesados": (tokens_input_dia + tokens_output_dia) * dias,
        "coste_input_usd": round(coste_input, 2),
        "coste_output_usd": round(coste_output, 2),
        "coste_total_usd": round(total, 2),
        "calidad": m["calidad"],
        "velocidad": m["velocidad"]
    }


# ─── PARTE 3: Llamada real a Claude ──────────────────────────────────────────
# Demostración de cómo los LLMs procesan una pregunta empresarial.

def consultar_claude(pregunta: str, modelo: str = "claude-haiku-4-5-20251001") -> dict:
    """
    Envía una pregunta a Claude y mide latencia + tokens usados.

    PARÁMETROS CLAVE:
        max_tokens: límite de tokens en la respuesta (controla coste y longitud)
        temperature: 0.0 = determinista, 1.0 = creativo (aquí usamos 0.3 = factual)
    """
    try:
        import anthropic
        client = anthropic.Anthropic()

        inicio = time.time()
        respuesta = client.messages.create(
            model=modelo,
            max_tokens=512,
            temperature=0.3,  # bajo → respuestas consistentes y factuales
            messages=[
                {"role": "user", "content": pregunta}
            ]
        )
        latencia_ms = round((time.time() - inicio) * 1000)

        return {
            "respuesta": respuesta.content[0].text,
            "tokens_input": respuesta.usage.input_tokens,
            "tokens_output": respuesta.usage.output_tokens,
            "latencia_ms": latencia_ms,
            "modelo": respuesta.model,
            "coste_estimado_usd": round(
                (respuesta.usage.input_tokens / 1_000_000 * 0.80) +
                (respuesta.usage.output_tokens / 1_000_000 * 4.00), 6
            )
        }
    except ImportError:
        return {"error": "Instala anthropic: pip install anthropic"}
    except Exception as e:
        return {"error": str(e)}


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 60)
    print("LAB 1.1 — Panorama de la IA: Tokens, Costes y Modelos")
    print("=" * 60)

    # EJERCICIO 1: Tokenización
    print("\n[1] ANÁLISIS DE TOKENIZACIÓN")
    print("-" * 40)
    textos = [
        "IA aplicada a la gestión empresarial",
        "Artificial Intelligence applied to enterprise management",
        "supercalifragilisticoespialidoso",  # ← palabra rara: más tokens
    ]
    for texto in textos:
        resultado = analizar_tokens(texto)
        if "error" not in resultado:
            print(f"Texto: '{texto}'")
            print(f"  Tokens: {resultado['num_tokens']} | Ratio tok/palabra: {resultado['ratio_tokens_palabras']}")
            print(f"  Fragmentos: {resultado['tokens_texto']}")
        else:
            print(f"  {resultado['error']}")

    # EJERCICIO 2: Comparativa de costes
    print("\n[2] COMPARATIVA DE COSTES — CASO: CHATBOT INTERNO (10k consultas/día)")
    print("-" * 60)
    # Asumimos: prompt promedio = 500 tokens input, 200 tokens output
    tokens_input_dia  = 10_000 * 500   # 5M tokens/día
    tokens_output_dia = 10_000 * 200   # 2M tokens/día

    print(f"{'Modelo':<25} {'Coste/mes USD':>13} {'Calidad':>10} {'Velocidad':>12}")
    print("-" * 65)
    for modelo in MODELOS_REFERENCIA:
        r = calcular_coste_mensual(modelo, tokens_input_dia, tokens_output_dia)
        print(f"{r['modelo']:<25} ${r['coste_total_usd']:>12,.2f} {r['calidad']:>10} {r['velocidad']:>12}")

    # EJERCICIO 3: Llamada real (requiere ANTHROPIC_API_KEY)
    print("\n[3] LLAMADA REAL A CLAUDE — Pregunta empresarial")
    print("-" * 40)
    print("NOTA: Requiere variable de entorno ANTHROPIC_API_KEY")
    print("      Configura con: export ANTHROPIC_API_KEY='sk-ant-...'")

    import os
    if os.getenv("ANTHROPIC_API_KEY"):
        pregunta = (
            "En máximo 3 bullets, ¿cuáles son las 3 barreras más comunes "
            "que frenan la adopción de IA en empresas medianas europeas?"
        )
        resultado = consultar_claude(pregunta)
        if "error" not in resultado:
            print(f"\nPregunta: {pregunta}")
            print(f"\nRespuesta:\n{resultado['respuesta']}")
            print(f"\n--- Métricas ---")
            print(f"Tokens input:  {resultado['tokens_input']}")
            print(f"Tokens output: {resultado['tokens_output']}")
            print(f"Latencia:      {resultado['latencia_ms']} ms")
            print(f"Coste:         ${resultado['coste_estimado_usd']} USD")
        else:
            print(f"Error: {resultado['error']}")
    else:
        print("  → Saltando (sin API key configurada)")

    # RESULTADO ESPERADO:
    # - Tokenización: "supercalifragilístico" → +5 tokens que en inglés
    # - Coste: Haiku ~$336/mes vs Opus ~$14,175/mes para mismo volumen
    # - Latencia típica Haiku: 300-800ms | Opus: 1500-4000ms
    print("\n[FIN DEL LAB 1.1]")
