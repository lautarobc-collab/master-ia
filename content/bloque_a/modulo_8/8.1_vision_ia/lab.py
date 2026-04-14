"""
LAB 8.1 — Visión por IA con Claude
=====================================
Objetivo: usar las capacidades multimodales de Claude para
analizar imágenes en casos de uso empresariales reales.

Ejercicios:
  1. Extracción de datos de factura (simula documento escaneado)
  2. Análisis de dashboard BI en imagen
  3. Inspección de calidad — criterios definidos por el negocio

Nota: los ejercicios usan imágenes públicas de ejemplo.
Para casos reales, sustituir por imágenes propias.

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json
import base64

MODELO = "claude-haiku-4-5-20251001"

# URLs de imágenes públicas para los ejercicios
# En producción, reemplazar con imágenes propias
IMAGEN_FACTURA_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/WebsiteRedesign_Mockup.png/800px-WebsiteRedesign_Mockup.png"
IMAGEN_GRAFICO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Scatter_diagram_for_quality_characteristic_XXX.svg/640px-Scatter_diagram_for_quality_characteristic_XXX.svg.png"
IMAGEN_PRODUCTO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Carre_de_chocolat.jpg/640px-Carre_de_chocolat.jpg"


def llamar_vision(url_imagen: str, prompt_texto: str,
                  media_type: str = "image/jpeg",
                  usar_url: bool = True,
                  max_tokens: int = 600) -> str:
    """Llama a la API de Claude con una imagen y un prompt."""
    try:
        import anthropic
        client = anthropic.Anthropic()

        if usar_url:
            contenido_imagen = {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": url_imagen,
                },
            }
        else:
            # Para imágenes locales, leer como base64
            with open(url_imagen, "rb") as f:
                datos_b64 = base64.standard_b64encode(f.read()).decode("utf-8")
            contenido_imagen = {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": datos_b64,
                },
            }

        respuesta = client.messages.create(
            model=MODELO,
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": [
                    contenido_imagen,
                    {"type": "text", "text": prompt_texto},
                ],
            }],
        )
        return respuesta.content[0].text.strip()

    except Exception as e:
        return f"[Error de visión: {e}]"


# ─── EJERCICIO 1: EXTRACCIÓN DE FACTURA ───────────────────────────────────────

PROMPT_EXTRACCION_FACTURA = """Analiza esta imagen y extrae todos los datos que puedas identificar.
Devuelve los datos en formato JSON con esta estructura:
{
  "tipo_documento": "tipo de documento identificado",
  "elementos_visuales": ["lista de elementos principales visibles"],
  "datos_texto": "texto relevante que puedas leer",
  "estructura": "descripción de la estructura del documento",
  "uso_empresarial_sugerido": "para qué podría usarse este documento en una empresa"
}
Si no puedes extraer algún campo, usa null."""

DATOS_FACTURA_SIMULADOS = {
    "numero_factura": "FAC-2025-00234",
    "fecha_emision": "2025-04-15",
    "proveedor": "Suministros Técnicos S.L.",
    "nif_proveedor": "B-12345678",
    "cliente": "Empresa Demo S.A.",
    "nif_cliente": "A-87654321",
    "concepto": "Materiales de oficina — Pedido PED-892",
    "base_imponible": 1250.00,
    "iva_porcentaje": 21,
    "iva_importe": 262.50,
    "total": 1512.50,
    "forma_pago": "Transferencia bancaria 30 días",
    "iban": "ES76 2100 0418 4502 0005 1332",
}


def ejercicio_1_extraccion_factura(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 1 — EXTRACCIÓN DE DATOS DE FACTURA (OCR + IA)")
    print("=" * 64)

    print("\n  Simulación de factura procesada:")
    print("  (En producción: enviar imagen escaneada a Claude)")
    print()

    if tiene_api:
        print(f"  Analizando imagen de ejemplo con Claude Vision...")
        print(f"  URL: {IMAGEN_FACTURA_URL[:60]}...")
        resultado = llamar_vision(
            IMAGEN_FACTURA_URL,
            PROMPT_EXTRACCION_FACTURA,
            media_type="image/png"
        )
        print("\n  Resultado del análisis visual:")
        try:
            datos = json.loads(resultado)
            for k, v in datos.items():
                if isinstance(v, list):
                    print(f"  {k}: {', '.join(v[:3])}")
                else:
                    print(f"  {k}: {v}")
        except json.JSONDecodeError:
            print(f"  {resultado}")

        # Demostrar el prompt ideal para una factura real
        print("\n  --- Prompt óptimo para factura real ---")
        prompt_factura_real = """Extrae los datos de esta factura y devuelve SOLO JSON válido:
{
  "numero_factura": null,
  "fecha_emision": "YYYY-MM-DD",
  "proveedor": null,
  "nif_proveedor": null,
  "base_imponible": 0.00,
  "iva_porcentaje": 0,
  "iva_importe": 0.00,
  "total": 0.00,
  "forma_pago": null,
  "confianza": "alta/media/baja"
}
Si un campo no es legible, usa null. El campo 'confianza' indica
tu nivel de seguridad en la extracción general."""
        print("  Prompt mostrado — aplicar a imagen de factura real.")
    else:
        print("  [Modo fallback — datos simulados de factura]")
        print()
        for k, v in DATOS_FACTURA_SIMULADOS.items():
            if isinstance(v, float):
                print(f"  {k}: {v:,.2f}€")
            else:
                print(f"  {k}: {v}")
        print()
        print("  Validaciones automáticas:")
        # Validar coherencia
        if abs(DATOS_FACTURA_SIMULADOS["base_imponible"] *
               DATOS_FACTURA_SIMULADOS["iva_porcentaje"] / 100 -
               DATOS_FACTURA_SIMULADOS["iva_importe"]) < 0.01:
            print("  ✓ IVA coherente con la base imponible")
        total_calculado = (DATOS_FACTURA_SIMULADOS["base_imponible"] +
                           DATOS_FACTURA_SIMULADOS["iva_importe"])
        if abs(total_calculado - DATOS_FACTURA_SIMULADOS["total"]) < 0.01:
            print("  ✓ Total coherente (base + IVA)")
        print("  [Configura ANTHROPIC_API_KEY para análisis real de imágenes]")


# ─── EJERCICIO 2: ANÁLISIS DE DASHBOARD ──────────────────────────────────────

PROMPT_DASHBOARD = """Esta imagen contiene un gráfico o diagrama de datos.
Analízala como si fuera un analista de negocio que debe presentar los hallazgos a la dirección.

