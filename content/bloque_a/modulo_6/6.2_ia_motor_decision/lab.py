"""
LAB 6.2 — IA como Motor de Decisión
=====================================
Objetivo: construir un motor de decisión en tres capas:
  reglas duras → scoring numérico → razonamiento IA.

Ejercicios:
  1. Scoring automatizado de solicitudes de crédito
  2. Motor de aprobación/rechazo de devoluciones
  3. Árbol de decisión IA para incorporación de proveedores

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json

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


# ─── EJERCICIO 1: SCORING DE CRÉDITO ─────────────────────────────────────────

SOLICITUDES_CREDITO = [
    {
        "id": "SOL-001",
        "nombre": "Distribuciones García S.L.",
        "anos_cliente": 5,
        "ingresos_anuales": 280000,
        "deuda_total": 42000,
        "pagos_a_tiempo": 48,
        "total_pagos": 50,
        "impago_reciente": False,
        "cliente_premium": True,
        "importe_solicitado": 40000,
        "limite_credito": 100000,
        "sector": "distribucion",
    },
    {
        "id": "SOL-002",
        "nombre": "Startup Tech S.L.",
        "anos_cliente": 0.5,
        "ingresos_anuales": 60000,
        "deuda_total": 55000,
        "pagos_a_tiempo": 3,
        "total_pagos": 5,
        "impago_reciente": True,
        "cliente_premium": False,
        "importe_solicitado": 30000,
        "limite_credito": 40000,
        "sector": "tecnologia",
    },
    {
        "id": "SOL-003",
        "nombre": "Clínica Wellness S.L.",
        "anos_cliente": 3,
        "ingresos_anuales": 150000,
        "deuda_total": 30000,
        "pagos_a_tiempo": 28,
        "total_pagos": 32,
        "impago_reciente": False,
        "cliente_premium": False,
        "importe_solicitado": 25000,
        "limite_credito": 50000,
        "sector": "salud",
    },
]

RIESGO_SECTOR = {
    "tecnologia": 0.7,
    "salud": 0.9,
    "distribucion": 0.85,
    "hosteleria": 0.55,
    "construccion": 0.60,
    "otro": 0.75,
}


def calcular_score_credito(sol):
    score = 0.0
    # Antigüedad (máx 20 pts)
    score += min(sol["anos_cliente"] * 4, 20)
    # Ratio deuda/ingresos (máx 25 pts)
    ratio = sol["deuda_total"] / max(sol["ingresos_anuales"], 1)
    score += max(0.0, (1.0 - ratio) * 25)
    # Historial de pagos (máx 25 pts)
    if sol["total_pagos"] > 0:
        score += (sol["pagos_a_tiempo"] / sol["total_pagos"]) * 25
    # Sector (máx 15 pts)
    factor_sector = RIESGO_SECTOR.get(sol["sector"], 0.75)
    score += factor_sector * 15
    # Importe vs. límite (máx 15 pts)
    ratio_importe = sol["importe_solicitado"] / max(sol["limite_credito"], 1)
    score += max(0.0, (1.0 - ratio_importe) * 15)
    # Ajustes
    if sol["impago_reciente"]:
        score -= 20
    if sol["cliente_premium"]:
        score += 10
    return round(max(0.0, min(100.0, score)), 1)


def decidir_credito(sol, score):
    """Aplica el semáforo de decisión."""
    if score > 75:
        return "APROBADO", "Aprobación automática por score alto"
    elif score < 30:
        return "RECHAZADO", "Rechazo automático por score insuficiente"
    else:
        return "REVISION_IA", "Score en zona gris — requiere análisis IA"


PROMPT_CREDITO_IA = """Eres el analista de riesgo de crédito de una empresa de distribución.
Evalúa esta solicitud que ha quedado en zona gris del scoring automático.

