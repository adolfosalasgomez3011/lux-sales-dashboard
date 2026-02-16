def delete_visita(visita_id: int) -> None:
    """Delete a visit record by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM visitas WHERE id = ?", (visita_id,))
    conn.commit()
    conn.close()
"""
Database schema and operations for Lux Sales Dashboard
Author: GitHub Copilot
Date: 13 January 2026
"""

import sqlite3
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / "data" / "lux_sales.db"

def init_database():
    """Create database tables if they don't exist"""
    
    # Ensure data directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table 1: Businesses (central registry)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS businesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        tipo_negocio TEXT NOT NULL,
        direccion TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(nombre, direccion)
    )
    """)
    
    # Table 2: Visits
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        fecha DATE NOT NULL,
        semana TEXT NOT NULL,
        notas TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (business_id) REFERENCES businesses(id)
    )
    """)
    
    # Table 3: Opportunities
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS oportunidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        visita_id INTEGER,
        fecha_contacto DATE NOT NULL,
        semana TEXT NOT NULL,
        m2_estimado INTEGER,
        producto_interes TEXT,
        siguiente_accion TEXT,
        estado TEXT DEFAULT 'Activa',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (business_id) REFERENCES businesses(id),
        FOREIGN KEY (visita_id) REFERENCES visitas(id)
    )
    """)
    
    # Table 4: Sales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id TEXT UNIQUE NOT NULL,
        business_id INTEGER NOT NULL,
        oportunidad_id INTEGER,
        fecha_cierre DATE NOT NULL,
        semana TEXT NOT NULL,
        m2_real INTEGER NOT NULL,
        producto TEXT NOT NULL,
        monto_soles DECIMAL(10,2) NOT NULL,
        fecha_instalacion DATE,
        estado TEXT DEFAULT 'Cerrada',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (business_id) REFERENCES businesses(id),
        FOREIGN KEY (oportunidad_id) REFERENCES oportunidades(id)
    )
    """)
    
    # Create indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_visitas_fecha ON visitas(fecha)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_visitas_semana ON visitas(semana)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_oportunidades_fecha ON oportunidades(fecha_contacto)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_oportunidades_estado ON oportunidades(estado)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas(fecha_cierre)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ventas_semana ON ventas(semana)")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized: {DB_PATH}")


def get_or_create_business(nombre: str, tipo_negocio: str, direccion: str) -> int:
    """
    Get existing business ID or create new one
    Automatic linking by nombre + direccion
    Returns: business_id
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Try to find existing business (case-insensitive)
    cursor.execute("""
        SELECT id FROM businesses 
        WHERE LOWER(nombre) = LOWER(?) AND LOWER(direccion) = LOWER(?)
    """, (nombre, direccion))
    
    result = cursor.fetchone()
    
    if result:
        business_id = result[0]
        # Update tipo_negocio if changed
        cursor.execute("""
            UPDATE businesses 
            SET tipo_negocio = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (tipo_negocio, business_id))
    else:
        # Create new business
        cursor.execute("""
            INSERT INTO businesses (nombre, tipo_negocio, direccion)
            VALUES (?, ?, ?)
        """, (nombre, tipo_negocio, direccion))
        business_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return business_id


