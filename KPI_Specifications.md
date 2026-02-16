# Especificaciones de KPIs - Dashboard de Control Semanal Lux 2026

**Fecha de Creación:** 13 de Enero 2026  
**Propósito:** Sistema de control semanal para ventas B2B de pisos industriales (Talleres Automotrices)  
**Principio de Diseño:** Máxima simplicidad - mínima carga de entrada, máxima visibilidad de resultados

---

## 1. Arquitectura de Datos

### 1.1 Fuentes de Información

| Fuente | Responsable | Frecuencia | Método de Entrada |
|--------|-------------|------------|-------------------|
| **Actividades de Ventas** | Vendedor/Gerente | Semanal (Viernes) | Dashboard App |
| **Costos por Proyecto** | Contador | Semanal (Lunes) | Excel Template |
| **Costos Indirectos** | Contador | Semanal (Lunes) | Excel Template |

### 1.2 Flujo de Datos (ETL Simplificado)

```
┌─────────────────────┐
│  Vendedor Ingresa   │
│  - Visitas          │──┐
│  - Oportunidades    │  │
│  - Ventas           │  │
│  - m² e Ingresos    │  │
└─────────────────────┘  │
                         │
┌─────────────────────┐  │    ┌──────────────────┐
│ Contador Ingresa    │  │    │  DASHBOARD APP   │
│ Excel Template:     │  ├───▶│  (Python/Web)    │───▶ Visualización
│  - Costos Directos  │  │    │  - Lee ambas     │     (Gráficos + Tablas)
│  - Costos Indirectos│──┘    │  - Calcula KPIs  │
└─────────────────────┘       │  - Genera Report │
                              └──────────────────┘
```

---

## 2. KPIs Definidos

### 2.1 Métricas de Actividad (Leading Indicators)

#### **KPI-01: Visitas Realizadas**
- **Definición:** Cantidad de talleres/negocios visitados donde se presentó Lux (contacto o no contacto)
- **Fuente:** Entrada manual del vendedor
- **Frecuencia:** Semanal
- **Granularidad:** Por Tipo de Negocio (Taller Automotriz, Detailing, Maestranza, Factoría, Otro)
- **Meta:** 25 visitas/semana, 100 visitas/mes
- **Cálculo:** Suma simple de registros

**Campos de Entrada:**
```json
{
  "fecha": "2026-01-13",
  "semana": "W02",
  "visitas_taller_automotriz": 12,
  "visitas_detailing": 5,
  "visitas_maestranza": 3,
  "visitas_factoria": 2,
  "visitas_otro": 3,
  "total_visitas": 25  // auto-calculado
}
```

---

#### **KPI-02: Oportunidades Creadas**
- **Definición:** Cantidad de prospectos que mostraron interés real (pidieron cotización, agendaron visita técnica, o solicitaron info adicional)
- **Fuente:** Entrada manual del vendedor
- **Frecuencia:** Semanal
- **Granularidad:** Por Tipo de Negocio
- **Meta:** 10 oportunidades/semana (40/mes)
- **Cálculo:** Suma simple de registros

**Criterio de Calificación:**
- ✅ **SÍ es Oportunidad:** "Envíeme la cotización", "Venga a medir", "¿Cuánto tarda la instalación?"
- ❌ **NO es Oportunidad:** "Déjeme su tarjeta", "Después lo llamo", "Ahora no tengo presupuesto"

**Campos de Entrada:**
```json
{
  "fecha": "2026-01-13",
  "semana": "W02",
  "oportunidades_taller_automotriz": 5,
  "oportunidades_detailing": 2,
  "oportunidades_maestranza": 1,
  "oportunidades_factoria": 1,
  "oportunidades_otro": 1,
  "total_oportunidades": 10  // auto-calculado
}
```

---

### 2.2 Métricas de Conversión (Auto-Calculadas)

#### **KPI-03: Tasa de Conversión Visitas → Oportunidades**
- **Definición:** % de visitas que generaron una oportunidad calificada
- **Fuente:** Auto-calculado
- **Fórmula:** `(Oportunidades Creadas / Visitas Realizadas) × 100`
- **Meta:** ≥ 40% (benchmark industria: 30-50%)
- **Alarma:** Si < 25%, revisar calidad del pitch o Sample Book

**Ejemplo:**
```
Semana 2: 10 oportunidades / 25 visitas = 40% ✅
Semana 3: 8 oportunidades / 30 visitas = 26.7% ⚠️
```

**Granularidad:** Se calcula también por tipo de negocio para identificar segmentos más receptivos.

---

