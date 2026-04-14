"""
LAB 9.2 — Políticas de IA Generativa en la Empresa
=====================================================
Objetivo: construir herramientas prácticas para implementar
y aplicar una política de IA corporativa.

Ejercicios:
  1. Clasificador de datos — ¿puede este dato usarse con IA externa?
  2. Validador de outputs — detectar alucinaciones y contenido problemático
  3. Generador de política de IA corporativa personalizada

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json

MODELO = "claude-haiku-4-5-20251001"


def llamar_api(prompt, system="", max_tokens=700):
    try:
        import anthropic
        client = anthropic.Anthropic()
        kwargs = dict(
            model=MODELO,
            max_tokens=max_tokens,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        if system:
            kwargs["system"] = system
        r = client.messages.create(**kwargs)
        return r.content[0].text.strip()
    except Exception as e:
        return f"[Error API: {e}]"


# ─── DEFINICIÓN DE POLÍTICA (configurable) ───────────────────────────────────

POLITICA_EMPRESA = {
    "nombre_empresa": "Distribuciones Ejemplo S.A.",
    "herramientas_aprobadas": [
        {"nombre": "Claude (Anthropic)", "nivel": "N2-N3", "dpa": True, "url": "claude.ai"},
        {"nombre": "GitHub Copilot", "nivel": "N1-N2", "dpa": True, "url": "copilot.github.com"},
        {"nombre": "Grammarly Business", "nivel": "N1-N2", "dpa": True, "url": "grammarly.com"},
    ],
    "herramientas_prohibidas": [
        "ChatGPT (cuenta personal sin DPA)",
        "Midjourney (uso personal)",
        "Herramientas sin DPA firmado",
    ],
    "datos_nivel_3": [
        "datos personales de clientes",
        "datos financieros de la empresa",
        "contratos y acuerdos",
        "datos de empleados",
        "información salarial",
    ],
    "datos_nivel_4": [
        "datos de salud",
        "datos de menores",
        "secretos industriales",
        "código fuente propietario crítico",
        "información de M&A no pública",
    ],
}


# ─── EJERCICIO 1: CLASIFICADOR DE DATOS ──────────────────────────────────────

CONSULTAS_CLASIFICACION = [
    {
        "id": "C-01",
        "descripcion": "Quiero usar Claude para resumir el email de queja de un cliente que incluye su nombre, teléfono y descripción del problema.",
        "datos_incluidos": ["nombre del cliente", "teléfono", "descripción de incidencia"],
    },
    {
        "id": "C-02",
        "descripcion": "Quiero usar IA para generar ideas de titulares para nuestro próximo post de LinkedIn sobre tendencias del sector.",
        "datos_incluidos": ["temática general del sector", "tono de marca"],
    },
    {
        "id": "C-03",
        "descripcion": "Quiero subir el contrato de un cliente importante a ChatGPT para que me lo resuma en puntos clave.",
        "datos_incluidos": ["contrato cliente", "condiciones comerciales", "cláusulas de confidencialidad"],
    },
    {
        "id": "C-04",
        "descripcion": "Quiero usar Copilot para que me ayude a escribir código Python que automatiza la generación de informes de ventas.",
        "datos_incluidos": ["lógica de negocio genérica", "sin datos reales de clientes"],
    },
    {
        "id": "C-05",
        "descripcion": "Quiero pegar el documento de estrategia corporativa 2025-2030 (confidencial) en Claude para que me lo resuma.",
        "datos_incluidos": ["estrategia corporativa", "previsiones financieras", "plan de M&A"],
    },
]

SYSTEM_CLASIFICADOR_DATOS = """Eres el responsable de cumplimiento de IA de la empresa.
Tu trabajo es evaluar consultas de empleados y decirles si pueden usar una herramienta de IA
y con qué condiciones, según la política de datos de la empresa.

Niveles de datos:
- N1 (Público): sin restricción
- N2 (Interno): solo herramientas aprobadas con DPA
- N3 (Confidencial): solo herramientas aprobadas con DPA + anonimizar si es posible
- N4 (Restringido): NUNCA en herramientas externas"""

PROMPT_CLASIFICAR_DATOS = """Evalúa esta solicitud de un empleado:

Solicitud: {descripcion}
Datos que incluiría: {datos}

Herramientas aprobadas en la empresa: Claude (N2-N3), GitHub Copilot (N1-N2), Grammarly (N1-N2)
Herramientas prohibidas: ChatGPT cuenta personal, herramientas sin DPA

