"""
LAB 7.1 — Anatomía de un Agente IA
=====================================
Objetivo: construir agentes simples desde cero para entender
el bucle percepción-razonamiento-acción en la práctica.

Ejercicios:
  1. Agente de investigación — bucle ReAct con herramientas simuladas
  2. Agente de proceso — onboarding de empleado paso a paso
  3. Comparativa: chatbot vs. agente en la misma tarea

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json

MODELO = "claude-haiku-4-5-20251001"

# ─── CLIENTE ANTHROPIC ────────────────────────────────────────────────────────

def get_client():
    try:
        import anthropic
        return anthropic.Anthropic()
    except Exception:
        return None


def llamar_llm(mensajes, system="", herramientas=None, max_tokens=600):
    client = get_client()
    if not client:
        return None, "sin_cliente"
    try:
        import anthropic
        kwargs = dict(
            model=MODELO,
            max_tokens=max_tokens,
            messages=mensajes,
        )
        if system:
            kwargs["system"] = system
        if herramientas:
            kwargs["tools"] = herramientas
        r = client.messages.create(**kwargs)
        return r, r.stop_reason
    except Exception as e:
        return None, str(e)


# ─── EJERCICIO 1: AGENTE DE INVESTIGACIÓN (ReAct simulado) ───────────────────

# Herramientas simuladas del agente
HERRAMIENTAS_INVESTIGACION = {
    "buscar_empresa": lambda nombre: {
        "nombre": nombre,
        "sede": "Madrid",
        "empleados": 85,
        "fundacion": 2018,
        "sector": "SaaS B2B",
        "facturacion_estimada": "4-8M€",
        "linkedin_seguidores": 1240,
    },
    "buscar_noticias": lambda empresa: [
        f"{empresa} cierra ronda de 3M€ en Serie A (hace 8 meses)",
        f"{empresa} gana el premio CEPYME a empresa innovadora 2024",
        "Sin noticias negativas encontradas",
    ],
    "verificar_registro_mercantil": lambda empresa: {
        "estado": "activa",
        "capital_social": "50.000€",
        "administrador": "Juan García López",
        "ultima_deposicion_cuentas": "2024-03-15",
        "incidencias": [],
    },
}


def ejecutar_herramienta(nombre, parametros):
    """Simula la ejecución de herramientas externas."""
    fn = HERRAMIENTAS_INVESTIGACION.get(nombre)
    if fn:
        param_valor = list(parametros.values())[0] if parametros else ""
        return fn(param_valor)
    return {"error": f"Herramienta '{nombre}' no disponible"}


TOOLS_ANTHROPIC = [
    {
        "name": "buscar_empresa",
        "description": "Busca información general de una empresa: sede, empleados, sector, facturación.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre_empresa": {"type": "string", "description": "Nombre de la empresa a buscar"}
            },
            "required": ["nombre_empresa"],
        },
    },
    {
        "name": "buscar_noticias",
        "description": "Busca noticias recientes sobre una empresa.",
        "input_schema": {
            "type": "object",
            "properties": {
                "empresa": {"type": "string", "description": "Nombre de la empresa"}
            },
            "required": ["empresa"],
        },
    },
    {
        "name": "verificar_registro_mercantil",
        "description": "Verifica el estado registral de una empresa: capital, administrador, incidencias.",
        "input_schema": {
            "type": "object",
            "properties": {
                "empresa": {"type": "string", "description": "Nombre legal de la empresa"}
            },
            "required": ["empresa"],
        },
    },
]

SYSTEM_AGENTE = """Eres un agente de due diligence empresarial.
Dado un nombre de empresa, investígala de forma exhaustiva usando las herramientas disponibles.
Sigue este proceso:
1. Busca información general
2. Busca noticias recientes
3. Verifica el registro mercantil
4. Sintetiza un informe ejecutivo conciso