Por favor:
1. Describe qué tipo de gráfico o visualización es
2. Identifica los ejes, leyendas o categorías visibles
3. Resume los patrones o tendencias más destacados
4. Proporciona 2-3 conclusiones en lenguaje ejecutivo
5. Sugiere qué preguntas de negocio podría responder este gráfico

Formato: texto estructurado, sin tecnicismos estadísticos."""

ANALISIS_DASHBOARD_SIMULADO = """
ANÁLISIS DE DASHBOARD — MODO SIMULADO

Tipo de gráfico: Dispersión (Scatter plot) de métricas de calidad

Hallazgos principales:
1. Se observa correlación positiva entre las dos variables medidas
2. Hay 3 puntos outliers en el cuadrante superior derecho que merecen atención
3. La distribución central sugiere estabilidad en el 80% de los casos

Conclusiones ejecutivas:
• La mayoría de los indicadores se mueven dentro del rango esperado
• Los outliers detectados requieren investigación — pueden indicar procesos
  no estandarizados o cambios en los inputs del sistema
• La tendencia general es positiva, con margen de mejora en los extremos

Preguntas de negocio que responde:
• ¿Hay correlación entre los dos factores medidos?
• ¿Existen casos atípicos que requieran acción?
• ¿Es el proceso lo suficientemente estable?
"""


def ejercicio_2_analisis_dashboard(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 2 — ANÁLISIS DE GRÁFICO/DASHBOARD EN IMAGEN")
    print("=" * 64)

    if tiene_api:
        print(f"\n  Analizando gráfico de ejemplo...")
        resultado = llamar_vision(
            IMAGEN_GRAFICO_URL,
            PROMPT_DASHBOARD,
            media_type="image/png",
            max_tokens=500
        )
        print("\n  Análisis ejecutivo:")
        print("  " + "─" * 50)
        for linea in resultado.split("\n"):
            print(f"  {linea}")

        # Segundo análisis: extraer métricas en JSON
        prompt_metricas = """Analiza esta visualización de datos y extrae en JSON:
{
  "tipo_grafico": "scatter/linea/barras/pastel/otro",
  "variables_identificadas": ["lista"],
  "rango_valores": "descripción del rango observable",
  "patron_principal": "1 frase",
  "nivel_dispersion": "bajo/medio/alto",
  "anomalias_detectadas": true/false
}"""
        print("\n  Extracción estructurada:")
        resultado_json = llamar_vision(IMAGEN_GRAFICO_URL, prompt_metricas,
                                       media_type="image/png", max_tokens=200)
        try:
            datos = json.loads(resultado_json)
            for k, v in datos.items():
                print(f"    {k}: {v}")
        except json.JSONDecodeError:
            print(f"  {resultado_json}")

    else:
        print(ANALISIS_DASHBOARD_SIMULADO)
        print("  [Configura ANTHROPIC_API_KEY para analizar imágenes reales de dashboards]")


# ─── EJERCICIO 3: INSPECCIÓN DE CALIDAD ──────────────────────────────────────

CRITERIOS_INSPECCION_CHOCOLATE = [
    "¿La superficie es lisa y uniforme, sin burbujas de aire visibles?",
    "¿El color es uniforme y brillante (indicador de buen temperado)?",
    "¿Los bordes están bien definidos y no presenta grietas?",
    "¿La textura parece homogénea o hay irregularidades?",
]

PROMPT_INSPECCION = """Eres un inspector de calidad en una línea de producción alimentaria.
Analiza esta imagen del producto según los siguientes criterios de calidad.