Solicitud ID: {id}
Empresa: {nombre}
Score automático: {score}/100
Sector: {sector}
Años como cliente: {anos_cliente}
Ingresos anuales: {ingresos_anuales}€
Deuda actual: {deuda_total}€ ({ratio_deuda:.0%} de ingresos)
Historial pagos: {pagos_a_tiempo}/{total_pagos} a tiempo
Importe solicitado: {importe_solicitado}€
Impago reciente: {impago_reciente}
Cliente premium: {cliente_premium}

Responde SOLO en este JSON:
{{
  "decision": "APROBAR o RECHAZAR",
  "confianza": "alta/media/baja",
  "justificacion": "1-2 frases",
  "condiciones": "condición opcional si se aprueba con reservas, o null",
  "escalar_humano": true/false
}}"""


def ejercicio_1_scoring_credito(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 1 — SCORING AUTOMATIZADO DE CRÉDITO")
    print("=" * 64)

    for sol in SOLICITUDES_CREDITO:
        score = calcular_score_credito(sol)
        decision, motivo = decidir_credito(sol, score)
        print(f"\n  [{sol['id']}] {sol['nombre']}")
        print(f"  Score: {score}/100  →  {decision}")
        print(f"  Motivo: {motivo}")

        if decision == "REVISION_IA":
            if tiene_api:
                ratio_deuda = sol["deuda_total"] / max(sol["ingresos_anuales"], 1)
                prompt = PROMPT_CREDITO_IA.format(**sol, score=score,
                                                  ratio_deuda=ratio_deuda)
                respuesta = llamar_api(prompt)
                try:
                    datos = json.loads(respuesta)
                    print(f"  IA → {datos['decision']} (confianza: {datos['confianza']})")
                    print(f"  Justificación: {datos['justificacion']}")
                    if datos.get("condiciones"):
                        print(f"  Condiciones: {datos['condiciones']}")
                    if datos.get("escalar_humano"):
                        print("  ⚑ Caso escalado a analista humano")
                except json.JSONDecodeError:
                    print(f"  IA → {respuesta}")
            else:
                print("  IA → [Configura ANTHROPIC_API_KEY para análisis IA]")


# ─── EJERCICIO 2: MOTOR DE DEVOLUCIONES ──────────────────────────────────────

CASOS_DEVOLUCION = [
    {
        "id": "DEV-101",
        "cliente": "María López",
        "anos_cliente": 3,
        "pedidos_totales": 47,
        "devoluciones_previas": 2,
        "dias_desde_entrega": 38,
        "plazo_politica": 30,
        "motivo": "El producto llegó dañado, tardé en abrir el paquete por viaje",
        "evidencia": "foto adjunta del embalaje roto",
        "importe": 89.50,
        "producto": "Zapatillas deportivas premium",
    },
    {
        "id": "DEV-102",
        "cliente": "Carlos Ruiz",
        "anos_cliente": 0.2,
        "pedidos_totales": 3,
        "devoluciones_previas": 2,
        "dias_desde_entrega": 15,
        "plazo_politica": 30,
        "motivo": "No me gusta el color aunque en la web se veía diferente",
        "evidencia": "ninguna",
        "importe": 45.00,
        "producto": "Camiseta casual",
    },
    {
        "id": "DEV-103",
        "cliente": "Ana Martín",
        "anos_cliente": 7,
        "pedidos_totales": 132,
        "devoluciones_previas": 4,
        "dias_desde_entrega": 5,
        "plazo_politica": 30,
        "motivo": "Talla incorrecta, pedí M y llegó L",
        "evidencia": "foto etiqueta y albarán",
        "importe": 120.00,
        "producto": "Abrigo de invierno",
    },
]

SYSTEM_DEVOLUCION = """Eres el motor de decisión de devoluciones de una tienda online.
Política:
- Plazo estándar: 30 días desde entrega.
- Defectos de fábrica: siempre aprobado hasta 90 días.
- Errores de la empresa (talla/modelo incorrecto): siempre aprobado.
- Clientes con >5 devoluciones/año: revisión estricta.
- Casos fuera de plazo: evaluar antigüedad del cliente y evidencia."""

PROMPT_DEVOLUCION = """Caso de devolución {id}:
Cliente: {cliente} ({anos_cliente} años, {pedidos_totales} pedidos, {devoluciones_previas} devoluciones previas)
Producto: {producto} — {importe}€
Días desde entrega: {dias_desde_entrega} (plazo política: {plazo_politica} días)
Motivo: {motivo}
Evidencia: {evidencia}