def create_visita(nombre: str, tipo_negocio: str, direccion: str, 
                  fecha: date, semana: str, notas: Optional[str] = None) -> int:
    """Create new visit record"""
    
    business_id = get_or_create_business(nombre, tipo_negocio, direccion)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO visitas (business_id, fecha, semana, notas)
        VALUES (?, ?, ?, ?)
    """, (business_id, fecha, semana, notas))
    
    visita_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return visita_id


def update_visita(visita_id: int, nombre: str, tipo_negocio: str, direccion: str,
                  fecha: date, semana: str, notas: Optional[str] = None) -> None:
    """Update an existing visit record by ID"""
    business_id = get_or_create_business(nombre, tipo_negocio, direccion)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE visitas
        SET business_id = ?, fecha = ?, semana = ?, notas = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (business_id, fecha, semana, notas, visita_id))
    conn.commit()
    conn.close()


def create_oportunidad(nombre: str, tipo_negocio: str, direccion: str,
                       fecha_contacto: date, semana: str, m2_estimado: Optional[int] = None,
                       producto_interes: Optional[str] = None, siguiente_accion: Optional[str] = None,
                       visita_id: Optional[int] = None) -> int:
    """Create new opportunity record"""
    
    business_id = get_or_create_business(nombre, tipo_negocio, direccion)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO oportunidades (business_id, visita_id, fecha_contacto, semana, 
                                   m2_estimado, producto_interes, siguiente_accion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (business_id, visita_id, fecha_contacto, semana, m2_estimado, producto_interes, siguiente_accion))
    
    oportunidad_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return oportunidad_id


def create_venta(venta_id: str, nombre: str, tipo_negocio: str, direccion: str,
                 fecha_cierre: date, semana: str, m2_real: int, producto: str,
                 monto_soles: float, fecha_instalacion: Optional[date] = None,
                 oportunidad_id: Optional[int] = None) -> int:
    """Create new sale record"""
    
    business_id = get_or_create_business(nombre, tipo_negocio, direccion)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO ventas (venta_id, business_id, oportunidad_id, fecha_cierre, semana,
                           m2_real, producto, monto_soles, fecha_instalacion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (venta_id, business_id, oportunidad_id, fecha_cierre, semana, m2_real, 
          producto, monto_soles, fecha_instalacion))
    
    sale_id = cursor.lastrowid
    
    # Mark opportunity as converted if linked
    if oportunidad_id:
        cursor.execute("""
            UPDATE oportunidades 
            SET estado = 'Convertida', updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (oportunidad_id,))
    
    conn.commit()
    conn.close()
    
    return sale_id


def get_visitas_by_period(start_date: date, end_date: date) -> List[Dict[str, Any]]:
    """Get visits within date range with business details"""
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT v.id, v.fecha, v.semana, v.notas,
               b.nombre, b.tipo_negocio, b.direccion
        FROM visitas v
        JOIN businesses b ON v.business_id = b.id
        WHERE v.fecha BETWEEN ? AND ?
        ORDER BY v.fecha DESC
    """, (start_date, end_date))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results


def get_oportunidades_activas() -> List[Dict[str, Any]]:
    """Get active opportunities with business details"""
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT o.id, o.fecha_contacto, o.semana, o.m2_estimado, 
               o.producto_interes, o.siguiente_accion, o.estado,
               b.nombre, b.tipo_negocio, b.direccion
        FROM oportunidades o
        JOIN businesses b ON o.business_id = b.id
        WHERE o.estado = 'Activa'
        ORDER BY o.fecha_contacto DESC
    """)
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results


def get_ventas_by_period(start_date: date, end_date: date) -> List[Dict[str, Any]]:
    """Get sales within date range with business details"""
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT v.id, v.venta_id, v.fecha_cierre, v.semana, v.m2_real,
               v.producto, v.monto_soles, v.fecha_instalacion, v.estado,
               b.nombre, b.tipo_negocio, b.direccion
        FROM ventas v
        JOIN businesses b ON v.business_id = b.id
        WHERE v.fecha_cierre BETWEEN ? AND ?
        ORDER BY v.fecha_cierre DESC
    """, (start_date, end_date))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results


def generate_venta_id() -> str:
    """Generate next sequential sale ID (LUX-2026-XXX)"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get current year
    year = datetime.now().year
    
    # Find highest number for this year
    cursor.execute("""
        SELECT venta_id FROM ventas 
        WHERE venta_id LIKE ?
        ORDER BY venta_id DESC LIMIT 1
    """, (f"LUX-{year}-%",))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        # Extract number and increment
        last_id = result[0]
        last_num = int(last_id.split('-')[-1])
        next_num = last_num + 1
    else:
        # First sale of the year
        next_num = 1
    
    return f"LUX-{year}-{next_num:03d}"


def get_week_number(date_obj: date) -> str:
    """Get ISO week number formatted as W##"""
    return f"W{date_obj.isocalendar()[1]:02d}"


if __name__ == "__main__":
    # Initialize database when run directly
    init_database()
    print("✅ Database schema created successfully")
    print(f"📁 Location: {DB_PATH}")