#### **KPI-04: Tasa de Conversión Oportunidades → Ventas**
- **Definición:** % de oportunidades que cerraron en venta
- **Fuente:** Auto-calculado
- **Fórmula:** `(Ventas Cerradas / Oportunidades Creadas en Período Anterior*) × 100`
- **Meta:** ≥ 20% (benchmark industria B2B: 15-25%)
- **Alarma:** Si < 10%, revisar pricing o tiempo de respuesta

**Nota sobre período:** Usar oportunidades de 2-4 semanas atrás (ciclo de venta promedio)

**Ejemplo:**
```
Oportunidades Semana 1: 12
Ventas cerradas Semana 3: 3
Conversión: 3/12 = 25% ✅
```

---

### 2.3 Métricas de Resultado (Business Impact)

#### **KPI-05: Ventas Cerradas**
- **Definición:** Cantidad de proyectos con contrato firmado y fecha de instalación confirmada
- **Fuente:** Entrada manual del vendedor
- **Frecuencia:** Semanal
- **Granularidad:** Por Tipo de Negocio
- **Meta:** 3 ventas/mes (12 ventas en Q1-Q2 2026)
- **Cálculo:** Suma simple

**Campos de Entrada:**
```json
{
  "fecha_cierre": "2026-01-13",
  "semana": "W02",
  "ventas_taller_automotriz": 1,
  "ventas_detailing": 1,
  "ventas_maestranza": 0,
  "ventas_factoria": 0,
  "ventas_otro": 0,
  "total_ventas": 2
}
```

---

#### **KPI-06: m² Totales Vendidos**
- **Definición:** Superficie total (metros cuadrados) de todos los proyectos cerrados
- **Fuente:** Entrada manual del vendedor (al cerrar venta)
- **Frecuencia:** Semanal
- **Meta:** 2,000 m²/mes (24,000 m² en 2026)
- **Cálculo:** Suma de m² por proyecto

**Campos de Entrada:**
```json
{
  "venta_id": "LUX-2026-001",
  "fecha_cierre": "2026-01-13",
  "tipo_negocio": "Taller Automotriz",
  "m2_vendidos": 150,
  "producto": "JS02Y + Flakes"
}
```

---

#### **KPI-07: Ingresos en Soles (S/.)**
- **Definición:** Valor total facturado o por facturar de ventas cerradas (sin IVA)
- **Fuente:** Entrada manual del vendedor
- **Frecuencia:** Semanal (al cerrar venta)
- **Meta:** S/. 45,000/mes (≈ $12,000 USD × 3.75 tipo de cambio)
- **Cálculo:** Suma de valor de contratos

**Campos de Entrada:**
```json
{
  "venta_id": "LUX-2026-001",
  "fecha_cierre": "2026-01-13",
  "tipo_negocio": "Taller Automotriz",
  "ingreso_soles": 18750.00,  // $5,000 × 3.75
  "estado_pago": "50% Adelanto Recibido"
}
```

---

#### **KPI-08: Ticket Promedio (Auto-Calculado)**
- **Definición:** Valor promedio por proyecto cerrado
- **Fuente:** Auto-calculado
- **Fórmula:** `Ingresos Totales / Ventas Cerradas`
- **Meta:** S/. 13,125 por proyecto (≈ $3,500 USD)
- **Insight:** Si baja < S/. 9,375, estás vendiendo proyectos muy pequeños (baja rentabilidad)

**Ejemplo:**
```
Semana 2: S/. 37,500 ingresos / 3 ventas = S/. 12,500/venta ✅
Semana 5: S/. 18,750 ingresos / 3 ventas = S/. 6,250/venta ⚠️ (proyectos muy chicos)
```

---

### 2.4 Métricas Financieras (Requieren Input del Contador)

#### **KPI-09: Costos Directos por Proyecto**
- **Definición:** Costos asignables a un proyecto específico
- **Fuente:** Excel Template del Contador
- **Frecuencia:** Semanal (lunes siguiente a cierre de proyecto)
- **Componentes:**
  1. **Materiales:** JP01Y, JS02Y, poliuretano, flakes, primers
  2. **Mano de Obra:** Pago a instaladores (si subcontratado)
  3. **Transporte Directo:** Flete de material al sitio, combustible del día

**Estructura Excel:**
```
| Venta_ID      | Fecha | Materiales_S/ | ManoObra_S/ | Transporte_S/ | Total_Costo_S/ |
|---------------|-------|---------------|-------------|---------------|----------------|
| LUX-2026-001  | 13-Ene| 6,250         | 4,000       | 500           | 10,750         |
| LUX-2026-002  | 14-Ene| 4,500         | 3,200       | 400           | 8,100          |
```

