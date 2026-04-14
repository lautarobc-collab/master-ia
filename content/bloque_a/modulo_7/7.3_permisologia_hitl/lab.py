"""
LAB 7.3 — Permisología y Human-in-the-Loop
============================================
Objetivo: implementar un sistema de permisos y aprobación humana
para agentes IA en entornos corporativos.

Ejercicios:
  1. Motor de permisos — qué puede hacer cada agente
  2. Flujo de aprobación HITL con escalada y timeout
  3. Generador de solicitudes de aprobación comprensibles para humanos

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json
import time
from datetime import datetime
from enum import Enum

MODELO = "claude-haiku-4-5-20251001"


def llamar_api(prompt, system="", max_tokens=500):
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


# ─── EJERCICIO 1: MOTOR DE PERMISOS ──────────────────────────────────────────

class NivelAutonomia(Enum):
    AUTONOMO = 0          # Ejecuta sin preguntar
    NOTIFICA = 1          # Ejecuta y notifica
    APROBACION = 2        # Espera aprobación
    SOLO_HUMANO = 3       # Bloqueado para el agente


MAPA_PERMISOS = {
    "agente_soporte": {
        NivelAutonomia.AUTONOMO: [
            "leer_datos_cliente",
            "consultar_pedido",
            "buscar_conocimiento",
            "clasificar_ticket",
        ],
        NivelAutonomia.NOTIFICA: [
            "registrar_interaccion_crm",
            "enviar_confirmacion_ticket",
            "escalar_ticket",
        ],
        NivelAutonomia.APROBACION: [
            "emitir_reembolso_hasta_100",
            "cambiar_estado_pedido",
            "enviar_email_cliente_personalizado",
        ],
        NivelAutonomia.SOLO_HUMANO: [
            "emitir_reembolso_mas_100",
            "acceder_datos_financieros",
            "modificar_precios",
            "borrar_registros_crm",
            "enviar_email_masivo",
        ],
    },
    "agente_comercial": {
        NivelAutonomia.AUTONOMO: [
            "buscar_contacto",
            "consultar_catalogo",
            "generar_borrador_propuesta",
        ],
        NivelAutonomia.NOTIFICA: [
            "actualizar_etapa_pipeline",
            "programar_recordatorio",
        ],
        NivelAutonomia.APROBACION: [
            "enviar_propuesta_comercial",
            "aplicar_descuento",
        ],
        NivelAutonomia.SOLO_HUMANO: [
            "firmar_contrato",
            "modificar_datos_bancarios_cliente",
            "acceder_datos_otros_comerciales",
        ],
    },
}


def verificar_permiso(agente_id: str, accion: str) -> dict:
    """Verifica si un agente tiene permiso para ejecutar una acción."""
    permisos = MAPA_PERMISOS.get(agente_id)
    if not permisos:
        return {"permitido": False, "nivel": None, "motivo": f"Agente '{agente_id}' no registrado"}

    for nivel, acciones in permisos.items():
        if accion in acciones:
            if nivel == NivelAutonomia.SOLO_HUMANO:
                return {
                    "permitido": False,
                    "nivel": nivel.name,
                    "motivo": f"Acción '{accion}' reservada exclusivamente a humanos",
                }
            return {
                "permitido": True,
                "nivel": nivel.name,
                "requiere_aprobacion": nivel == NivelAutonomia.APROBACION,
                "requiere_notificacion": nivel == NivelAutonomia.NOTIFICA,
            }

    return {
        "permitido": False,
        "nivel": None,
        "motivo": f"Acción '{accion}' no está en la lista de permisos del agente",
    }


ESCENARIOS_PERMISO = [
    ("agente_soporte", "leer_datos_cliente"),
    ("agente_soporte", "emitir_reembolso_hasta_100"),
    ("agente_soporte", "emitir_reembolso_mas_100"),
    ("agente_soporte", "enviar_email_masivo"),
    ("agente_comercial", "enviar_propuesta_comercial"),
    ("agente_comercial", "firmar_contrato"),
    ("agente_ventas_nuevo", "consultar_pedido"),    # agente no registrado
]


def ejercicio_1_motor_permisos(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 1 — MOTOR DE PERMISOS")
    print("=" * 64)

    print("\n  Verificando permisos de agentes:")
    print(f"  {'Agente':<25} {'Acción':<35} {'Resultado'}")
    print("  " + "-" * 80)

    for agente, accion in ESCENARIOS_PERMISO:
        resultado = verificar_permiso(agente, accion)
        if resultado["permitido"]:
            extras = []
            if resultado.get("requiere_aprobacion"):
                extras.append("APROBACIÓN REQUERIDA")
            if resultado.get("requiere_notificacion"):
                extras.append("notifica")
            nivel = resultado["nivel"]
            extra_str = f" ({', '.join(extras)})" if extras else " (autónomo)"
            print(f"  {agente:<25} {accion:<35} ✓ {nivel}{extra_str}")
        else:
            print(f"  {agente:<25} {accion:<35} ✗ BLOQUEADO — {resultado['motivo'][:30]}")

    if not tiene_api:
        print("\n  [Configura ANTHROPIC_API_KEY para análisis de escenarios complejos]")


# ─── EJERCICIO 2: FLUJO HITL CON ESCALADA ────────────────────────────────────

class EstadoAprobacion(Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
    ESCALADO = "ESCALADO"
    TIMEOUT = "TIMEOUT"


COLA_APROBACIONES = []


def solicitar_aprobacion(agente_id: str, accion: str, contexto: dict,
                         aprobador: str, timeout_segundos: int = 300) -> str:
    """Crea una solicitud de aprobación y la añade a la cola."""
    solicitud_id = f"HITL-{datetime.now().strftime('%H%M%S%f')[:10]}"
    solicitud = {
        "id": solicitud_id,
        "agente_id": agente_id,
        "accion": accion,
        "contexto": contexto,
        "aprobador": aprobador,
        "estado": EstadoAprobacion.PENDIENTE,
        "timestamp_creacion": datetime.now().isoformat(),
        "timeout_segundos": timeout_segundos,
    }
    COLA_APROBACIONES.append(solicitud)
    return solicitud_id


def simular_decision_humana(solicitud_id: str, decision: str, comentario: str = ""):
    """Simula la decisión del aprobador humano."""
    for sol in COLA_APROBACIONES:
        if sol["id"] == solicitud_id:
            sol["estado"] = EstadoAprobacion[decision]
            sol["decision_humana"] = decision
            sol["comentario"] = comentario
            sol["timestamp_decision"] = datetime.now().isoformat()
            return True
    return False


CASOS_HITL = [
    {
        "agente": "agente_soporte",
        "accion": "emitir_reembolso_hasta_100",
        "contexto": {
            "cliente": "Ana Martín",
            "email": "ana.martin@cliente.com",
            "importe_reembolso": 89.50,
            "motivo": "Producto defectuoso — confirmado con fotos",
            "historial_cliente": "3 años, 47 pedidos, 2 devoluciones previas",
            "recomendacion_agente": "APROBAR — cliente de alto valor, motivo legítimo",
        },
        "aprobador": "supervisor_soporte@empresa.com",
        "decision_simulada": "APROBADO",
        "comentario_simulado": "Aprobado. Cliente prioritario.",
    },
    {
        "agente": "agente_comercial",
        "accion": "aplicar_descuento",
        "contexto": {
            "cliente": "Beta Solutions",
            "contacto": "Carlos Ruiz (CEO)",
            "descuento_solicitado": "15%",
            "valor_contrato": 120000,
            "motivo": "Competencia ha ofrecido precio similar",
            "margen_afectado": "Margen pasa del 40% al 29%",
            "recomendacion_agente": "APROBAR con descuento máximo del 10% como contraoferta",
        },
        "aprobador": "director_ventas@empresa.com",
        "decision_simulada": "APROBADO",
        "comentario_simulado": "Aprobado 10%. No más. Incluir cláusula de permanencia 2 años.",
    },
    {
        "agente": "agente_soporte",
        "accion": "cambiar_estado_pedido",
        "contexto": {
            "pedido": "PED-98765",
            "cambio": "De 'enviado' a 'cancelado'",
            "motivo": "Cliente solicita cancelación por error en dirección de entrega",
            "pedido_ya_en_transito": True,
            "coste_cancelacion": "35€ (cargo transportista)",
            "recomendacion_agente": "ESCALAR — pedido en tránsito, cancelación costosa",
        },
        "aprobador": "supervisor_logistica@empresa.com",
        "decision_simulada": "RECHAZADO",
        "comentario_simulado": "No cancelar. Contactar al cliente para redirigir envío.",
    },
]


def ejercicio_2_flujo_hitl(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 2 — FLUJO DE APROBACIÓN HITL")
    print("=" * 64)

    for caso in CASOS_HITL:
        print(f"\n  Agente: {caso['agente']} | Acción: {caso['accion']}")

        # Verificar permiso
        perm = verificar_permiso(caso["agente"], caso["accion"])
        if not perm["permitido"]:
            print(f"  ✗ Bloqueado: {perm['motivo']}")
            continue

        if not perm.get("requiere_aprobacion"):
            print(f"  ✓ Ejecutado autónomamente (nivel: {perm['nivel']})")
            continue

        # Crear solicitud de aprobación
        sol_id = solicitar_aprobacion(
            caso["agente"], caso["accion"], caso["contexto"],
            caso["aprobador"], timeout_segundos=30
        )
        print(f"  Solicitud creada: {sol_id}")
        print(f"  Aprobador: {caso['aprobador']}")
        print(f"  Contexto:")
        for k, v in caso["contexto"].items():
            if k != "recomendacion_agente":
                print(f"    {k}: {v}")
        print(f"  IA recomienda: {caso['contexto']['recomendacion_agente']}")

        # Simular decisión humana
        simular_decision_humana(sol_id, caso["decision_simulada"], caso["comentario_simulado"])
        decision = caso["decision_simulada"]
        comentario = caso["comentario_simulado"]

        icono = "✓" if decision == "APROBADO" else "✗" if decision == "RECHAZADO" else "→"
        print(f"\n  Decisión humana: {icono} {decision}")
        print(f"  Comentario: {comentario}")

        # El agente genera el siguiente paso con IA
        if tiene_api:
            prompt = f"""El agente solicitó: {caso['accion']}