Decide y devuelve SOLO JSON:
{{
  "decision": "APROBAR/RECHAZAR/ESCALAR",
  "tipo_resolucion": "devolucion_completa/cambio/cupon/ninguna",
  "justificacion": "max 2 frases",
  "mensaje_cliente": "mensaje empático para enviar al cliente (max 3 frases)"
}}"""


def ejercicio_2_motor_devoluciones(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 2 — MOTOR DE APROBACIÓN DE DEVOLUCIONES")
    print("=" * 64)

    for caso in CASOS_DEVOLUCION:
        print(f"\n  [{caso['id']}] {caso['cliente']} — {caso['producto']}")
        print(f"  Días: {caso['dias_desde_entrega']} / Plazo: {caso['plazo_politica']}")
        print(f"  Motivo: {caso['motivo']}")

        if tiene_api:
            prompt = PROMPT_DEVOLUCION.format(**caso)
            respuesta = llamar_api(prompt, system=SYSTEM_DEVOLUCION, max_tokens=400)
            try:
                datos = json.loads(respuesta)
                print(f"  → DECISIÓN: {datos['decision']} ({datos['tipo_resolucion']})")
                print(f"  → Justif.: {datos['justificacion']}")
                print(f"  → Msg cliente: {datos['mensaje_cliente']}")
            except json.JSONDecodeError:
                print(f"  → {respuesta}")
        else:
            # Fallback con reglas básicas
            if caso["dias_desde_entrega"] <= caso["plazo_politica"]:
                decision = "APROBAR (dentro de plazo)"
            elif "dañado" in caso["motivo"].lower() or "incorrecto" in caso["motivo"].lower():
                decision = "APROBAR (defecto/error empresa)"
            else:
                decision = "REVISAR (fuera de plazo)"
            print(f"  → Regla básica: {decision}")
            print("  [Configura ANTHROPIC_API_KEY para análisis completo]")


# ─── EJERCICIO 3: HOMOLOGACIÓN DE PROVEEDORES ─────────────────────────────────

PROVEEDORES = [
    {
        "nombre": "CloudServ Solutions S.L.",
        "pais": "España",
        "anos_mercado": 4,
        "certificaciones": ["ISO 27001", "SOC 2"],
        "referencias": 12,
        "precio_oferta": 85000,
        "presupuesto_maximo": 100000,
        "datos_personales_involucrados": True,
        "datos_en_cloud_extranjera": False,
        "incidentes_seguridad": 0,
        "capacidad_sla_99": True,
        "notas": "Proveedor local con buenas referencias en banca y seguros",
    },
    {
        "nombre": "CheapIT Global Inc.",
        "pais": "India",
        "anos_mercado": 2,
        "certificaciones": [],
        "referencias": 3,
        "precio_oferta": 32000,
        "presupuesto_maximo": 100000,
        "datos_personales_involucrados": True,
        "datos_en_cloud_extranjera": True,
        "incidentes_segurentes": 1,
        "incidentes_seguridad": 1,
        "capacidad_sla_99": False,
        "notas": "Sin certificaciones, precio muy bajo, datos en servidores EEUU",
    },
]

SYSTEM_PROVEEDOR = """Eres el responsable de homologación de proveedores tecnológicos.
Criterios obligatorios (TODOS deben cumplirse):
  1. Si maneja datos personales → ISO 27001 o SOC 2 obligatorio
  2. Si datos en cloud extranjera → cláusulas GDPR y DPA firmado
  3. Cero incidentes graves de seguridad en los últimos 2 años
  4. SLA 99% si es servicio crítico