**Cálculo de Margen por Proyecto:**
```
Margen Bruto = (Ingreso - Costo Directo) / Ingreso × 100

Ejemplo:
Venta LUX-2026-001: (S/. 18,750 - S/. 10,750) / S/. 18,750 = 42.7% ✅
```

---

#### **KPI-10: Costos Indirectos (Overhead)**
- **Definición:** Gastos operativos no asignables a un proyecto específico
- **Fuente:** Excel Template del Contador
- **Frecuencia:** Semanal (totalizado al mes)
- **Componentes:**
  1. **Marketing:** Sample Book, impresión de folletos, ads Facebook
  2. **Administrativos:** Oficina, servicios, teléfono, internet
  3. **Transporte General:** Combustible de visitas sin venta
  4. **Sueldos Fijos:** Salario base del vendedor (si aplica)
  5. **Otros:** Mantenimiento de equipo, depreciación

**Estructura Excel:**
```
| Semana | Marketing_S/ | Admin_S/ | Transporte_S/ | Sueldos_S/ | Otros_S/ | Total_Indirecto_S/ |
|--------|--------------|----------|---------------|------------|-----------|--------------------|
| W01    | 800          | 500      | 600           | 2,000      | 200       | 4,100              |
| W02    | 300          | 500      | 550           | 2,000      | 100       | 3,450              |
```

---

#### **KPI-11: Utilidad Operativa**
- **Definición:** Ganancia real después de todos los costos (directos + indirectos)
- **Fuente:** Auto-calculado
- **Fórmula:** `Ingresos - Costos Directos - Costos Indirectos`
- **Meta:** 30-40% del ingreso (industria construcción: 25-35%)

**Ejemplo Mensual:**
```
Ingresos Mes 1:           S/. 45,000
Costos Directos (3 obras): S/. 24,000  (53% del ingreso)
Costos Indirectos:         S/. 8,500   (19% del ingreso)
────────────────────────────────────
Utilidad Operativa:        S/. 12,500  (28% del ingreso) ⚠️ Ajustar precios
```

---

#### **KPI-12: Margen Operativo (%)**
- **Definición:** % de ganancia sobre ingresos
- **Fuente:** Auto-calculado
- **Fórmula:** `(Utilidad Operativa / Ingresos) × 100`
- **Meta:** ≥ 30%
- **Alarma:** Si < 20%, negocio no es sostenible

---

## 3. Vistas del Dashboard

### 3.1 Vista Semanal (Operativa)
**Usuario:** Vendedor / Gerente de Ventas  
**Actualización:** Cada viernes antes de las 6pm

**Elementos Visualizados:**
- 📊 **Gráfico de Embudo Semanal:**
  ```
  Visitas (25)
     ↓ 40%
  Oportunidades (10)
     ↓ 30%* (*de semana anterior)
  Ventas (3)
  ```

- 📈 **Tendencia de 4 Semanas:**
  - Líneas: Visitas, Oportunidades, Ventas
  - Detecta si hay caída de actividad

- 🎯 **Progreso a Meta Mensual:**
  - "Visitas: 52 / 100 (52%)" con barra de progreso
  - "Ventas: 2 / 3 (67%)" ✅

- 🏆 **Ranking por Tipo de Negocio:**
  ```
  1. Taller Automotriz: 60% de ventas, Conversión 45%
  2. Detailing: 30% de ventas, Conversión 50%
  3. Maestranza: 10% de ventas, Conversión 20%
  ```

---

### 3.2 Vista Mensual (Gerencial)
**Usuario:** Dueño / Gerente General  
**Actualización:** Primera semana del nuevo mes

**Elementos Visualizados:**
- 💰 **P&L Simplificado (Estado de Resultados):**
  ```
  Ingresos:              S/. 45,000  100%
  - Costos Directos:     S/. 24,000   53%
  ─────────────────────────────────
  Margen Bruto:          S/. 21,000   47%
  
  - Costos Indirectos:   S/.  8,500   19%
  ─────────────────────────────────
  Utilidad Operativa:    S/. 12,500   28%
  ```

- 📊 **Comparación Mes vs Meta:**
  - Ventas: 3 / 3 ✅
  - m²: 450 / 2,000 ⚠️ (22% de meta)
  - Ingresos: S/. 45k / S/. 45k ✅