Para cada criterio, indica: CONFORME / NO CONFORME / NO DETERMINABLE
y una breve justificación (1 frase).

Criterios de inspección:
{criterios}

Al final, da un veredicto global: APROBADO / RECHAZADO / REVISAR
con el número de criterios que pasaron."""


def ejercicio_3_inspeccion_calidad(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 3 — INSPECCIÓN DE CALIDAD CON VISIÓN IA")
    print("=" * 64)

    criterios_texto = "\n".join([f"{i+1}. {c}" for i, c in
                                  enumerate(CRITERIOS_INSPECCION_CHOCOLATE)])

    if tiene_api:
        print(f"\n  Producto: Tableta de chocolate (imagen pública)")
        print(f"  Criterios de inspección: {len(CRITERIOS_INSPECCION_CHOCOLATE)}")
        print()

        prompt = PROMPT_INSPECCION.format(criterios=criterios_texto)
        resultado = llamar_vision(
            IMAGEN_PRODUCTO_URL,
            prompt,
            media_type="image/jpeg",
            max_tokens=500
        )
        print("  RESULTADO DE INSPECCIÓN:")
        print("  " + "─" * 50)
        for linea in resultado.split("\n"):
            print(f"  {linea}")

    else:
        print("\n  [Modo simulado — inspección por reglas]")
        print(f"\n  Producto analizado: tableta de chocolate")
        print(f"  Criterios evaluados: {len(CRITERIOS_INSPECCION_CHOCOLATE)}")
        print()
        # Simular resultado
        resultados_simulados = ["CONFORME", "CONFORME", "CONFORME", "NO DETERMINABLE"]
        for i, (criterio, res) in enumerate(zip(CRITERIOS_INSPECCION_CHOCOLATE, resultados_simulados)):
            icono = "✓" if res == "CONFORME" else "?" if "NO DET" in res else "✗"
            print(f"  {icono} Criterio {i+1}: {res}")
            print(f"    {criterio[:60]}...")
        conformes = resultados_simulados.count("CONFORME")
        print(f"\n  VEREDICTO GLOBAL: {'APROBADO' if conformes >= 3 else 'REVISAR'}")
        print(f"  ({conformes}/{len(CRITERIOS_INSPECCION_CHOCOLATE)} criterios conformes)")
        print()
        print("  [Configura ANTHROPIC_API_KEY para inspección real con visión IA]")

    print("\n  Cómo escalar este sistema:")
    print("  1. Captura automática con cámara en línea de producción")
    print("  2. Cada imagen → llamada a Claude con criterios del producto")
    print("  3. Resultado → registro en sistema de calidad + alerta si RECHAZADO")
    print("  4. Dashboard diario de tasa de conformidad por turno/máquina")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 8.1 — VISIÓN POR IA CON CLAUDE")
    print("=" * 64)

    tiene_api = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if tiene_api:
        print(f"  Modelo: {MODELO}")
        print("  Modo: API activa — análisis real de imágenes")
        print("  Nota: usando imágenes públicas de ejemplo")
        print("        Sustituir por imágenes propias en producción")
    else:
        print("  AVISO: ANTHROPIC_API_KEY no configurada.")
        print("  Modo: Fallback con datos simulados")
        print("  Para usar visión real: pip install anthropic + configurar API key")

    ejercicio_1_extraccion_factura(tiene_api)
    ejercicio_2_analisis_dashboard(tiene_api)
    ejercicio_3_inspeccion_calidad(tiene_api)

    print("\n" + "=" * 64)
    print("RESUMEN DEL LAB")
    print("=" * 64)
    print("""
  Casos de uso demostrados:
  ✓ Extracción estructurada de datos de documentos (OCR + IA)
  ✓ Análisis ejecutivo de gráficos y dashboards
  ✓ Inspección de calidad con criterios definidos por negocio

  Patrón de uso de visión IA:
    imagen + prompt específico → JSON estructurado → sistema corporativo

  Cuándo NO usar visión LLM:
    • Medición precisa (use visión clásica calibrada)
    • > 100 piezas/minuto (use sistema dedicado)
    • Documentos con datos ultra-confidenciales (evaluar on-premise)
""")

    print("[FIN DEL LAB 8.1]")
