"""
Lux Sales Dashboard - Main Streamlit Application
Author: GitHub Copilot
Date: 13 January 2026
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from pathlib import Path
import sys

# Add app directory to path
sys.path.append(str(Path(__file__).parent))

from database_supabase import (
    init_database, create_visita, update_visita, delete_visita, 
    create_oportunidad, update_oportunidad, delete_oportunidad, 
    create_venta, get_visitas_by_period, get_oportunidades_activas, 
    get_ventas_by_period, generate_venta_id, get_week_number
)
from excel_reader import (
    read_gastos_excel, get_gastos_by_period, get_gastos_by_week,
    get_gastos_by_venta_id, get_costos_summary, IS_CLOUD,
    read_gastos_from_uploaded_file
)

# Page config
st.set_page_config(
    page_title="Lux Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_database()

# Constants
TIPOS_NEGOCIO = ["Taller Automotriz", "Detailing", "Maestranza", "Factoría", "Comercializadora", "Salón de Belleza", "Otro"]
PRODUCTOS = ["JP01Y (Poliurea Alto Tránsito)", "JP02R (Poliurea Impermeabilización)", 
             "JS02Y (Poliaspártico)", "JS02Y + Flakes Decorativos", 
             "1002A/B (Poliuretano Brillante)", "1003A/B (Poliuretano Mate)"]
SOURCES = ["Digital Advertising", "F2F Contact", "Known Client", "Referral"]
ASSIGNED_TO = ["Sebastian", "Ingemar", "Emmanuel", "Adolfo"]

# Sidebar navigation
st.sidebar.title("📊 Lux Dashboard")
st.sidebar.markdown("---")

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state['page'] = "🏠 Inicio"

# Page options
PAGES = ["🏠 Inicio", "📝 Registrar Visita", "🎯 Registrar Oportunidad", 
         "💰 Registrar Venta", "📋 Ver Registros", "📊 KPIs y Reportes"]

# Sidebar radio controlled by session state
current_index = PAGES.index(st.session_state['page']) if st.session_state['page'] in PAGES else 0

page = st.sidebar.radio(
    "Navegación",
    PAGES,
    index=current_index
)

# Only update session state if radio actually changed
if page != st.session_state['page']:
    st.session_state['page'] = page
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(f"📅 Hoy: {date.today().strftime('%d-%b-%Y')}\n\n🗓️ Semana: {get_week_number(date.today())}")


# ============= PAGE: INICIO =============
if st.session_state['page'] == "🏠 Inicio":
    st.title("🏠 Bienvenido al Dashboard Lux")
    st.markdown("### Sistema de Control de Ventas B2B - Pisos Industriales")
    
    col1, col2, col3 = st.columns(3)
    
    # Quick stats for this week
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = date(today.year, today.month, 1)
    
    visitas = get_visitas_by_period(week_start, today)
    visitas_mes = get_visitas_by_period(month_start, today)
    oportunidades = get_oportunidades_activas()
    ventas_semana = get_ventas_by_period(week_start, today)
    
    with col1:
        st.metric("✅ Visitas esta Semana", len(visitas), delta=f"{len(visitas_mes)} en el mes")
    
    with col2:
        st.metric("🎯 Oportunidades Activas", len(oportunidades))
    
    with col3:
        st.metric("💰 Ventas esta Semana", len(ventas_semana))
    
    st.markdown("---")
    st.markdown("### 📌 Acciones Rápidas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Nueva Visita", use_container_width=True):
            st.session_state['page'] = "📝 Registrar Visita"
            st.rerun()
    
    with col2:
        if st.button("🎯 Nueva Oportunidad", use_container_width=True):
            st.session_state['page'] = "🎯 Registrar Oportunidad"
            st.rerun()
    
    with col3:
        if st.button("💰 Nueva Venta", use_container_width=True):
            st.session_state['page'] = "💰 Registrar Venta"
            st.rerun()



# ============= PAGE: REGISTRAR VISITA =============
elif st.session_state['page'] == "📝 Registrar Visita":
    # Check if editing an existing visit
    editing_visita = st.session_state.get('visita_to_edit', None)
    st.title("📝 " + ("Editar Visita" if editing_visita else "Registrar Nueva Visita"))

    with st.form("form_visita"):
        st.markdown("### Datos del Negocio")

        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("Nombre del Negocio *", value=editing_visita['nombre'] if editing_visita else "", placeholder="Ej: Taller El Rayo")
            tipo_negocio = st.selectbox("Tipo de Negocio *", TIPOS_NEGOCIO, index=TIPOS_NEGOCIO.index(editing_visita['tipo_negocio']) if editing_visita else 0)

        with col2:
            fecha = st.date_input("Fecha de Visita *", value=editing_visita['fecha'] if editing_visita else date.today())
            semana = get_week_number(fecha)
            st.text_input("Semana", value=semana, disabled=True)

        direccion = st.text_area("Dirección *", value=editing_visita['direccion'] if editing_visita else "", placeholder="Ej: Av. Arriola 234, Urb. Industrial, La Victoria", height=100)

        notas = st.text_area("Notas / Observaciones", value=editing_visita['notas'] if editing_visita and editing_visita['notas'] else "", placeholder="Ej: Hablé con el dueño, mostró interés en JS02Y, tiene 150m²", height=100)

        submitted = st.form_submit_button("💾 Guardar Visita", use_container_width=True)

        if submitted:
            if nombre and tipo_negocio and direccion:
                try:
                    if editing_visita:
                        update_visita(editing_visita['id'], nombre, tipo_negocio, direccion, fecha, semana, notas)
                        st.success(f"✅ Visita actualizada exitosamente! ID: {editing_visita['id']}")
                        del st.session_state['visita_to_edit']
                        st.rerun()
                    else:
                        visita_id = create_visita(nombre, tipo_negocio, direccion, fecha, semana, notas)
                        st.success(f"✅ Visita registrada exitosamente! ID: {visita_id}")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error al guardar: {str(e)}")
            else:
                st.error("⚠️ Por favor complete todos los campos obligatorios (*)")

    # Show recent visits
    st.markdown("---")
    
    # Filter controls for the list
    col_filter1, col_filter2 = st.columns([2, 1])
    with col_filter1:
        st.markdown(f"### 📋 Visitas Recientes")
    with col_filter2:
        # Week number display in corner as requested
        current_week_num = get_week_number(date.today())
        st.markdown(f"#### 🗓️ Semana Actual: {current_week_num}")

    # Date selector for the list
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        filter_option = st.selectbox(
            "Filtrar lista por:", 
            ["Esta Semana (Lun-Dom)", "Últimos 15 días", "Seleccionar Rango"],
            index=1 # Default to last 15 days so we see recent entries even if they were last week
        )
    
    today = date.today()
    if filter_option == "Esta Semana (Lun-Dom)":
        start_date = today - timedelta(days=today.weekday())
        end_date = today + timedelta(days=6 - today.weekday())
    elif filter_option == "Últimos 15 días":
        start_date = today - timedelta(days=15)
        end_date = today
    else: # Select Range
        with col_d2:
            date_range = st.date_input(
                "Selecciona rango",
                value=(today - timedelta(days=7), today),
                key="visit_date_range"
            )
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
            else:
                start_date = today - timedelta(days=7)
                end_date = today

    visitas = get_visitas_by_period(start_date, end_date)

    if visitas:
        st.info(f"Mostrando {len(visitas)} visitas del {start_date} al {end_date}")
        for visita in visitas:
            with st.expander(f"📅 {visita['fecha']} | {visita['nombre']} ({visita['tipo_negocio']})"):
                st.write(f"**Dirección:** {visita['direccion']}")
                st.write(f"**Semana:** {visita['semana']}")
                if visita['notas']:
                    st.write(f"**Notas:** {visita['notas']}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✏️ Editar Visita", key=f"edit_{visita['id']}"):
                        st.session_state['visita_to_edit'] = visita
                        st.session_state['page'] = "📝 Registrar Visita"
                        st.rerun()
                with col2:
                    if st.button("🎯 Convertir a Oportunidad", key=f"conv_{visita['id']}"):
                        st.session_state['visita_to_convert'] = visita
                        st.session_state['page'] = "🎯 Registrar Oportunidad"
                        st.rerun()
                with col3:
                    if st.button("🗑️ Eliminar Visita", key=f"del_{visita['id']}"):
                        st.session_state['visita_to_delete'] = visita['id']
                        st.session_state['show_delete_confirm'] = True
                        st.rerun()
    else:
        st.info("No hay visitas registradas en este período.")

    # Delete confirmation dialog
    if st.session_state.get('show_delete_confirm', False):
        visita_id = st.session_state.get('visita_to_delete')
        if visita_id:
            st.warning("¿Está seguro que desea eliminar esta visita? Esta acción no se puede deshacer.")
            col1, col2 = st.columns(2)
            with col1:
                # Use a specific key for the confirm button that doesn't conflict
                if st.button("✅ Confirmar Eliminación", key="confirm_delete_btn"):
                    try:
                        delete_visita(visita_id)
                        st.success("Visita eliminada exitosamente.")
                        # Clear state
                        del st.session_state['visita_to_delete']
                        del st.session_state['show_delete_confirm']
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al eliminar: {e}")
            with col2:
                if st.button("❌ Cancelar", key="cancel_delete_btn"):
                    del st.session_state['visita_to_delete']
                    del st.session_state['show_delete_confirm']
                    st.rerun()


# ============= PAGE: REGISTRAR OPORTUNIDAD =============
elif st.session_state['page'] == "🎯 Registrar Oportunidad":
    st.title("🎯 Gestión de Oportunidades")
    
    # Check if converting from visit
    visita_convert = st.session_state.get('visita_to_convert', None)
    # Check if editing existing opportunity
    opp_to_edit = st.session_state.get('opp_to_edit', None)
    
    if opp_to_edit:
        st.info(f"✏️ Editando oportunidad: {opp_to_edit['nombre']}")
        if st.button("❌ Cancelar Edición"):
            del st.session_state['opp_to_edit']
            st.rerun()

    title_text = "Editar Oportunidad" if opp_to_edit else "Registrar Nueva Oportunidad"
    
    with st.form("form_oportunidad"):
        st.markdown(f"### {title_text}")
        
        col1, col2 = st.columns(2)
        
        # Defaults
        def_nombre = opp_to_edit['nombre'] if opp_to_edit else (visita_convert['nombre'] if visita_convert else "")
        def_tipo_idx = TIPOS_NEGOCIO.index(opp_to_edit['tipo_negocio']) if opp_to_edit else (TIPOS_NEGOCIO.index(visita_convert['tipo_negocio']) if visita_convert else 0)
        
        # Handle source default properly
        def_source_idx = 0
        if opp_to_edit and opp_to_edit.get('source') in SOURCES:
            def_source_idx = SOURCES.index(opp_to_edit['source'])
            
        def_fecha = datetime.strptime(opp_to_edit['fecha_contacto'], '%Y-%m-%d').date() if opp_to_edit and isinstance(opp_to_edit['fecha_contacto'], str) else (opp_to_edit['fecha_contacto'] if opp_to_edit else date.today())
        
        with col1:
            nombre = st.text_input("Nombre del Negocio *", 
                                   value=def_nombre,
                                   placeholder="Ej: Taller Los Andes")
            tipo_negocio = st.selectbox("Tipo de Negocio *", TIPOS_NEGOCIO,
                                       index=def_tipo_idx)
            source = st.selectbox("Fuente de Oportunidad *", SOURCES,
                                 index=def_source_idx)
        
        with col2:
            fecha_contacto = st.date_input("Fecha de Contacto *", value=def_fecha)
            semana = get_week_number(fecha_contacto)
            st.text_input("Semana", value=semana, disabled=True)
            
        def_direccion = opp_to_edit['direccion'] if opp_to_edit else (visita_convert['direccion'] if visita_convert else "")
        direccion = st.text_area("Dirección *", 
                                 value=def_direccion,
                                 placeholder="Ej: Av. Argentina 890, Callao", height=80)
        
        # --- Contact Info ---
        col_c1, col_c2, col_c3 = st.columns(3)
        def_contacto = opp_to_edit.get('nombre_contacto', "") if opp_to_edit else ""
        def_cargo = opp_to_edit.get('cargo_contacto', "") if opp_to_edit else ""
        def_celular = opp_to_edit.get('celular_contacto', "") if opp_to_edit else ""
        
        with col_c1:
            nombre_contacto = st.text_input("Nombre de Contacto", value=def_contacto, placeholder="Ej: Juan Pérez")
        with col_c2:
            cargo_contacto = st.text_input("Cargo", value=def_cargo, placeholder="Ej: Jefe de Mantenimiento")
        with col_c3:
            celular_contacto = st.text_input("Nro Celular", value=def_celular, placeholder="Ej: 999 888 777")
        # --------------------
        
        st.markdown("### Detalles de la Oportunidad")
        
        col1, col2 = st.columns(2)
        
        def_m2 = opp_to_edit['m2_estimado'] if opp_to_edit else 100
        
        # Product default
        def_prod_idx = 0
        if opp_to_edit and opp_to_edit.get('producto_interes') in PRODUCTOS:
            def_prod_idx = PRODUCTOS.index(opp_to_edit['producto_interes']) + 1 # +1 because of [""]
        elif opp_to_edit and opp_to_edit.get('producto_interes'):
             # If product exists but not in current list, handle it or just default 0
             pass 
        
        with col1:
            m2_estimado = st.number_input("m² Estimado", min_value=0, value=def_m2 or 0, step=10)
            
            # Handle product selection carefully
            prod_options = [""] + PRODUCTOS
            # Recalculate index based on full list
            curr_prod = opp_to_edit['producto_interes'] if opp_to_edit else ""
            try:
                prod_idx = prod_options.index(curr_prod)
            except ValueError:
                prod_idx = 0
                
            producto_interes = st.selectbox("Producto de Interés", prod_options, index=prod_idx)
        
        with col2:
            def_accion = opp_to_edit['siguiente_accion'] if opp_to_edit else ""
            siguiente_accion = st.text_area("Siguiente Acción", 
                                           value=def_accion or "",
                                           placeholder="Ej: Visita técnica programada para 20-Ene",
                                           height=100)
            
            # --- Auto-Assignment Display / Edit ---
            if opp_to_edit:
                curr_assigned = opp_to_edit.get('asignado_a')
                # If current assigned is not in list (e.g. None), default to first or handle it
                try:
                    assigned_idx = ASSIGNED_TO.index(curr_assigned)
                except ValueError:
                    assigned_idx = 0
                
                # Allow manual reassignment
                asignado_a = st.selectbox("Asignado a", ASSIGNED_TO, index=assigned_idx)
            else:
                # For new opportunities, assignment happens automatically on creation
                # We do NOT let the user pick here to ensure the probabilities are respected
                st.info("ℹ️ La oportunidad será asignada automáticamente a un vendedor al guardar.")
                asignado_a = None
            # --------------------------------------
        
        btn_label = "💾 Actualizar Oportunidad" if opp_to_edit else "💾 Guardar Oportunidad"
        submitted = st.form_submit_button(btn_label, use_container_width=True)
        
        if submitted:
            if nombre and tipo_negocio and direccion and source:
                try:
                    m2_val = m2_estimado if m2_estimado > 0 else None
                    prod_val = producto_interes if producto_interes else None
                    accion_val = siguiente_accion if siguiente_accion else None
                    
                    if opp_to_edit:
                        # Update
                        update_oportunidad(
                            opp_to_edit['id'], nombre, tipo_negocio, direccion,
                            fecha_contacto, semana, m2_val, prod_val, accion_val, source,
                            nombre_contacto, cargo_contacto, celular_contacto,
                            asignado_a=asignado_a
                        )
                        st.success(f"✅ Oportunidad actualizada exitosamente!")
                        del st.session_state['opp_to_edit']
                        st.balloons()
                        st.rerun()
                    else:
                        # Create
                        visita_id = visita_convert['id'] if visita_convert else None
                        opp_id = create_oportunidad(
                            nombre, tipo_negocio, direccion, fecha_contacto, semana,
                            m2_val, prod_val, accion_val,
                            visita_id, source,
                            nombre_contacto, cargo_contacto, celular_contacto
                        )
                        st.success(f"✅ Oportunidad registrada exitosamente! ID: {opp_id}")
                        st.balloons()
                        
                        # Clear conversion state
                        if 'visita_to_convert' in st.session_state:
                            del st.session_state['visita_to_convert']
                        
                except Exception as e:
                    st.error(f"❌ Error al guardar: {str(e)}")
            else:
                st.error("⚠️ Por favor complete todos los campos obligatorios (*)")
    
    # Show active opportunities
    st.markdown("---")
    st.markdown("### 📋 Oportunidades Activas")
    
    # Handle deletion state
    if 'opp_to_delete' in st.session_state:
        st.warning(f"¿Está seguro que desea eliminar la oportunidad de '{st.session_state['opp_to_delete']['nombre']}'? Esta acción no se puede deshacer.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirmar Eliminación", key="confirm_del_opp"):
                delete_oportunidad(st.session_state['opp_to_delete']['id'])
                st.success("Oportunidad eliminada.")
                del st.session_state['opp_to_delete']
                st.rerun()
        with col2:
            if st.button("❌ Cancelar", key="cancel_del_opp"):
                del st.session_state['opp_to_delete']
                st.rerun()

    oportunidades = get_oportunidades_activas()
    
    if oportunidades:
        for opp in oportunidades[:20]:  # Show first 20
            with st.expander(f"🎯 {opp['nombre']} ({opp['tipo_negocio']}) - {opp['m2_estimado']}m²"):
                st.write(f"**Dirección:** {opp['direccion']}")
                
                # Show contact info if available
                if opp.get('nombre_contacto') or opp.get('celular_contacto') or opp.get('cargo_contacto'):
                    contact_parts = []
                    if opp.get('nombre_contacto'): contact_parts.append(opp['nombre_contacto'])
                    if opp.get('cargo_contacto'): contact_parts.append(f"({opp['cargo_contacto']})")
                    if opp.get('celular_contacto'): contact_parts.append(f"📞 {opp['celular_contacto']}")
                    
                    st.write(f"**Contacto:** {' '.join(contact_parts)}")

                st.write(f"**Fuente:** {opp.get('source', 'N/A')}")
                st.write(f"**Asignado a:** {opp.get('asignado_a', 'Pendiente')}")
                st.write(f"**Fecha Contacto:** {opp['fecha_contacto']} ({opp['semana']})")
                if opp['producto_interes']:
                    st.write(f"**Producto:** {opp['producto_interes']}")
                if opp['siguiente_accion']:
                    st.write(f"**Siguiente Acción:** {opp['siguiente_accion']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("💰 Convertir", key=f"convventa_{opp['id']}"):
                        st.session_state['opp_to_convert'] = opp
                        st.session_state['page'] = "💰 Registrar Venta"
                        st.rerun()
                with col2:
                    if st.button("✏️ Editar", key=f"edit_{opp['id']}"):
                        st.session_state['opp_to_edit'] = opp
                        st.rerun()
                with col3:
                    if st.button("🗑️ Eliminar", key=f"del_{opp['id']}"):
                        st.session_state['opp_to_delete'] = opp
                        st.rerun()
    else:
        st.info("No hay oportunidades activas.")


# ============= PAGE: REGISTRAR VENTA =============
elif st.session_state['page'] == "💰 Registrar Venta":
    st.title("💰 Registrar Nueva Venta")
    
    # Check if converting from opportunity
    opp_convert = st.session_state.get('opp_to_convert', None)
    
    with st.form("form_venta"):
        st.markdown("### Datos de la Venta")
        
        col1, col2 = st.columns(2)
        
        with col1:
            venta_id = st.text_input("ID de Venta *", value=generate_venta_id(), disabled=True)
            nombre = st.text_input("Nombre del Negocio *",
                                   value=opp_convert['nombre'] if opp_convert else "",
                                   placeholder="Ej: Taller El Rayo")
            tipo_negocio = st.selectbox("Tipo de Negocio *", TIPOS_NEGOCIO,
                                       index=TIPOS_NEGOCIO.index(opp_convert['tipo_negocio']) if opp_convert else 0)
        
        with col2:
            fecha_cierre = st.date_input("Fecha de Cierre *", value=date.today())
            semana = get_week_number(fecha_cierre)
            st.text_input("Semana", value=semana, disabled=True)
        
        direccion = st.text_area("Dirección *",
                                 value=opp_convert['direccion'] if opp_convert else "",
                                 placeholder="Ej: Av. Arriola 234, La Victoria", height=80)
        
        st.markdown("### Detalles del Proyecto")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            m2_real = st.number_input("m² Real *", min_value=1, 
                                     value=opp_convert['m2_estimado'] if opp_convert and opp_convert['m2_estimado'] else 100,
                                     step=10)
        
        with col2:
            producto = st.selectbox("Producto *", PRODUCTOS,
                                   index=PRODUCTOS.index(opp_convert['producto_interes']) if opp_convert and opp_convert['producto_interes'] in PRODUCTOS else 0)
        
        with col3:
            monto_soles = st.number_input("Monto S/. *", min_value=0.0, value=10000.0, step=500.0)
        
        fecha_instalacion = st.date_input("Fecha de Instalación", value=date.today() + timedelta(days=7))
        
        submitted = st.form_submit_button("💰 Registrar Venta", use_container_width=True)
        
        if submitted:
            if nombre and tipo_negocio and direccion and m2_real > 0 and monto_soles > 0:
                try:
                    opp_id = opp_convert['id'] if opp_convert else None
                    sale_id = create_venta(
                        venta_id, nombre, tipo_negocio, direccion,
                        fecha_cierre, semana, m2_real, producto, monto_soles,
                        fecha_instalacion, opp_id
                    )
                    st.success(f"✅ Venta registrada exitosamente! {venta_id}")
                    st.balloons()
                    
                    # Show summary
                    st.info(f"""
                    **Resumen de la Venta:**
                    - Cliente: {nombre}
                    - m²: {m2_real}
                    - Monto: S/. {monto_soles:,.2f}
                    - Instalación: {fecha_instalacion}
                    """)
                    
                    # Clear conversion state
                    if 'opp_to_convert' in st.session_state:
                        del st.session_state['opp_to_convert']
                        
                except Exception as e:
                    st.error(f"❌ Error al guardar: {str(e)}")
            else:
                st.error("⚠️ Por favor complete todos los campos obligatorios (*)")
    
    # Show recent sales
    st.markdown("---")
    st.markdown("### 📋 Ventas Recientes (Este Mes)")
    
    today = date.today()
    month_start = date(today.year, today.month, 1)
    ventas = get_ventas_by_period(month_start, today)
    
    if ventas:
        for venta in ventas:
            with st.expander(f"💰 {venta['venta_id']} | {venta['nombre']} - S/. {venta['monto_soles']:,.2f}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Tipo:** {venta['tipo_negocio']}")
                    st.write(f"**m²:** {venta['m2_real']}")
                    st.write(f"**Producto:** {venta['producto']}")
                with col2:
                    st.write(f"**Fecha Cierre:** {venta['fecha_cierre']}")
                    st.write(f"**Instalación:** {venta['fecha_instalacion']}")
                    st.write(f"**Dirección:** {venta['direccion']}")
    else:
        st.info("No hay ventas registradas este mes.")


# ============= PAGE: VER REGISTROS =============
elif st.session_state['page'] == "📋 Ver Registros":
    st.title("📋 Historial de Registros")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Visitas", "🎯 Oportunidades", "💰 Ventas", "💸 Gastos"])
    
    with tab1:
        st.markdown("### Visitas Registradas")
        
        col1, col2 = st.columns(2)
        with col1:
            periodo = st.selectbox("Período", ["Esta Semana", "Este Mes", "Todo"])
        
        today = date.today()
        
        if periodo == "Esta Semana":
            start_date = today - timedelta(days=today.weekday())
            end_date = today
        elif periodo == "Este Mes":
            start_date = date(today.year, today.month, 1)
            end_date = today
        else:
            start_date = date(2026, 1, 1)
            end_date = today
        
        visitas = get_visitas_by_period(start_date, end_date)
        
        if visitas:
            df = pd.DataFrame(visitas)
            st.dataframe(df[['fecha', 'nombre', 'tipo_negocio', 'direccion', 'semana']], use_container_width=True)
            st.info(f"📊 Total: {len(visitas)} visitas")
        else:
            st.info("No hay visitas en este período.")
    
    with tab2:
        st.markdown("### Oportunidades")
        
        estado_filter = st.selectbox("Estado", ["Activas", "Todas"])
        
        oportunidades = get_oportunidades_activas()  # TODO: Add filter for all
        
        if oportunidades:
            df = pd.DataFrame(oportunidades)
            st.dataframe(df[['fecha_contacto', 'nombre', 'tipo_negocio', 'm2_estimado', 'producto_interes']], 
                        use_container_width=True)
            st.info(f"📊 Total: {len(oportunidades)} oportunidades")
        else:
            st.info("No hay oportunidades activas.")
    
    with tab3:
        st.markdown("### Ventas Cerradas")
        
        col1, col2 = st.columns(2)
        with col1:
            periodo_ventas = st.selectbox("Período", ["Este Mes", "Este Año", "Todo"], key="periodo_ventas")
        
        today = date.today()
        
        if periodo_ventas == "Este Mes":
            start_date = date(today.year, today.month, 1)
            end_date = today
        elif periodo_ventas == "Este Año":
            start_date = date(today.year, 1, 1)
            end_date = today
        else:
            start_date = date(2026, 1, 1)
            end_date = today
        
        ventas = get_ventas_by_period(start_date, end_date)
        
        if ventas:
            df = pd.DataFrame(ventas)
            st.dataframe(df[['venta_id', 'fecha_cierre', 'nombre', 'tipo_negocio', 'm2_real', 'monto_soles']], 
                        use_container_width=True)
            
            total_m2 = df['m2_real'].sum()
            total_soles = df['monto_soles'].sum()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Ventas", len(ventas))
            with col2:
                st.metric("📐 m² Totales", f"{total_m2:,}")
            with col3:
                st.metric("💰 Ingresos S/.", f"{total_soles:,.2f}")
        else:
            st.info("No hay ventas en este período.")
    
    with tab4:
        st.markdown("### Gastos y Costos (desde Excel)")
        
        # Show cloud warning if applicable
        if IS_CLOUD:
            st.warning("⚠️ **Modo Cloud**: El archivo Excel en Google Drive no está accesible desde la nube.")
            
            # File uploader
            st.markdown("#### 📤 Subir Archivo Excel")
            uploaded_file = st.file_uploader(
                "Sube el archivo `Gastos_Semanal_Template_V2.xlsx` aquí:",
                type=['xlsx', 'xls'],
                help="El contador debe subir el archivo Excel con los gastos registrados"
            )
            
            if uploaded_file is not None:
                # Store in session state
                st.session_state['uploaded_gastos'] = uploaded_file
                st.success("✅ Archivo cargado exitosamente!")
        
        col1, col2 = st.columns(2)
        with col1:
            periodo_gastos = st.selectbox("Período", ["Este Mes", "Este Año", "Todo"], key="periodo_gastos")
        
        today = date.today()
        
        if periodo_gastos == "Este Mes":
            start_date = date(today.year, today.month, 1)
            end_date = today
        elif periodo_gastos == "Este Año":
            start_date = date(today.year, 1, 1)
            end_date = today
        else:
            start_date = date(2026, 1, 1)
            end_date = today
        
        # Read expenses from Excel
        gastos_df = pd.DataFrame()
        
        try:
            if IS_CLOUD and 'uploaded_gastos' in st.session_state:
                # Read from uploaded file
                gastos_df = read_gastos_from_uploaded_file(st.session_state['uploaded_gastos'])
                # Filter by period
                if not gastos_df.empty:
                    mask = (gastos_df['Fecha'].dt.date >= start_date) & (gastos_df['Fecha'].dt.date <= end_date)
                    gastos_df = gastos_df[mask]
            else:
                # Read from local file
                gastos_df = get_gastos_by_period(start_date, end_date)
        except Exception as e:
            st.error(f"❌ Error al leer archivo Excel: {str(e)}")
            gastos_df = pd.DataFrame()
        
        if not gastos_df.empty:
            # Show data table
            display_df = gastos_df.copy()
            display_df['Fecha'] = display_df['Fecha'].dt.strftime('%Y-%m-%d')
            st.dataframe(display_df[['Fecha', 'Semana', 'Tipo_Gasto', 'Categoría', 'Tipo_Negocio', 'Monto_Soles', 'Venta_ID']], 
                        use_container_width=True)
            
            # Summary metrics
            total_gastos = gastos_df['Monto_Soles'].sum()
            costos_directos = gastos_df[gastos_df['Categoría'] == 'Costo Directo']['Monto_Soles'].sum()
            costos_indirectos = gastos_df[gastos_df['Categoría'] == 'Costo Indirecto']['Monto_Soles'].sum()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total Gastos", f"S/. {total_gastos:,.0f}")
            with col2:
                st.metric("💰 Costos Directos", f"S/. {costos_directos:,.0f}")
            with col3:
                st.metric("🏢 Costos Indirectos", f"S/. {costos_indirectos:,.0f}")
            with col4:
                st.metric("📝 Registros", len(gastos_df))
            
            # Breakdown by type
            st.markdown("#### 📊 Distribución por Tipo de Gasto")
            tipo_gasto_sum = gastos_df.groupby('Tipo_Gasto')['Monto_Soles'].sum().sort_values(ascending=False)
            
            for tipo, monto in tipo_gasto_sum.items():
                pct = (monto / total_gastos * 100) if total_gastos > 0 else 0
                st.write(f"**{tipo}**: S/. {monto:,.2f} ({pct:.1f}%)")
        else:
            st.info("📝 No hay gastos registrados en este período.\n\nEl contador debe llenar el archivo Excel en Google Drive.")
            st.caption(f"📁 Archivo: `G:\\My Drive\\NewLux\\KPIs_Accounting\\Gastos_Semanal_Template_V2.xlsx`")
            
            # Show instructions
            with st.expander("ℹ️ Instrucciones para el Contador"):
                st.markdown("""
                **Cómo registrar gastos:**
                
                1. Abrir archivo Excel en Google Drive
                2. Ir a la hoja "Gastos"
                3. Llenar una fila por cada gasto:
                   - **Fecha**: Fecha del gasto
                   - **Semana**: Número de semana (se calcula automático)
                   - **Tipo_Gasto**: Material, Mano de Obra, Transporte, u Otro
                   - **Categoría**: Costo Directo o Indirecto
                   - **Tipo_Negocio**: Taller Automotriz, Detailing, etc.
                   - **Descripción**: Detalle del gasto
                   - **Monto_Soles**: Cantidad en soles
                   - **Venta_ID**: Si aplica a una venta específica (ej: LUX-2026-001)
                4. Guardar el archivo
                5. Recargar esta página para ver los datos actualizados
                """)



# ============= PAGE: KPIs Y REPORTES =============
elif st.session_state['page'] == "📊 KPIs y Reportes":
    st.title("📊 KPIs y Reportes")
    st.info("🚧 Dashboard de KPIs en desarrollo - Próximamente con gráficos interactivos")
    
    # Quick summary
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = date(today.year, today.month, 1)
    
    visitas_semana = get_visitas_by_period(week_start, today)
    visitas_mes = get_visitas_by_period(month_start, today)
    oportunidades = get_oportunidades_activas()
    ventas_mes = get_ventas_by_period(month_start, today)
    
    st.markdown("### 📊 Resumen Mensual")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Visitas (Mes)", len(visitas_mes))
        st.caption(f"Esta semana: {len(visitas_semana)}")
    
    with col2:
        st.metric("Oportunidades Activas", len(oportunidades))
    
    with col3:
        st.metric("Ventas (Mes)", len(ventas_mes))
    
    with col4:
        if ventas_mes:
            total_ingresos = sum(v['monto_soles'] for v in ventas_mes)
            st.metric("Ingresos S/.", f"{total_ingresos:,.0f}")
        else:
            st.metric("Ingresos S/.", "0")
    
    # Conversion rates
    st.markdown("### 🎯 Tasas de Conversión")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if len(visitas_mes) > 0:
            tasa_vo = (len(oportunidades) / len(visitas_mes)) * 100
            st.metric("Visitas → Oportunidades", f"{tasa_vo:.1f}%")
        else:
            st.metric("Visitas → Oportunidades", "N/A")
    
    with col2:
        if len(oportunidades) > 0:
            tasa_ov = (len(ventas_mes) / len(oportunidades)) * 100
            st.metric("Oportunidades → Ventas", f"{tasa_ov:.1f}%")
        else:
            st.metric("Oportunidades → Ventas", "N/A")


# Footer
st.markdown("---")
st.markdown("**Lux Pisos Industriales** | Dashboard v1.0 | 2026")