- 🔍 **Análisis de Rentabilidad por Segmento:**
  ```
  Taller Automotriz:
    - Ticket Promedio: S/. 15,000
    - Margen Bruto: 45%
    - Recomendación: Foco principal
  
  Detailing:
    - Ticket Promedio: S/. 8,500
    - Margen Bruto: 52%
    - Recomendación: Buena rentabilidad pero bajo volumen
  ```

---

## 4. Alertas Automáticas

### 4.1 Alarmas Rojas (Requieren Acción Inmediata)
| Condición | Alerta | Acción Sugerida |
|-----------|--------|----------------|
| Conversión V→O < 20% por 2 semanas | 🔴 "Pitch no está funcionando" | Revisar Sample Book, actualizar demo |
| Conversión O→V < 10% por 3 semanas | 🔴 "Pricing o velocidad de respuesta" | Analizar objeciones comunes, reducir tiempo de cotización |
| Margen Operativo < 15% | 🔴 "Negocio no rentable" | Subir precios 15% o reducir costos indirectos |
| Cero ventas en 3 semanas | 🔴 "Pipeline vacío" | Intensificar visitas, revisar estrategia |

### 4.2 Alarmas Amarillas (Monitorear)
| Condición | Alerta | Acción Sugerida |
|-----------|--------|----------------|
| Visitas < 20/semana por 2 semanas | ⚠️ "Actividad baja" | Revisar ruta de visitas, motivación |
| Ticket Promedio < S/. 9,000 | ⚠️ "Proyectos muy pequeños" | Enfocar en talleres > 80m² |
| Costos Indirectos > 25% ingresos | ⚠️ "Overhead alto" | Revisar gastos administrativos |

---

## 5. Especificación del Excel Template (Contador)

### Archivo: `Gastos_Semanal_Template_V2.xlsx`

#### **Hoja 1: Gastos** (Tabla Unificada)
```
| Fecha | Semana | Descripción | Tipo_Gasto | Categoría | Venta_ID | Tipo_Negocio | Monto_S/ |
|-------|--------|-------------|------------|-----------|----------|--------------|----------|
| [Date]| [W##]  | [Text]      | [Dropdown1]| [Dropdown2]| [Manual]| [Dropdown3]  | [#]      |
```

**Validaciones y Dropdowns:**

1. **Tipo_Gasto (Dropdown):** Lista desplegable
   - Opciones: `Material`, `Mano de Obra`, `Transporte`, `Otro`
   - Objetivo: Clasificar el tipo de gasto

2. **Categoría (Dropdown):** Lista desplegable
   - Opciones: `Costo Directo`, `Costo Indirecto`
   - Objetivo: Determinar si está asociado a un proyecto específico o es gasto general

3. **Tipo_Negocio (Dropdown):** Lista desplegable (opcional)
   - Opciones: `Taller Automotriz`, `Detailing`, `Maestranza`, `Factoría`, `Otro`
   - Solo llenar si Categoría = "Costo Directo"

**Reglas:**
- Si `Categoría = "Costo Directo"` → `Venta_ID` y `Tipo_Negocio` son obligatorios
- Si `Categoría = "Costo Indirecto"` → `Venta_ID` y `Tipo_Negocio` deben quedar vacíos

**Ejemplo de datos:**
```
15-Ene | W02 | Resina JS02Y Taller Surquillo    | Material      | Costo Directo   | LUX-2026-003 | Taller Automotriz | 5200
15-Ene | W02 | Pago instaladores                | Mano de Obra  | Costo Directo   | LUX-2026-003 | Taller Automotriz | 3500
16-Ene | W02 | Gasolina visitas (no instalación)| Transporte    | Costo Indirecto |              |                   | 550
17-Ene | W02 | Sueldo base vendedor             | Otro          | Costo Indirecto |              |                   | 2000
```

---

#### **Hoja 2: Instrucciones**
Guía completa para el contador con:
- Explicación de cada columna
- Ejemplos de Costo Directo vs Indirecto
- Preguntas frecuentes
- Tips para ahorrar tiempo

---

### Procesamiento del Dashboard (ETL)

El dashboard leerá este Excel y automáticamente:

1. **Agrupa por Venta_ID** → Calcula Costos Directos por proyecto
2. **Agrupa por Semana + Categoría = "Indirecto"** → Calcula Costos Indirectos semanales
3. **Calcula KPI-09:** Costos Directos por Proyecto
4. **Calcula KPI-10:** Costos Indirectos (suma de todos los indirectos)
5. **Calcula KPI-11:** Utilidad Operativa = Ingresos - Directos - Indirectos
6. **Calcula KPI-12:** Margen Operativo % = (Utilidad / Ingresos) × 100

---

