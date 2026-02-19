"""
WhatsApp Notification Module – Lux Dashboard
Uses Green API (https://green-api.com) – no rep opt-in required.

One-time admin setup:
  1. Create account at green-api.com
  2. Create an instance and scan QR with any WhatsApp number
  3. Add credentials to secrets.toml and Streamlit Cloud secrets:

secrets.toml structure:
  [green_api]
  instance_id     = "XXXXXXXXXX"
  token           = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  api_url         = "https://XXXX.api.greenapi.com"
  sebastian_phone = "+51XXXXXXXXX"
  ingemar_phone   = "+51XXXXXXXXX"
  emmanuel_phone  = "+51XXXXXXXXX"
"""

import requests
import streamlit as st
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Map rep names (lowercase) to their phone secret key
# Adolfo is the dashboard owner — no notification needed
REP_PHONE_KEYS = {
    "sebastian": "sebastian_phone",
    "ingemar":   "ingemar_phone",
    "emmanuel":  "emmanuel_phone",
}


def _get_green_api_config() -> dict:
    """Retrieve Green API config from st.secrets."""
    try:
        return st.secrets.get("green_api", {})
    except Exception:
        return {}


def _get_rep_phone(rep_name: str) -> Optional[str]:
    """Retrieve phone number for a rep, silently return None if missing."""
    try:
        cfg = _get_green_api_config()
        phone_key = REP_PHONE_KEYS.get(rep_name.lower())
        if not phone_key:
            return None
        phone = cfg.get(phone_key, "")
        # Must be a real number, not a placeholder
        return phone if phone and len(phone) > 5 else None
    except Exception:
        return None


def _is_enabled() -> bool:
    """Check if Green API is configured."""
    try:
        cfg = _get_green_api_config()
        return bool(cfg.get("instance_id") and cfg.get("token") and cfg.get("api_url"))
    except Exception:
        return False


def send_whatsapp(rep_name: str, message: str) -> bool:
    """
    Send a WhatsApp message to a sales rep via Green API.
    Returns True on success, False on failure (silent – never crashes the app).
    """
    if not _is_enabled():
        return False

    phone = _get_rep_phone(rep_name)
    if not phone:
        logger.warning(f"WhatsApp: no phone configured for rep '{rep_name}'. Skipping.")
        return False

    try:
        cfg = _get_green_api_config()
        instance_id = cfg["instance_id"]
        token = cfg["token"]
        api_url = cfg["api_url"].rstrip("/")

        # Green API chatId format: number without '+' followed by @c.us
        chat_id = phone.replace("+", "").replace(" ", "") + "@c.us"

        url = f"{api_url}/waInstance{instance_id}/sendMessage/{token}"
        payload = {"chatId": chat_id, "message": message}

        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200 and response.json().get("idMessage"):
            logger.info(f"WhatsApp sent to {rep_name} ({chat_id})")
            return True
        else:
            logger.warning(f"Green API returned {response.status_code} for {rep_name}: {response.text}")
            return False
    except requests.exceptions.Timeout:
        logger.warning(f"WhatsApp timeout for {rep_name}")
        return False
    except Exception as e:
        logger.warning(f"WhatsApp error for {rep_name}: {e}")
        return False


def notify_new_assignment(
    rep_name: str,
    opp_id: int,
    nombre_negocio: str,
    producto: Optional[str],
    m2: Optional[int],
    siguiente_accion: Optional[str],
    nombre_contacto: Optional[str],
    celular_contacto: Optional[str],
    source: Optional[str],
) -> None:
    """
    Notify a rep that a NEW opportunity has been assigned to them.
    """
    producto_str = producto or "Sin especificar"
    m2_str = f"{m2} m²" if m2 else "Sin especificar"
    accion_str = siguiente_accion or "Pendiente definir"
    contacto_str = nombre_contacto or "Sin nombre"
    celular_str = celular_contacto or "Sin número"
    source_str = source or "-"

    message = (
        f"🎯 *Nueva Oportunidad Asignada* | Lux Dashboard\n\n"
        f"Hola {rep_name}! Se te acaba de asignar una nueva oportunidad.\n\n"
        f"🏢 *Negocio:* {nombre_negocio}\n"
        f"🆔 *ID Oportunidad:* #{opp_id}\n"
        f"📦 *Producto:* {producto_str}\n"
        f"📐 *m² Estimado:* {m2_str}\n"
        f"📣 *Fuente:* {source_str}\n"
        f"👤 *Contacto:* {contacto_str} | {celular_str}\n"
        f"➡️ *Siguiente Acción:* {accion_str}\n\n"
        f"👉 Gestiona esta oportunidad aquí:\n"
        f"https://lux-dashboard.streamlit.app"
    )

    send_whatsapp(rep_name, message)


def notify_reassignment(
    new_rep_name: str,
    prev_rep_name: str,
    opp_id: int,
    nombre_negocio: str,
    producto: Optional[str],
    m2: Optional[int],
    siguiente_accion: Optional[str],
    nombre_contacto: Optional[str],
    celular_contacto: Optional[str],
) -> None:
    """
    Notify a rep that an EXISTING opportunity has been reassigned to them.
    """
    producto_str = producto or "Sin especificar"
    m2_str = f"{m2} m²" if m2 else "Sin especificar"
    accion_str = siguiente_accion or "Pendiente definir"
    contacto_str = nombre_contacto or "Sin nombre"
    celular_str = celular_contacto or "Sin número"

    message = (
        f"🔄 *Reasignación de Oportunidad* | Lux Dashboard\n\n"
        f"Hola {new_rep_name}! La oportunidad #{opp_id} ha sido reasignada a ti"
        f" (antes: {prev_rep_name}).\n\n"
        f"🏢 *Negocio:* {nombre_negocio}\n"
        f"📦 *Producto:* {producto_str}\n"
        f"📐 *m² Estimado:* {m2_str}\n"
        f"👤 *Contacto:* {contacto_str} | {celular_str}\n"
        f"➡️ *Siguiente Acción:* {accion_str}\n\n"
        f"👉 Gestiona esta oportunidad aquí:\n"
        f"https://lux-dashboard.streamlit.app"
    )

    send_whatsapp(new_rep_name, message)