Llama las herramientas en el orden necesario y finaliza con un informe claro."""


def ejercicio_1_agente_investigacion(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 1 — AGENTE DE INVESTIGACIÓN (bucle ReAct)")
    print("=" * 64)

    empresa_objetivo = "TechFlow Solutions S.L."
    print(f"\n  Objetivo: investigar '{empresa_objetivo}'")

    if not tiene_api:
        # Fallback: simulación del bucle manualmente
        print("\n  [MODO SIMULADO — sin API]")
        print(f"\n  CICLO 1: Percepción → No sé nada de {empresa_objetivo}")
        print("  Razonamiento → Voy a buscar info general")
        print("  Acción → buscar_empresa(nombre_empresa='TechFlow Solutions S.L.')")
        datos = ejecutar_herramienta("buscar_empresa", {"nombre_empresa": empresa_objetivo})
        print(f"  Resultado: {json.dumps(datos, ensure_ascii=False, indent=4)}")

        print("\n  CICLO 2: Percepción → Tengo datos generales")
        print("  Razonamiento → Buscar noticias recientes")
        print("  Acción → buscar_noticias(empresa='TechFlow Solutions S.L.')")
        noticias = ejecutar_herramienta("buscar_noticias", {"empresa": empresa_objetivo})
        for n in noticias:
            print(f"    • {n}")

        print("\n  CICLO 3: Verificar registro mercantil")
        registro = ejecutar_herramienta("verificar_registro_mercantil", {"empresa": empresa_objetivo})
        print(f"  Resultado: {json.dumps(registro, ensure_ascii=False, indent=4)}")

        print("\n  INFORME FINAL (generado por reglas):")
        print(f"  {empresa_objetivo}: empresa activa, sector SaaS, 85 empleados,")
        print("  buenas noticias recientes, sin incidencias mercantiles. RIESGO: BAJO.")
        print("\n  [Configura ANTHROPIC_API_KEY para agente con razonamiento IA real]")
        return

    # Con API: bucle real con tool_use
    mensajes = [{"role": "user", "content": f"Investiga esta empresa para una posible colaboración: {empresa_objetivo}"}]
    ciclo = 0
    max_ciclos = 6

    while ciclo < max_ciclos:
        ciclo += 1
        print(f"\n  --- CICLO {ciclo} ---")

        respuesta, stop_reason = llamar_llm(mensajes, system=SYSTEM_AGENTE,
                                            herramientas=TOOLS_ANTHROPIC, max_tokens=800)
        if respuesta is None:
            print(f"  Error: {stop_reason}")
            break

        # Extraer texto de razonamiento
        for bloque in respuesta.content:
            if hasattr(bloque, "text") and bloque.text:
                print(f"  Razonamiento: {bloque.text[:200]}...")

        if stop_reason == "end_turn":
            # Respuesta final del agente
            for bloque in respuesta.content:
                if hasattr(bloque, "text"):
                    print(f"\n  INFORME FINAL:\n  {bloque.text}")
            break

        if stop_reason == "tool_use":
            # Ejecutar herramientas solicitadas
            tool_results = []
            for bloque in respuesta.content:
                if bloque.type == "tool_use":
                    print(f"  Acción: {bloque.name}({bloque.input})")
                    resultado = ejecutar_herramienta(bloque.name, bloque.input)
                    print(f"  Resultado: {json.dumps(resultado, ensure_ascii=False)[:100]}...")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": bloque.id,
                        "content": json.dumps(resultado, ensure_ascii=False),
                    })

            # Actualizar historial de mensajes
            mensajes.append({"role": "assistant", "content": respuesta.content})
            mensajes.append({"role": "user", "content": tool_results})
        else:
            break


# ─── EJERCICIO 2: AGENTE DE PROCESO — ONBOARDING ─────────────────────────────

PASOS_ONBOARDING = [
    ("crear_cuenta_corporativa", "Crea cuenta de email y accesos en sistemas"),
    ("asignar_equipamiento", "Registra asignación de portátil y periféricos"),
    ("enviar_documentacion", "Envía manual de empleado y políticas"),
    ("programar_reuniones", "Agenda reunión con RRHH y con el equipo"),
    ("configurar_accesos_crm", "Solicita acceso al CRM y herramientas del equipo"),
]

NUEVO_EMPLEADO = {
    "nombre": "Laura Sánchez",
    "cargo": "Account Manager",
    "departamento": "Ventas",
    "fecha_inicio": "2025-05-06",
    "manager": "Roberto Gómez",
}


def simular_paso(nombre_paso, empleado):
    """Simula la ejecución de un paso del proceso de onboarding."""
    simulaciones = {
        "crear_cuenta_corporativa": f"✓ Cuenta laura.sanchez@empresa.com creada",
        "asignar_equipamiento": f"✓ MacBook Pro 14' + Magic Mouse asignados (ticket IT-2891)",
        "enviar_documentacion": f"✓ Email enviado a laura.sanchez@empresa.com con 3 documentos adjuntos",
        "programar_reuniones": f"✓ Reunión RRHH: lunes 10:00 | Reunión equipo: lunes 12:00",
        "configurar_accesos_crm": f"✓ Ticket de acceso HubSpot enviado al administrador IT",
    }
    return simulaciones.get(nombre_paso, f"✓ Paso '{nombre_paso}' completado")


def ejercicio_2_agente_onboarding(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 2 — AGENTE DE PROCESO: ONBOARDING DE EMPLEADO")
    print("=" * 64)

    print(f"\n  Nuevo empleado: {NUEVO_EMPLEADO['nombre']} — {NUEVO_EMPLEADO['cargo']}")
    print(f"  Departamento: {NUEVO_EMPLEADO['departamento']} | Fecha inicio: {NUEVO_EMPLEADO['fecha_inicio']}")
    print(f"\n  Ejecutando {len(PASOS_ONBOARDING)} pasos del proceso:")

    resultados = []
    for paso_id, descripcion in PASOS_ONBOARDING:
        resultado = simular_paso(paso_id, NUEVO_EMPLEADO)
        resultados.append({"paso": paso_id, "descripcion": descripcion, "resultado": resultado})
        print(f"\n  [{paso_id}]")
        print(f"  → {resultado}")

    if tiene_api:
        # El agente genera el email de bienvenida personalizado
        resumen = "\n".join([f"- {r['descripcion']}: {r['resultado']}" for r in resultados])
        prompt = f"""El proceso de onboarding de {NUEVO_EMPLEADO['nombre']} ha completado estos pasos:

{resumen}

Genera un email de bienvenida para enviar al nuevo empleado.
El email debe:
- Ser cálido y profesional
- Mencionar los próximos pasos concretos
- Incluir quién es su manager: {NUEVO_EMPLEADO['manager']}
- Máximo 150 palabras"""

        respuesta, _ = llamar_llm(
            [{"role": "user", "content": prompt}],
            system="Eres el asistente de RRHH de la empresa.",
            max_tokens=400
        )
        if respuesta:
            for bloque in respuesta.content:
                if hasattr(bloque, "text"):
                    print(f"\n  EMAIL DE BIENVENIDA GENERADO:\n  {'─'*50}")
                    for linea in bloque.text.split("\n"):
                        print(f"  {linea}")
    else:
        print("\n  [Configura ANTHROPIC_API_KEY para generación de email personalizado]")
        print("\n  Email de muestra (fallback):")
        print(f"  Bienvenida a {NUEVO_EMPLEADO['nombre']}. Tu cuenta está activa,")
        print(f"  el equipamiento está preparado y tienes reuniones agendadas.")
        print(f"  Tu manager {NUEVO_EMPLEADO['manager']} te espera el {NUEVO_EMPLEADO['fecha_inicio']}.")


# ─── EJERCICIO 3: CHATBOT VS. AGENTE — COMPARATIVA ───────────────────────────

TAREA_COMPARATIVA = "Necesito saber si el proveedor Acme Corp tiene deudas con Hacienda y si es seguro trabajar con ellos."


def ejercicio_3_chatbot_vs_agente(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 3 — CHATBOT vs. AGENTE: MISMA TAREA")
    print("=" * 64)

    print(f"\n  Tarea: '{TAREA_COMPARATIVA}'")

    print("\n  ── MODO CHATBOT (una sola respuesta) ──")
    if tiene_api:
        respuesta, _ = llamar_llm(
            [{"role": "user", "content": TAREA_COMPARATIVA}],
            system="Eres un asistente corporativo. Responde con lo que sabes.",
            max_tokens=300
        )
        if respuesta:
            for bloque in respuesta.content:
                if hasattr(bloque, "text"):
                    print(f"  Chatbot: {bloque.text}")
    else:
        print("  Chatbot: No tengo acceso a bases de datos externas. Para verificar si")
        print("  Acme Corp tiene deudas con Hacienda, deberías consultar el Registro")
        print("  de Deudores de la AEAT directamente o contratar un informe de riesgo.")

    print("\n  ── MODO AGENTE (plan + ejecución) ──")
    print("  Plan del agente:")
    pasos_agente = [
        ("buscar_empresa", "Obtener datos básicos de Acme Corp"),
        ("verificar_registro_mercantil", "Comprobar estado registral y deudas"),
        ("buscar_noticias", "Buscar noticias sobre litigios o problemas"),
        ("SÍNTESIS", "Redactar informe de riesgo con los datos recopilados"),
    ]
    for paso, desc in pasos_agente:
        resultado = ejecutar_herramienta(paso.lower(), {"empresa": "Acme Corp"}) if paso != "SÍNTESIS" else None
        print(f"\n  Paso: {paso}")
        print(f"  → {desc}")
        if resultado:
            if isinstance(resultado, list):
                for item in resultado:
                    print(f"    • {item}")
            elif isinstance(resultado, dict):
                for k, v in list(resultado.items())[:3]:
                    print(f"    {k}: {v}")

    print("\n  CONCLUSIÓN DE LA COMPARATIVA:")
    print("  Chatbot: admite que no puede hacer la tarea → respuesta honesta pero inútil")
    print("  Agente:  ejecuta los pasos necesarios → respuesta accionable con datos reales")
    print("\n  Cuándo usar cada uno:")
    print("  Chatbot → preguntas de conocimiento, redacción, análisis de texto ya disponible")
    print("  Agente  → tareas que requieren consultar sistemas, ejecutar pasos, tomar decisiones")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 7.1 — ANATOMÍA DE UN AGENTE IA")
    print("=" * 64)

    tiene_api = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if tiene_api:
        print(f"  Modelo: {MODELO}")
        print("  Modo: API activa — agente con tool_use real")
    else:
        print("  AVISO: ANTHROPIC_API_KEY no configurada.")
        print("  Modo: Simulación del bucle ReAct con herramientas stub")

    ejercicio_1_agente_investigacion(tiene_api)
    ejercicio_2_agente_onboarding(tiene_api)
    ejercicio_3_chatbot_vs_agente(tiene_api)

    print("\n" + "=" * 64)
    print("RESUMEN DEL LAB")
    print("=" * 64)
    print("""
  Conceptos demostrados:
  ✓ Bucle percepción-razonamiento-acción (ReAct)
  ✓ Agente de proceso: pasos deterministas con IA para síntesis
  ✓ Comparativa chatbot vs. agente en tarea que requiere acción

  Takeaway clave:
    Un agente no es magia — es un LLM en un bucle con herramientas.
    El valor está en las herramientas, no solo en el modelo.
""")

    print("[FIN DEL LAB 7.1]")
