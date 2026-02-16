
import os
import streamlit as st
from supabase import create_client, Client
from datetime import date, datetime
import random
from typing import Optional, List, Dict, Any
from pathlib import Path

# --- Configuration ---
# Uses st.secrets for production (Streamlit Cloud)
# Uses os.environ or .env for local development (if not using st.secrets locally)

SALES_REPS = ["Emmanuel", "Sebastian", "Ingemar", "Adolfo"]
SALES_WEIGHTS = [0.40, 0.30, 0.20, 0.10]

@st.cache_resource
def init_connection():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"❌ Error connecting to Supabase: {e}")
        st.stop()

# --- Database Initialization ---
# Tables must be created in Supabase SQL Editor.
# This function is a placeholder or can run SQL if enabled (usually not recommended for client)

# --- CRUD Operations ---

def get_or_create_business(nombre: str, tipo_negocio: str, direccion: str) -> int:
    """
    Get existing business ID or create new one.
    Retries to find business by nombre + direccion (case insensitive).
    Returns: business_id
    """
    supabase = init_connection()

    # 1. Search existing
    # Note: Supabase/Postgres ILIKE is case-insensitive
    try:
        response = supabase.table("businesses").select("id")\
            .ilike("nombre", nombre)\
            .ilike("direccion", direccion)\
            .execute()
        
        if response.data:
            # Update type if changed
            business_id = response.data[0]['id']
            supabase.table("businesses").update({
                "tipo_negocio": tipo_negocio,
                "updated_at": "now()"
            }).eq("id", business_id).execute()
            return business_id
        
        # 2. Create new
        new_business = {
            "nombre": nombre,
            "tipo_negocio": tipo_negocio,
            "direccion": direccion
        }
        response = supabase.table("businesses").insert(new_business).execute()
        return response.data[0]['id']

    except Exception as e:
        st.error(f"Database Error: {e}")
        raise e

def create_visita(nombre: str, tipo_negocio: str, direccion: str, 
                  fecha: date, semana: str, notas: Optional[str] = None) -> int:
    """Create new visit record in Supabase"""
    supabase = init_connection()
    business_id = get_or_create_business(nombre, tipo_negocio, direccion)
    
    new_visita = {
        "business_id": business_id,
        "fecha": fecha.isoformat(),
        "semana": semana,
        "notas": notas
    }
    
    response = supabase.table("visitas").insert(new_visita).execute()
    return response.data[0]['id']

def update_visita(visita_id: int, nombre: str, tipo_negocio: str, direccion: str,
                  fecha: date, semana: str, notas: Optional[str] = None) -> None:
    """Update an existing visit record"""
    supabase = init_connection()
    # Update business info first (could change links, but keeping simple for now)
    # Ideally should update business record if details changed
    business_id = get_or_create_business(nombre, tipo_negocio, direccion)
    
    update_data = {
        "business_id": business_id,
        "fecha": fecha.isoformat(),
        "semana": semana,
        "notas": notas,
        "updated_at": "now()"
    }
    
    supabase.table("visitas").update(update_data).eq("id", visita_id).execute()

def delete_visita(visita_id: int) -> None:
    """Delete a visit record by ID"""
    supabase = init_connection()
    
    # First, decouple any linked opportunities (set visita_id to NULL)
    # This prevents foreign key constraint errors
    supabase.table("oportunidades").update({"visita_id": None}).eq("visita_id", visita_id).execute()
    
    # Now safe to delete the visit
    supabase.table("visitas").delete().eq("id", visita_id).execute()

def create_oportunidad(nombre: str, tipo_negocio: str, direccion: str,
                       fecha_contacto: date, semana: str, m2_estimado: Optional[int] = None,
                       producto_interes: Optional[str] = None, siguiente_accion: Optional[str] = None,
                       visita_id: Optional[int] = None, source: Optional[str] = None,
                       nombre_contacto: Optional[str] = None, cargo_contacto: Optional[str] = None, 
                       celular_contacto: Optional[str] = None) -> int:
    """Create new opportunity record in Supabase"""
    supabase = init_connection()
    business_id = get_or_create_business(nombre, tipo_negocio, direccion)
    
    # Assign sales rep automatically
    assigned_to = random.choices(SALES_REPS, weights=SALES_WEIGHTS, k=1)[0]
    
    new_opp = {
        "business_id": business_id,
        "fecha_contacto": fecha_contacto.isoformat(),
        "semana": semana,
        "m2_estimado": m2_estimado,
        "producto_interes": producto_interes,
        "siguiente_accion": siguiente_accion,
        "visita_id": visita_id,
        "estado": "Activa",
        "source": source,
        "nombre_contacto": nombre_contacto,
        "cargo_contacto": cargo_contacto,
        "celular_contacto": celular_contacto,
        "asignado_a": assigned_to,
    }
    
    response = supabase.table("oportunidades").insert(new_opp).execute()
    return response.data[0]['id']

