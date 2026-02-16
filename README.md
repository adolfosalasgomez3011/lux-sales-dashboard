# Lux Sales Dashboard

📊 Sistema de control de ventas B2B para Lux Pisos Industriales

## Características

- 📝 Registro de visitas con información del cliente
- 🎯 Gestión de oportunidades de venta
- 💰 Seguimiento de ventas cerradas
- 📊 KPIs y reportes de desempeño
- 💸 Integración con costos (Excel)

## Instalación Local

```bash
# Clonar repositorio
git clone <your-repo-url>
cd Control_Dashboard

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app/dashboard.py
```

## Base de Datos

El sistema utiliza SQLite para almacenar datos de:
- Negocios (clientes)
- Visitas realizadas
- Oportunidades activas
- Ventas cerradas

## Integración Excel

Los costos y gastos se leen desde un archivo Excel en Google Drive.
Ver `app/excel_reader.py` para configuración de ruta.

## Deployment

Ver `DEPLOYMENT.md` para instrucciones de despliegue en Streamlit Cloud.

---
Desarrollado para Lux Pisos Industriales - 2026