Criterios deseables: referencias, años en mercado, precio."""

PROMPT_PROVEEDOR = """Solicitud de homologación:
Proveedor: {nombre} ({pais}, {anos_mercado} años en mercado)
Certificaciones: {certificaciones}
Referencias comprobadas: {referencias}
Precio oferta: {precio_oferta}€ (presupuesto máximo: {presupuesto_maximo}€)
Maneja datos personales: {datos_personales_involucrados}
Datos en cloud extranjera: {datos_en_cloud_extranjera}
Incidentes de seguridad: {incidentes_seguridad}
Capacidad SLA 99%: {capacidad_sla_99}
Notas: {notas}

Evalúa y devuelve SOLO JSON:
{{
  "decision": "HOMOLOGAR/RECHAZAR/CONDICIONAL",
  "bloqueantes": ["lista de criterios obligatorios incumplidos, puede ser vacía"],
  "puntuacion_cualitativa": 0-100,
  "condiciones_si_aplica": "requisitos para homologación condicional o null",
  "resumen_ejecutivo": "1 frase para el comité de compras"
}}"""


def ejercicio_3_homologacion_proveedores(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 3 — ÁRBOL DE DECISIÓN: HOMOLOGACIÓN DE PROVEEDORES")
    print("=" * 64)

    for prov in PROVEEDORES:
        print(f"\n  Proveedor: {prov['nombre']} ({prov['pais']})")
        print(f"  Certifs.: {prov['certificaciones'] or 'Ninguna'}")
        print(f"  Precio: {prov['precio_oferta']:,}€")

        if tiene_api:
            prompt = PROMPT_PROVEEDOR.format(**prov)
            respuesta = llamar_api(prompt, system=SYSTEM_PROVEEDOR, max_tokens=450)
            try:
                datos = json.loads(respuesta)
                print(f"  → DECISIÓN: {datos['decision']}")
                if datos["bloqueantes"]:
                    print(f"  → Bloqueantes: {', '.join(datos['bloqueantes'])}")
                print(f"  → Score cualitativo: {datos['puntuacion_cualitativa']}/100")
                if datos.get("condiciones_si_aplica"):
                    print(f"  → Condiciones: {datos['condiciones_si_aplica']}")
                print(f"  → Comité: {datos['resumen_ejecutivo']}")
            except json.JSONDecodeError:
                print(f"  → {respuesta}")
        else:
            # Fallback: reglas duras sin IA
            bloqueantes = []
            if prov["datos_personales_involucrados"] and not prov["certificaciones"]:
                bloqueantes.append("sin certificación de seguridad")
            if prov.get("incidentes_seguridad", 0) > 0:
                bloqueantes.append("incidentes de seguridad recientes")
            if bloqueantes:
                print(f"  → Regla básica: RECHAZAR — {', '.join(bloqueantes)}")
            else:
                print("  → Regla básica: CANDIDATO VÁLIDO — análisis IA necesario")
            print("  [Configura ANTHROPIC_API_KEY para evaluación completa]")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 6.2 — IA COMO MOTOR DE DECISIÓN")
    print("=" * 64)

    tiene_api = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if tiene_api:
        print(f"  Modelo: {MODELO}")
        print("  Modo: API activa — ejercicios con análisis IA completo")
    else:
        print("  AVISO: ANTHROPIC_API_KEY no configurada.")
        print("  Modo: Fallback con reglas deterministas")

    ejercicio_1_scoring_credito(tiene_api)
    ejercicio_2_motor_devoluciones(tiene_api)
    ejercicio_3_homologacion_proveedores(tiene_api)

    print("\n" + "=" * 64)
    print("RESUMEN DEL LAB")
    print("=" * 64)
    print("""
  Lo que hemos construido:
  ✓ Scoring numérico multicriteria (Ej. 1)
  ✓ Motor de aprobación/rechazo con política corporativa (Ej. 2)
  ✓ Árbol de decisión con criterios obligatorios y deseables (Ej. 3)

  Principio clave:
    Reglas duras → Scoring → IA en zona gris → Humano en casos límite
    Nunca delegar a la IA lo que debe ser una regla inmutable.
""")

    print("[FIN DEL LAB 6.2]")