Responde SOLO JSON:
{{
  "nivel_datos": "N1/N2/N3/N4",
  "permitido": true/false,
  "herramienta_recomendada": "nombre o null",
  "condiciones": "condiciones de uso o null",
  "alternativa_si_no_permitido": "qué puede hacer el empleado en su lugar",
  "explicacion": "1 frase clara para el empleado"
}}"""


def clasificar_datos_heuristico(consulta):
    """Clasificación básica sin IA."""
    datos = " ".join(consulta["datos_incluidos"]).lower()
    descripcion = consulta["descripcion"].lower()
    nivel = "N1"
    permitido = True
    condicion = None
    herramienta = "Cualquier herramienta aprobada"

    if any(t in datos for t in ["contrato", "estrategia", "m&a", "financiero", "confidencial"]):
        nivel = "N4"
        permitido = False
        herramienta = None
        condicion = "Datos restringidos — NO usar herramientas externas"
    elif any(t in datos for t in ["cliente", "empleado", "personal", "nombre", "teléfono", "email"]):
        nivel = "N3"
        permitido = "chatgpt" not in descripcion
        herramienta = "Claude (con DPA) — anonimizar si es posible"
        condicion = "Usar solo herramientas con DPA firmado"
    elif any(t in datos for t in ["interno", "proceso", "informe de ventas"]):
        nivel = "N2"
        herramienta = "Claude o Copilot"

    return nivel, permitido, herramienta, condicion


def ejercicio_1_clasificador_datos(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 1 — CLASIFICADOR DE DATOS PARA USO CON IA")
    print("=" * 64)

    for consulta in CONSULTAS_CLASIFICACION:
        print(f"\n  [{consulta['id']}] {consulta['descripcion'][:70]}...")
        print(f"  Datos: {', '.join(consulta['datos_incluidos'][:3])}")

        if tiene_api:
            prompt = PROMPT_CLASIFICAR_DATOS.format(
                descripcion=consulta["descripcion"],
                datos=", ".join(consulta["datos_incluidos"])
            )
            resultado = llamar_api(prompt, system=SYSTEM_CLASIFICADOR_DATOS, max_tokens=250)
            try:
                datos = json.loads(resultado)
                icono = "✓" if datos["permitido"] else "✗"
                print(f"  {icono} Nivel: {datos['nivel_datos']} | Permitido: {'Sí' if datos['permitido'] else 'No'}")
                if datos.get("herramienta_recomendada"):
                    print(f"  Herramienta: {datos['herramienta_recomendada']}")
                if datos.get("condiciones"):
                    print(f"  Condiciones: {datos['condiciones']}")
                if not datos["permitido"] and datos.get("alternativa_si_no_permitido"):
                    print(f"  Alternativa: {datos['alternativa_si_no_permitido']}")
                print(f"  Explicación: {datos['explicacion']}")
            except json.JSONDecodeError:
                print(f"  {resultado[:150]}")
        else:
            nivel, permitido, herramienta, condicion = clasificar_datos_heuristico(consulta)
            icono = "✓" if permitido else "✗"
            print(f"  {icono} Nivel: {nivel} | Permitido: {'Sí' if permitido else 'No'}")
            if herramienta:
                print(f"  Herramienta: {herramienta}")
            if condicion:
                print(f"  Condición: {condicion}")


# ─── EJERCICIO 2: VALIDADOR DE OUTPUTS ───────────────────────────────────────

OUTPUTS_PARA_VALIDAR = [
    {
        "id": "OUT-01",
        "tipo": "informe_financiero",
        "contexto": "Informe de resultados Q1 para el consejo de administración",
        "output_ia": "La empresa alcanzó una facturación de 3,2 millones de euros en Q1 2025, superando el objetivo en un 15%. El EBITDA se situó en el 22%, y el número de clientes activos creció un 8% hasta alcanzar los 1.240 clientes. Los mercados de mayor crecimiento fueron el sector industrial (+34%) y el sector servicios (+18%).",
        "datos_reales": {
            "facturacion": 2.8,  # La IA dijo 3.2M cuando son 2.8M
            "objetivo_cumplimiento": "12%",  # La IA dijo 15%
        },
    },
    {
        "id": "OUT-02",
        "tipo": "comunicacion_cliente",
        "contexto": "Email de respuesta a consulta de cliente sobre plazo de entrega",
        "output_ia": "Estimado cliente, le confirmamos que su pedido número PED-8921 será entregado el próximo martes 13 de mayo. El transportista realizará la entrega entre las 9:00 y las 14:00 horas. Para cualquier consulta, puede contactarnos en soporte@empresa.com.",
        "datos_reales": None,  # Sin datos para verificar
    },
    {
        "id": "OUT-03",
        "tipo": "resumen_contrato",
        "contexto": "Resumen de contrato de proveedor para el equipo de compras",
        "output_ia": "El contrato con Proveedor Tech S.L. establece un precio fijo de 2.000€/mes durante 24 meses, con posibilidad de rescisión con 30 días de preaviso sin penalización. Incluye SLA del 99,9% de disponibilidad con penalización del 10% mensual por incumplimiento.",
        "datos_reales": None,
    },
]

PROMPT_VALIDAR_OUTPUT = """Eres el responsable de calidad de contenido IA de la empresa.
Valida este output de un sistema IA antes de que se use.