def update_oportunidad(oportunidad_id: int, nombre: str, tipo_negocio: str, direccion: str,
                       fecha_contacto: date, semana: str, m2_estimado: Optional[int] = None,
                       producto_interes: Optional[str] = None, siguiente_accion: Optional[str] = None,
                       source: Optional[str] = None,
                       nombre_contacto: Optional[str] = None, cargo_contacto: Optional[str] = None,
                       celular_contacto: Optional[str] = None,
                       asignado_a: Optional[str] = None) -> None:
    """Update existing opportunity"""
    supabase = init_connection()
    business_id = get_or_create_business(nombre, tipo_negocio, direccion)
    
    update_data = {
        "business_id": business_id,
        "fecha_contacto": fecha_contacto.isoformat(),
        "semana": semana,
        "m2_estimado": m2_estimado,
        "producto_interes": producto_interes,
        "siguiente_accion": siguiente_accion,
        "source": source,
        "nombre_contacto": nombre_contacto,
        "cargo_contacto": cargo_contacto,
        "celular_contacto": celular_contacto,
        "updated_at": "now()"
    }

    if asignado_a:
        update_data["asignado_a"] = asignado_a
    # If asignado_a is explicitly passed as None or empty, we generally don't want to clear it 
    # unless that's intended. Here we only update if a value is provided. 
    # To prevent accidental overwrites, we rely on the callers to pass the existing value if they want to keep it,
    # or a new value if they want to change it.
    
    supabase.table("oportunidades").update(update_data).eq("id", oportunidad_id).execute()

def delete_oportunidad(oportunidad_id: int) -> None:
    """Delete opportunity"""
    supabase = init_connection()
    supabase.table("oportunidades").delete().eq("id", oportunidad_id).execute()

def create_venta(venta_id: str, nombre: str, tipo_negocio: str, direccion: str,
                 fecha_cierre: date, semana: str, m2_real: int, producto: str,
                 monto_soles: float, fecha_instalacion: Optional[date] = None,
                 oportunidad_id: Optional[int] = None) -> int:
    """Create new sale record in Supabase"""
    supabase = init_connection()
    business_id = get_or_create_business(nombre, tipo_negocio, direccion)
    
    new_sale = {
        "venta_id": venta_id,
        "business_id": business_id,
        "fecha_cierre": fecha_cierre.isoformat(),
        "semana": semana,
        "m2_real": m2_real,
        "producto": producto,
        "monto_soles": monto_soles,
        "fecha_instalacion": fecha_instalacion.isoformat() if fecha_instalacion else None,
        "oportunidad_id": oportunidad_id,
        "estado": "Cerrada"
    }
    
    response = supabase.table("ventas").insert(new_sale).execute()
    
    # Mark opportunity as converted
    if oportunidad_id:
        supabase.table("oportunidades").update({
            "estado": "Convertida",
            "updated_at": "now()"
        }).eq("id", oportunidad_id).execute()
        
    return response.data[0]['id']

# --- Getters ---

def get_visitas_by_period(start_date: date, end_date: date) -> List[Dict[str, Any]]:
    """Get visits within date range with business details"""
    supabase = init_connection()
    
    # Perform a join using Supabase syntax
    # select (*, businesses(*))
    response = supabase.table("visitas")\
        .select("*, businesses(nombre, tipo_negocio, direccion)")\
        .gte("fecha", start_date.isoformat())\
        .lte("fecha", end_date.isoformat())\
        .order("fecha", desc=True)\
        .execute()
    
    # Flatten the result for the frontend
    results = []
    for item in response.data:
        flat = item.copy()
        if item.get('businesses'):
            flat['nombre'] = item['businesses']['nombre']
            flat['tipo_negocio'] = item['businesses']['tipo_negocio']
            flat['direccion'] = item['businesses']['direccion']
        results.append(flat)
        
    return results

def get_oportunidades_activas() -> List[Dict[str, Any]]:
    """Get active opportunities"""
    supabase = init_connection()
    
    response = supabase.table("oportunidades")\
        .select("*, businesses(nombre, tipo_negocio, direccion)")\
        .eq("estado", "Activa")\
        .order("fecha_contacto", desc=True)\
        .execute()
        
    results = []
    for item in response.data:
        flat = item.copy()
        if item.get('businesses'):
            flat['nombre'] = item['businesses']['nombre']
            flat['tipo_negocio'] = item['businesses']['tipo_negocio']
            flat['direccion'] = item['businesses']['direccion']
        results.append(flat)
        
    return results

def get_ventas_by_period(start_date: date, end_date: date) -> List[Dict[str, Any]]:
    """Get sales within date range"""
    supabase = init_connection()
    
    response = supabase.table("ventas")\
        .select("*, businesses(nombre, tipo_negocio, direccion)")\
        .gte("fecha_cierre", start_date.isoformat())\
        .lte("fecha_cierre", end_date.isoformat())\
        .order("fecha_cierre", desc=True)\
        .execute()
        
    results = []
    for item in response.data:
        flat = item.copy()
        if item.get('businesses'):
            flat['nombre'] = item['businesses']['nombre']
            flat['tipo_negocio'] = item['businesses']['tipo_negocio']
            flat['direccion'] = item['businesses']['direccion']
        results.append(flat)
        
    return results

def generate_venta_id() -> str:
    """Generate next sequential sale ID (LUX-YYYY-XXX)"""
    supabase = init_connection()
    current_year = datetime.now().year
    prefix = f"LUX-{current_year}-"
    
    # Get last sale ID for this year
    response = supabase.table("ventas")\
        .select("venta_id")\
        .ilike("venta_id", f"{prefix}%")\
        .order("venta_id", desc=True)\
        .limit(1)\
        .execute()
        
    if response.data:
        last_id = response.data[0]['venta_id']
        try:
            last_num = int(last_id.split('-')[-1])
            next_num = last_num + 1
        except ValueError:
            next_num = 1
    else:
        next_num = 1
        
    return f"{prefix}{next_num:03d}"

def get_week_number(date_obj: date) -> str:
    """Get ISO week number formatted as W##"""
    return f"W{date_obj.isocalendar()[1]:02d}"

# This initialization function is kept for compatibility but does nothing with Supabase directly
# Tables must be set up manually or via SQL migration script
def init_database():
    pass