## 6. Arquitectura Técnica del Dashboard

### 6.1 Opción Recomendada: **Aplicación Web (Streamlit + Python)**

**Ventajas:**
- ✅ Accesible desde cualquier dispositivo (PC, tablet, celular)
- ✅ No requiere instalación (solo navegador)
- ✅ Fácil de actualizar (un solo código fuente)
- ✅ Gráficos interactivos con Plotly
- ✅ Puede leer Excel del contador automáticamente

**Stack Tecnológico:**
```
Frontend: Streamlit (Python framework)
Backend: Python 3.10+
Base de Datos: SQLite (simple, archivo local)
Lectura de Excel: pandas + openpyxl
Visualización: Plotly / Altair
Hosting: Local (localhost) o Streamlit Cloud (gratis)
```

### 6.2 Flujo de Uso

**Vendedor (cada viernes):**
1. Abre navegador → `http://localhost:8501` o `https://lux-dashboard.streamlit.app`
2. Selecciona "Ingresar Datos Semanales"
3. Llena formulario (5 minutos):
   - Visitas por tipo de negocio
   - Oportunidades por tipo
   - Ventas cerradas (si hubo)
   - m² e Ingresos por cada venta
4. Click "Guardar" → Datos se almacenan en SQLite

**Contador (cada lunes):**
1. Abre Excel Template en Google Drive: `G:\My Drive\NewLux\KPIs_Accounting\Gastos_Semanal_Template_V2.xlsx`
2. Por cada gasto de la semana anterior (5-15 minutos):
   - Agregar nueva fila en hoja "Gastos"
   - Llenar: Fecha, Semana, Descripción, Monto
   - **Dropdown 1:** Tipo_Gasto (Material/Mano Obra/Transporte/Otro)
   - **Dropdown 2:** Categoría (Costo Directo/Costo Indirecto)
   - Si es Directo: Llenar Venta_ID + Tipo_Negocio
   - Si es Indirecto: Dejar Venta_ID vacío
3. Guarda archivo (auto-sincroniza con Google Drive - no requiere acción adicional)
Gastos_Semanal_Template_V2.xlsx`
   - Filtra por `Categoría = "Costo Directo"` → Agrupa por Venta_ID
   - Filtra por `Categoría = "Costo Indirecto"` → Agrupa por Semana
**Dashboard (automático):**
1. Al abrir la app, lee:
   - Base de datos SQLite (datos de ventas)
   - Excel del contador desde Google Drive: `G:\My Drive\NewLux\KPIs_Accounting\Costos_Semanal_Template.xlsx`
2. Calcula todos los KPIs
3. Muestra gráficos y tablas actualizadas

---

## 7. Roadmap de Implementación

### Fase 1: Setup Básico (Semana 1) 🔄 EN PROGRESO
- [✅] Diseñar Excel Template para contador
- [✅] Crear Excel Template con fórmulas y dropdowns
- [✅] Configurar Google Drive para contador
- [ ] Crear base de datos SQLite con tablas
- [ ] Desarrollar formulario de entrada de ventas (Streamlit)
- [ ] Implementar cálculo de KPIs básicos (1-8)

### Fase 2: Visualizaciones (Semana 2)
- [ ] Vista Semanal con embudo y tendencias
- [ ] Vista Mensual con P&L
- [ ] Gráficos por tipo de negocio
- [ ] Exportar reportes a PDF

### Fase 3: Integración Financiera (Semana 3)
- [ ] Lector automático de Excel del contador
- [ ] Cálculo de márgenes por proyecto
- [ ] Dashboard de rentabilidad

### Fase 4: Alertas y Optimización (Semana 4)
- [ ] Sistema de alertas automáticas
- [ ] Comparación vs metas
- [ ] Móvil-responsive

---

## 8. Preguntas Pendientes para Continuar

1. **¿Prefieres hostear el dashboard localmente (tu PC) o en la nube (accesible desde cualquier lugar)?**
   - Local: Gratis, pero solo funciona cuando tu PC está prendida
   - Nube (Streamlit Cloud): Gratis también, accesible 24/7 desde celular

2. **✅ RESUELTO: El contador usa Google Drive**
   - Carpeta compartida: `G:\My Drive\NewLux\KPIs_Accounting`
   - El dashboard lee automáticamente desde Google Drive Desktop
   - Template Excel ya creado y funcionando

3. **¿Quieres que yo desarrolle el código completo ahora o prefieres revisar esta especificación primero?**

---

**Próximo Paso Sugerido:** Crear el Excel Template y la estructura de base de datos para empezar a registrar datos esta semana.