Tipo de uso: {tipo}
Contexto: {contexto}
Output a validar: {output}
{datos_reales_str}

Evalúa:
1. ¿Hay datos concretos (cifras, fechas, nombres) que deberían verificarse?
2. ¿El tono y contenido es apropiado para el uso indicado?
3. ¿Hay afirmaciones que podrían ser alucinaciones?
4. ¿Hay datos personales o confidenciales que no deberían estar?

Responde JSON:
{{
  "aprobado_para_uso": true/false,
  "nivel_verificacion_requerido": "ninguna/basica/rigurosa",
  "elementos_verificar": ["lista de datos concretos a verificar"],
  "posibles_alucinaciones": ["lista o vacía"],
  "problemas_detectados": ["lista o vacía"],
  "recomendacion": "1 frase de acción para el usuario"
}}"""


def ejercicio_2_validador_outputs(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 2 — VALIDADOR DE OUTPUTS IA")
    print("=" * 64)

    for caso in OUTPUTS_PARA_VALIDAR:
        print(f"\n  [{caso['id']}] Tipo: {caso['tipo']}")
        print(f"  Contexto: {caso['contexto']}")
        print(f"  Output: {caso['output_ia'][:80]}...")

        if tiene_api:
            datos_reales_str = ""
            if caso["datos_reales"]:
                datos_reales_str = f"\nDATOS REALES DISPONIBLES PARA CONTRASTE:\n{json.dumps(caso['datos_reales'], ensure_ascii=False)}"
            prompt = PROMPT_VALIDAR_OUTPUT.format(
                tipo=caso["tipo"],
                contexto=caso["contexto"],
                output=caso["output_ia"],
                datos_reales_str=datos_reales_str
            )
            resultado = llamar_api(prompt, max_tokens=350)
            try:
                datos = json.loads(resultado)
                icono = "✓" if datos["aprobado_para_uso"] else "⚠"
                print(f"  {icono} Aprobado: {'Sí' if datos['aprobado_para_uso'] else 'No'}")
                print(f"  Verificación requerida: {datos['nivel_verificacion_requerido'].upper()}")
                if datos.get("elementos_verificar"):
                    print(f"  Verificar: {', '.join(datos['elementos_verificar'][:3])}")
                if datos.get("posibles_alucinaciones"):
                    print(f"  Posibles alucinaciones: {', '.join(datos['posibles_alucinaciones'][:2])}")
                if datos.get("problemas_detectados"):
                    print(f"  Problemas: {', '.join(datos['problemas_detectados'][:2])}")
                print(f"  Recomendación: {datos['recomendacion']}")
            except json.JSONDecodeError:
                print(f"  {resultado[:200]}")
        else:
            # Validación heurística básica
            output = caso["output_ia"]
            import re
            tiene_cifras = bool(re.search(r'\d+[\.,]\d+|\d{4}', output))
            tiene_fechas = any(m in output.lower() for m in ["enero", "febrero", "marzo", "abril",
                               "mayo", "junio", "julio", "agosto", "2025", "2024"])
            print(f"  Cifras verificables: {'Sí — verificar contra fuentes' if tiene_cifras else 'No detectadas'}")
            print(f"  Fechas verificables: {'Sí — verificar que son correctas' if tiene_fechas else 'No detectadas'}")
            if caso["datos_reales"]:
                print(f"  ALERTA: Hay datos reales disponibles — comparar antes de usar")
            print("  [Configura ANTHROPIC_API_KEY para validación inteligente completa]")


# ─── EJERCICIO 3: GENERADOR DE POLÍTICA CORPORATIVA ──────────────────────────

PERFIL_EMPRESA_PARA_POLITICA = {
    "nombre": "Grupo Médico Norte S.L.",
    "sector": "Salud — clínicas privadas",
    "empleados": 320,
    "datos_sensibles_principales": ["historiales médicos", "datos de pacientes", "información diagnóstica"],
    "herramientas_ia_actuales": ["Microsoft 365 Copilot", "Claude API (en evaluación)"],
    "casos_uso_previstos": [
        "Resúmenes de historiales clínicos para médicos",
        "Gestión de citas y recordatorios",
        "Redacción de informes administrativos",
    ],
    "regulacion_aplicable": ["GDPR", "AI Act", "Ley 41/2002 autonomía del paciente"],
    "preocupaciones_principales": [
        "Confidencialidad de datos de pacientes",
        "Responsabilidad médico-legal",
        "Cumplimiento normativo sanitario",
    ],
}

PROMPT_GENERAR_POLITICA = """Eres un consultor experto en gobernanza de IA para empresas del sector sanitario.
Genera una política de IA generativa adaptada a esta empresa.

