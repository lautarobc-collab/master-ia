"""
LAB 3.2 — Identidad Comunicativa y Tono
=========================================
Objetivo: construir una guía de estilo corporativa, inyectarla
como system prompt y medir su impacto en la consistencia del tono.

Ejercicios:
  1. Detector de tono — analiza el estilo de un texto
  2. Transformador de tono — adapta el mismo contenido a 3 voces distintas
  3. Constructor de guía de estilo — genera la guía desde ejemplos reales

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import time

MODELO = "claude-sonnet-4-6"


def llamar_api(prompt, system="", temperatura=0.3, max_tokens=500):
    try:
        import anthropic
        client = anthropic.Anthropic()
        kwargs = dict(model=MODELO, max_tokens=max_tokens, temperature=temperatura,
                      messages=[{"role": "user", "content": prompt}])
        if system:
            kwargs["system"] = system
        inicio = time.time()
        r = client.messages.create(**kwargs)
        return {"output": r.content[0].text.strip(), "ms": round((time.time()-inicio)*1000)}
    except Exception as e:
        return {"output": f"Error: {e}", "ms": 0}


# ─── PARTE 1: DETECTOR DE TONO ────────────────────────────────────────────────

TEXTOS_ANALIZAR = {
    "corporativo_vacio": """En el marco de nuestra estrategia de transformación digital,
    nos complace anunciar la implementación de soluciones innovadoras de inteligencia
    artificial que potenciarán las sinergias interdepartamentales y generarán valor
    añadido en todo el ecosistema organizacional.""",

    "directo_datos": """El piloto de IA redujo el tiempo de clasificación de incidencias
    de 4.2 horas a 0.8 horas por ciclo. En el mes de marzo procesamos 1.240 incidencias.
    El ahorro neto fue de 4.216 horas — equivalente a 2 personas a tiempo completo.""",

    "ambiguo": """Los resultados del proyecto han sido bastante positivos en general,
    aunque hay algunas áreas donde podría mejorarse un poco la adopción por parte
    de ciertos equipos que todavía están en proceso de adaptación.""",
}

PROMPT_DETECTOR = """Analiza el tono de este texto corporativo y evalúa en escala 1-5:
- Formalidad (1=muy informal, 5=muy formal)
- Densidad informativa (1=mucho relleno, 5=solo datos útiles)
- Orientación a la acción (1=descriptivo, 5=orientado a decisión)
- Riesgo de "sonido IA" (1=suena humano, 5=claramente generado por IA)

Identifica las 2 palabras o frases más débiles del texto.
Responde en formato JSON.

TEXTO: {texto}"""


# ─── PARTE 2: TRANSFORMADOR DE TONO ──────────────────────────────────────────

CONTENIDO_BASE = """
Datos del mes de abril:
- Volumen de tickets de soporte: 1.847
- Tiempo medio de resolución: 6.2 horas
- Tickets resueltos en primera respuesta: 34%
- Satisfacción cliente: 6.8/10
- Tickets escalados a nivel 2: 312 (17%)
- Coste operativo: 28.400€
"""

ESTILOS = {
    "ejecutivo": {
        "desc": "Para el Comité de Dirección — decisión sobre ampliar el equipo de soporte",
        "system": "Eres redactor ejecutivo. Directo, orientado a decisión. Conclusión primero. Max 120 palabras."
    },
    "operativo": {
        "desc": "Para el jefe de equipo de soporte — reunión semanal de revisión",
        "system": "Eres analista de operaciones. Detallado, orientado a mejora. Identifica el problema raíz. Max 150 palabras."
    },
    "cliente": {
        "desc": "Para comunicar el estado del servicio a clientes enterprise",
        "system": "Eres responsable de customer success. Tono positivo pero honesto. Sin métricas internas. Max 100 palabras."
    },
}

PROMPT_TRANSFORMADOR = """Redacta una comunicación sobre los datos de soporte del mes de abril.
Propósito: {desc}

DATOS:
{datos}"""


# ─── PARTE 3: GENERADOR DE GUÍA DE ESTILO ────────────────────────────────────

EJEMPLOS_EMPRESA = [
    {
        "malo": "En aras de optimizar la eficiencia operacional, se ha procedido a la implementación de mejoras sustanciales.",
        "bueno": "Reducimos el tiempo de procesamiento de 4h a 1h cambiando el flujo de aprobación."
    },
    {
        "malo": "El equipo está trabajando arduamente para potenciar las capacidades digitales de la organización.",
        "bueno": "El equipo termina la formación en Python el 15 de mayo. Después pueden mantener los pipelines solos."
    },
    {
        "malo": "Los resultados han sido muy satisfactorios y esperamos continuar en esta línea de éxito.",
        "bueno": "ROI del trimestre: 340%. Meta para Q2: 400%. Bloqueador actual: falta de datos limpios en ERP."
    },
]

PROMPT_GUIA = """Analiza estos pares de textos (malo/bueno) de una empresa y genera una guía de estilo
corporativa en formato JSON con estas secciones:
- voz_empresa: descripción en 2 frases
- palabras_prohibidas: lista de 8-10 palabras/expresiones a evitar
- palabras_preferidas: lista de 8-10 alternativas concretas
- reglas_formato: 3-5 reglas de estructura
- ejemplo_bueno_adicional: un ejemplo nuevo que respete el estilo detectado

PARES DE EJEMPLO:
{ejemplos}"""


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 64)
    print("LAB 3.2 — Identidad Comunicativa y Tono")
    print("=" * 64)

    tiene_api = bool(os.getenv("ANTHROPIC_API_KEY"))

    # ── EJERCICIO 1: Detector de tono ───────────────────────────────────────
    print("\n[1] DETECTOR DE TONO")
    print("-" * 64)

    if tiene_api:
        for nombre, texto in TEXTOS_ANALIZAR.items():
            prompt = PROMPT_DETECTOR.format(texto=texto)
            r = llamar_api(prompt, temperatura=0.1, max_tokens=300)
            print(f"\n  [{nombre}]\n  {r['output']}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY.")
        print("  Resultado esperado: 'corporativo_vacio' score bajo en densidad y alto en riesgo IA.")

    # ── EJERCICIO 2: Transformador de tono ──────────────────────────────────
    print("\n\n[2] MISMO CONTENIDO, 3 TONOS DISTINTOS")
    print("-" * 64)

    if tiene_api:
        for estilo, config in ESTILOS.items():
            prompt = PROMPT_TRANSFORMADOR.format(desc=config["desc"], datos=CONTENIDO_BASE)
            r = llamar_api(prompt, system=config["system"], temperatura=0.3, max_tokens=300)
            print(f"\n  [{estilo.upper()}]\n  {r['output']}\n  [{r['ms']}ms]")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY.")
        print("  Resultado esperado: mismo dato, 3 narrativas radicalmente distintas.")

    # ── EJERCICIO 3: Generador de guía de estilo ────────────────────────────
    print("\n\n[3] GENERADOR DE GUÍA DE ESTILO")
    print("-" * 64)

    if tiene_api:
        import json
        ejemplos_str = json.dumps(EJEMPLOS_EMPRESA, ensure_ascii=False, indent=2)
        prompt = PROMPT_GUIA.format(ejemplos=ejemplos_str)
        r = llamar_api(prompt, temperatura=0.4, max_tokens=600)
        print(f"\n{r['output']}")
        print(f"\n  → Guarda este JSON como 'guia_estilo.json' y úsalo en tus system prompts.")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY.")
        print("  El generador crea una guía JSON lista para usar como system prompt.")

    print("\n[FIN DEL LAB 3.2]")
