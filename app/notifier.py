"""
WhatsApp Notification Module – Lux Dashboard
Uses CallMeBot free API (https://www.callmebot.com/blog/free-api-whatsapp-messages/)

Each sales rep must opt-in ONCE:
  1. Save this number in their WhatsApp contacts: +34 644 52 74 38  (name it e.g. "CallMeBot")
  2. Send the message:  I allow callmebot to send me messages
     ...to that contact via WhatsApp
  3. They will receive their personal apikey by WhatsApp within seconds.
  4. Add their phone (+51XXXXXXXXX) and apikey to secrets.toml and Streamlit Cloud secrets.

secrets.toml structure needed:
  [whatsapp]
  enabled = true
  sebastian_phone  = "+51XXXXXXXXX"
  sebastian_apikey = "XXXXXX"
  ingemar_phone    = "+51XXXXXXXXX"
  ingemar_apikey   = "XXXXXX"
  emmanuel_phone   = "+51XXXXXXXXX"
  emmanuel_apikey  = "XXXXXX"
  adolfo_phone     = "+51XXXXXXXXX"
  adolfo_apikey    = "XXXXXX"
"""

import requests
import urllib.parse
import streamlit as st
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Map rep names (lowercase) to their secrets keys
REP_KEYS = {
    "sebastian": ("sebastian_phone", "sebastian_apikey"),
    "ingemar":   ("ingemar_phone",   "ingemar_apikey"),
    "emmanuel":  ("emmanuel_phone",  "emmanuel_apikey"),
    "adolfo":    ("adolfo_phone",    "adolfo_apikey"),
}

CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


def _get_rep_credentials(rep_name: str) -> tuple[Optional[str], Optional[str]]:
    """Retrieve phone and apikey for a rep from st.secrets, silently return None if missing."""
    try:
        wapp = st.secrets.get("whatsapp", {})
        phone_key, apikey_key = REP_KEYS[rep_name.lower()]
        phone = wapp.get(phone_key)
        apikey = wapp.get(apikey_key)
        return phone, apikey
    except (KeyError, AttributeError):
        return None, None


def _is_enabled() -> bool:
    """Check if WhatsApp notifications are enabled in secrets."""
    try:
        return st.secrets.get("whatsapp", {}).get("enabled", False)
    except Exception:
        return False


def send_whatsapp(rep_name: str, message: str) -> bool:
    """
    Send a WhatsApp message to a sales rep via CallMeBot.
    Returns True on success, False on failure (silent – never crashes the app).
    """
    if not _is_enabled():
        return False

    phone, apikey = _get_rep_credentials(rep_name)

    if not phone or not apikey:
        logger.warning(f"WhatsApp: no credentials configured for rep '{rep_name}'. Skipping.")
        return False

    try:
        encoded_message = urllib.parse.quote(message)
        url = f"{CALLMEBOT_URL}?phone={phone}&text={encoded_message}&apikey={apikey}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logger.info(f"WhatsApp sent to {rep_name}")
            return True
        else:
            logger.warning(f"CallMeBot returned {response.status_code} for {rep_name}: {response.text}")
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
        f"Ingresa al Dashboard para ver los detalles completos."
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
        f"Ingresa al Dashboard para ver los detalles completos."
    )

    send_whatsapp(new_rep_name, message)