Perfil de la empresa:
{perfil}

Genera una política concisa pero completa con estas secciones:
1. ÁMBITO Y PROPÓSITO (2-3 frases)
2. HERRAMIENTAS APROBADAS (tabla o lista)
3. DATOS PROHIBIDOS EN HERRAMIENTAS IA EXTERNAS (lista específica para el sector)
4. USOS PERMITIDOS (casos de uso del sector sanitario)
5. USOS PROHIBIDOS (específicos para el sector)
6. PROCESO DE VALIDACIÓN DE OUTPUTS
7. RESPONSABILIDADES

Tono: profesional, directo, sin jerga innecesaria.
Extensión máxima: 500 palabras."""


def ejercicio_3_generar_politica(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 3 — GENERADOR DE POLÍTICA DE IA CORPORATIVA")
    print("=" * 64)

    print(f"\n  Empresa: {PERFIL_EMPRESA_PARA_POLITICA['nombre']}")
    print(f"  Sector: {PERFIL_EMPRESA_PARA_POLITICA['sector']}")
    print(f"  Casos de uso: {', '.join(PERFIL_EMPRESA_PARA_POLITICA['casos_uso_previstos'][:2])}...")

    if tiene_api:
        prompt = PROMPT_GENERAR_POLITICA.format(
            perfil=json.dumps(PERFIL_EMPRESA_PARA_POLITICA, ensure_ascii=False, indent=2)
        )
        politica = llamar_api(prompt, max_tokens=800)
        print("\n  POLÍTICA DE IA GENERADA:")
        print("  " + "=" * 55)
        for linea in politica.split("\n"):
            print(f"  {linea}")
    else:
        print("\n  POLÍTICA DE IA — PLANTILLA (sector sanitario):")
        print("  " + "=" * 55)
        print("""
  ÁMBITO: Esta política aplica a todos los profesionales y personal
  administrativo del Grupo Médico Norte que utilicen herramientas
  de inteligencia artificial generativa en su actividad.

  HERRAMIENTAS APROBADAS:
  • Microsoft 365 Copilot — datos internos no clínicos (N1-N2)
  • Claude API — con supervisión DPO, solo datos anonimizados (N2)

  DATOS PROHIBIDOS EN IA EXTERNA:
  ✗ Historiales clínicos con identificación del paciente
  ✗ Diagnósticos, tratamientos o evolución de pacientes
  ✗ Datos de menores o personas en situación de vulnerabilidad
  ✗ Resultados de pruebas diagnósticas

  USOS PERMITIDOS:
  ✓ Redacción de documentos administrativos (sin datos de pacientes)
  ✓ Resúmenes de historiales ANONIMIZADOS para investigación
  ✓ Recordatorios de cita (sin información clínica)
  ✓ Formación interna y protocolos genéricos

  RESPONSABILIDADES:
  • DPO: aprueba nuevas herramientas y casos de uso clínicos
  • Médico responsable: valida todo output clínico antes de usar
  • IT: gestiona accesos y auditoría de uso

  Revisión semestral. Aprobado por Dirección General.""")
        print()
        print("  [Configura ANTHROPIC_API_KEY para política personalizada con IA]")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 9.2 — POLÍTICAS DE IA GENERATIVA EN LA EMPRESA")
    print("=" * 64)

    tiene_api = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if tiene_api:
        print(f"  Modelo: {MODELO}")
        print("  Modo: API activa")
    else:
        print("  AVISO: ANTHROPIC_API_KEY no configurada.")
        print("  Modo: Herramientas con lógica de clasificación por reglas")

    ejercicio_1_clasificador_datos(tiene_api)
    ejercicio_2_validador_outputs(tiene_api)
    ejercicio_3_generar_politica(tiene_api)

    print("\n" + "=" * 64)
    print("RESUMEN DEL LAB")
    print("=" * 64)
    print("""
  Herramientas implementadas:
  ✓ Clasificador de datos (N1-N4) para uso con IA
  ✓ Validador de outputs — detecta elementos a verificar
  ✓ Generador de política corporativa adaptada al sector

  Los 3 pilares de una buena política de IA:
    1. CLARIDAD — Qué datos pueden usarse y con qué herramienta
    2. SIMPLICIDAD — Que los empleados la entiendan y sigan
    3. REVISIÓN — Actualizar cada 6 meses o tras incidentes

  Error más común:
    Política muy restrictiva → empleados la ignoran
    Política muy laxa → riesgos sin gestionar
    El equilibrio: permitir el 80% de casos de uso con reglas claras,
    restringir el 20% crítico con proceso de excepción.
""")

    print("[FIN DEL LAB 9.2]")