Decisión del aprobador: {decision}
Comentario: {comentario}
Contexto: {json.dumps(caso['contexto'], ensure_ascii=False)}

Genera en 1-2 frases la comunicación al cliente o la acción de seguimiento."""
            siguiente_paso = llamar_api(prompt, max_tokens=150)
            print(f"  Siguiente paso IA: {siguiente_paso}")
        else:
            if decision == "APROBADO":
                print("  Siguiente paso: ejecutar acción aprobada y notificar al cliente")
            else:
                print("  Siguiente paso: notificar al agente del rechazo para aplicar alternativa")


# ─── EJERCICIO 3: GENERADOR DE SOLICITUDES HITL ──────────────────────────────

SITUACIONES_COMPLEJAS = [
    {
        "situacion": "Un cliente lleva 3 meses sin pagar y tiene una deuda de 8.400€. El agente quiere bloquear su acceso al servicio.",
        "agente": "agente_soporte",
        "accion_propuesta": "bloquear_acceso_cliente",
    },
    {
        "situacion": "Un proveedor pide ampliar el plazo de entrega de 30 a 60 días para un pedido de 50.000€. El agente considera que afecta a 3 proyectos de clientes activos.",
        "agente": "agente_compras",
        "accion_propuesta": "modificar_condiciones_proveedor",
    },
]

PROMPT_GENERAR_SOLICITUD_HITL = """Eres el sistema de gestión de aprobaciones de una empresa.
Un agente IA necesita aprobación humana para una acción de alto impacto.
Genera una solicitud de aprobación clara y útil para el aprobador humano.

