# 🚀 Dashboard de Control - Resumen Ejecutivo

**Fecha:** 13 Enero 2026  
**Estado:** ✅ Excel Template creado | 🔄 Dashboard App en desarrollo

---

## ✅ Lo Que Ya Está Listo

### 1. Excel Template para Contador
- **Ubicación:** `G:\My Drive\NewLux\KPIs_Accounting\Costos_Semanal_Template.xlsx`
- **Estado:** ✅ Creado y funcional
- **Características:**
  - 3 hojas (Costos Directos, Costos Indirectos, Instrucciones)
  - Fórmulas automáticas para totales
  - Dropdowns para tipos de negocio
  - 52 semanas pre-cargadas
  - Formato profesional con colores Lux

### 2. Documentación Completa
- **KPI Specifications:** Todos los KPIs definidos con fórmulas exactas
- **README para Contador:** Guía completa de cómo usar el Excel

---

## 🎯 Los 12 KPIs del Dashboard

### 📊 Actividad (Leading Indicators)
1. **Visitas Realizadas** - Meta: 100/mes
2. **Oportunidades Creadas** - Meta: 40/mes

### 🔄 Conversión (Auto-calculados)
3. **Tasa V→O** - Meta: ≥40%
4. **Tasa O→V** - Meta: ≥20%

### 💰 Resultados (Business Impact)
5. **Ventas Cerradas** - Meta: 3/mes
6. **m² Vendidos** - Meta: 2,000/mes
7. **Ingresos (S/.)** - Meta: S/. 45,000/mes
8. **Ticket Promedio** - Meta: S/. 13,125/venta

### 💵 Financieros (Con data del contador)
9. **Costos Directos por Proyecto**
10. **Costos Indirectos (Overhead)**
11. **Utilidad Operativa** - Meta: S/. 12,500/mes
12. **Margen Operativo (%)** - Meta: ≥30%

---

## 📋 Workflow Semanal

### Viernes (Vendedor):
- [ ] Abrir dashboard web (localhost:8501)
- [ ] Ingresar datos de la semana:
  - Visitas por tipo de negocio
  - Oportunidades creadas
  - Ventas cerradas (si hubo)
  - m² e ingresos
- [ ] Revisar gráficos y alertas
- [ ] **Tiempo:** 5 minutos

### Lunes (Contador):
- [ ] Abrir Excel en Google Drive
- [ ] Llenar "Costos_Directos" (proyectos cerrados)
- [ ] Llenar "Costos_Indirectos" (gastos de la semana)
- [ ] Guardar (auto-sincroniza)
- [ ] **Tiempo:** 10-15 minutos

### Automático (Dashboard):
- Lee base de datos SQLite
- Lee Excel desde Google Drive
- Calcula 12 KPIs
- Genera alertas si hay problemas
- Muestra gráficos actualizados

---

## 🎨 Visualizaciones del Dashboard

### Vista Semanal (Operativa):
```
┌─────────────────────────────────────┐
│   EMBUDO DE CONVERSIÓN - W02        │
├─────────────────────────────────────┤
│   Visitas: 25                       │
│      ↓ 40% (Meta: >40%) ✅          │
│   Oportunidades: 10                 │
│      ↓ 30% (Meta: >20%) ✅          │
│   Ventas: 3                         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   PROGRESO VS META MENSUAL          │
├─────────────────────────────────────┤
│   Visitas:  52/100  [████████░░] 52%│
│   Ventas:    2/3    [██████░░░░] 67%│
│   m²:      450/2000 [██░░░░░░░░] 23%│
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   RANKING POR SEGMENTO              │
├─────────────────────────────────────┤
│  1. Taller Automotriz  60% 🏆       │
│  2. Detailing          30%          │
│  3. Maestranza         10%          │
└─────────────────────────────────────┘
```

### Vista Mensual (Financiera):
```
┌─────────────────────────────────────┐
│   ESTADO DE RESULTADOS - ENERO      │
├─────────────────────────────────────┤
│   Ingresos:          S/. 45,000     │
│   - Costos Directos: S/. 24,000     │
│   ─────────────────────────────     │
│   = Margen Bruto:    S/. 21,000 47% │
│                                      │
│   - Costos Indirect: S/.  8,500     │
│   ─────────────────────────────     │
│   = Utilidad Oper:   S/. 12,500 28% │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   RENTABILIDAD POR SEGMENTO         │
├─────────────────────────────────────┤
│   Taller Automotriz                 │
│   • Ticket: S/. 15,000              │
│   • Margen: 45% ✅                  │
│                                      │
│   Detailing                         │
│   • Ticket: S/. 8,500               │
│   • Margen: 52% ✅                  │
└─────────────────────────────────────┘
```

---

## 🚨 Sistema de Alertas

### 🔴 Alarmas Rojas (Acción Inmediata):
- Conversión V→O < 20% por 2 semanas → Revisar pitch
- Conversión O→V < 10% por 3 semanas → Revisar pricing
- Margen Operativo < 15% → Subir precios o bajar costos
- Cero ventas en 3 semanas → Intensificar visitas

### ⚠️ Alarmas Amarillas (Monitorear):
- Visitas < 20/semana por 2 semanas → Revisar motivación
- Ticket Promedio < S/. 9,000 → Enfocarse en proyectos grandes
- Costos Indirectos > 25% → Revisar gastos admin

---

## 🔧 Stack Tecnológico

### Backend:
- **Python 3.10+**
- **SQLite** (base de datos local)
- **pandas + openpyxl** (lectura de Excel)

### Frontend:
- **Streamlit** (framework web Python)
- **Plotly** (gráficos interactivos)

### Hosting:
- **Streamlit Cloud** (gratis, accesible 24/7)
- **URL:** `https://lux-dashboard.streamlit.app` (por definir)

### Datos:
- **Ventas:** SQLite en `Control_Dashboard/data/lux_sales.db`
- **Costos:** Excel en Google Drive `G:\My Drive\NewLux\KPIs_Accounting\Costos_Semanal_Template.xlsx`

---

## 📅 Próximos Pasos

### Semana 1 (Actual):
- [✅] Excel Template creado
- [✅] Documentación completa
- [ ] Crear estructura SQLite
- [ ] Desarrollar formulario de entrada (Streamlit)
- [ ] Implementar cálculo de KPIs 1-8

### Semana 2:
- [ ] Vista Semanal (embudo + tendencias)
- [ ] Vista Mensual (P&L + segmentos)
- [ ] Gráficos interactivos con Plotly
- [ ] Exportar a PDF

### Semana 3:
- [ ] Integrar lector de Excel (costos)
- [ ] Calcular márgenes por proyecto
- [ ] Dashboard financiero completo

### Semana 4:
- [ ] Sistema de alertas automáticas
- [ ] Móvil-responsive
- [ ] Deploy a Streamlit Cloud
- [ ] Capacitación al equipo

---

## 📞 Contacto

**Preguntas sobre el Dashboard:**  
📧 Email: [tu email]

**Soporte Técnico:**  
GitHub Copilot @ VS Code

---

**Última actualización:** 13 Enero 2026  
**Versión:** 1.0 - Excel Template Ready