Situación: {situacion}
Agente: {agente}
Acción propuesta: {accion_propuesta}

La solicitud debe incluir:
1. Resumen de la situación (2-3 frases)
2. Qué pasará si se APRUEBA (consecuencias concretas)
3. Qué pasará si se RECHAZA (alternativa)
4. Recomendación del sistema (basada en buenas prácticas)
5. Urgencia: ALTA/MEDIA/BAJA

Formato: texto claro para un manager sin contexto técnico."""


def ejercicio_3_generador_solicitudes(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 3 — GENERADOR DE SOLICITUDES HITL COMPRENSIBLES")
    print("=" * 64)

    for caso in SITUACIONES_COMPLEJAS:
        print(f"\n  Situación: {caso['situacion'][:70]}...")
        print(f"  Acción propuesta: {caso['accion_propuesta']}")
        print()

        if tiene_api:
            prompt = PROMPT_GENERAR_SOLICITUD_HITL.format(**caso)
            solicitud = llamar_api(prompt, max_tokens=400)
            print("  SOLICITUD GENERADA:")
            print("  " + "─" * 50)
            for linea in solicitud.split("\n"):
                print(f"  {linea}")
        else:
            print("  [Solicitud generada por fallback]")
            print(f"  SOLICITUD: El agente {caso['agente']} solicita ejecutar '{caso['accion_propuesta']}'.")
            print(f"  Situación: {caso['situacion']}")
            print("  Por favor, revise y apruebe o rechace esta acción.")
            print("  Urgencia: MEDIA")
            print("  [Configura ANTHROPIC_API_KEY para solicitudes comprensibles generadas por IA]")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 7.3 — PERMISOLOGÍA Y HUMAN-IN-THE-LOOP")
    print("=" * 64)

    tiene_api = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if tiene_api:
        print(f"  Modelo: {MODELO}")
        print("  Modo: API activa")
    else:
        print("  AVISO: ANTHROPIC_API_KEY no configurada.")
        print("  Modo: Lógica de permisos sin generación IA")

    ejercicio_1_motor_permisos(tiene_api)
    ejercicio_2_flujo_hitl(tiene_api)
    ejercicio_3_generador_solicitudes(tiene_api)

    print("\n" + "=" * 64)
    print("RESUMEN DEL LAB")
    print("=" * 64)
    print("""
  Sistemas implementados:
  ✓ Motor de permisos con 4 niveles de autonomía
  ✓ Cola de aprobaciones HITL con simulación de decisión humana
  ✓ Generador de solicitudes comprensibles para aprobadores

  Los cuatro niveles:
    0 — Autónomo   → ejecuta sin preguntar
    1 — Notifica   → ejecuta y avisa
    2 — Aprobación → espera confirmación humana
    3 — Solo humano → bloqueado para el agente

  Regla de oro:
    La irreversibilidad de la acción determina el nivel de control.
    Si borrar es definitivo, preguntar es obligatorio.
""")

    print("[FIN DEL LAB 7.3]")
