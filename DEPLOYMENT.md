# 🚀 Deployment Guide - Streamlit Cloud

## ⚠️ IMPORTANTE: Google Drive Files Won't Work in Cloud

El archivo Excel en `G:\My Drive\...` **NO estará accesible** desde Streamlit Cloud porque es una ruta local de tu computadora.

### Opciones para Manejar Datos de Costos en la Nube:

**OPCIÓN 1 (Recomendada): Subir Excel Manualmente en la App**
- Añadir un botón "Subir Archivo Excel" en el dashboard
- El contador sube el archivo actualizado cada semana
- Los datos se almacenan temporalmente mientras la app está corriendo

**OPCIÓN 2: Google Sheets API**
- Convertir Excel a Google Sheets
- Usar API de Google Sheets para leer datos
- Requiere configuración adicional (OAuth, service account)

**OPCIÓN 3: Base de Datos para Costos**
- Añadir tabla de costos en SQLite
- Crear formulario web para que el contador ingrese costos
- Todo queda en la misma base de datos

**Para este despliegue inicial, la pestaña Gastos mostrará "No data" en la nube.**

---

## 📋 Pre-requisitos

1. ✅ Cuenta de GitHub (gratis)
2. ✅ Cuenta de Streamlit Cloud (gratis) - https://streamlit.io/cloud
3. ✅ Git instalado en tu computadora

---

## 🔧 PASO 1: Preparar Git Repository

Abre el terminal en VS Code y ejecuta:

```bash
# Navegar al directorio del proyecto
cd "c:\Users\USER\OneDrive\Lux\Plan2026\Control_Dashboard"

# Inicializar repositorio Git (si no existe)
git init

# Crear .gitignore para excluir archivos sensibles
echo "data/" > .gitignore
echo "*.db" >> .gitignore
echo ".streamlit/secrets.toml" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore

# Agregar todos los archivos
git add .

# Hacer commit inicial
git commit -m "Initial commit - Lux Sales Dashboard"
```

---

## 🌐 PASO 2: Crear Repositorio en GitHub

### Opción A: Desde GitHub Website (Más Fácil)

1. Ve a https://github.com
2. Click en **"New"** (botón verde) o **"+"** → "New repository"
3. Configuración:
   - **Repository name**: `lux-sales-dashboard`
   - **Description**: `Sistema de control de ventas B2B - Lux Pisos Industriales`
   - **Public** o **Private** (elige Private si quieres que sea privado)
   - ❌ NO marques "Initialize with README" (ya tenemos archivos)
4. Click **"Create repository"**

5. En la página siguiente, copia los comandos de "push an existing repository":

```bash
git remote add origin https://github.com/TU-USUARIO/lux-sales-dashboard.git
git branch -M main
git push -u origin main
```

### Opción B: Desde Terminal (Requiere GitHub CLI)

```bash
# Instalar GitHub CLI si no lo tienes: https://cli.github.com/

# Crear repo directamente desde terminal
gh repo create lux-sales-dashboard --private --source=. --push

# O público:
gh repo create lux-sales-dashboard --public --source=. --push
```

---

## ☁️ PASO 3: Deploy en Streamlit Cloud

### 3.1 Crear Cuenta en Streamlit Cloud

1. Ve a https://streamlit.io/cloud
2. Click **"Sign up"**
3. Selecciona **"Continue with GitHub"**
4. Autoriza Streamlit Cloud a acceder a tu GitHub

### 3.2 Crear Nueva App

1. En el dashboard de Streamlit Cloud, click **"New app"**

2. Configuración del Deploy:
   ```
   Repository: TU-USUARIO/lux-sales-dashboard
   Branch: main
   Main file path: app/dashboard.py
   App URL (custom): lux-sales-dashboard  (o el que prefieras)
   ```

3. Click **"Deploy!"**

### 3.3 Esperar Deploy (2-5 minutos)

- Verás logs de instalación en pantalla
- Streamlit instalará dependencias de `requirements.txt`
- Cuando termine, la app estará disponible

---

## 🔗 PASO 4: Obtener URL

Tu app estará disponible en:
```
https://TU-USUARIO-lux-sales-dashboard.streamlit.app
```

O la URL personalizada que elegiste.

---

## 🔐 PASO 5: Configurar Base de Datos (Persistencia)

⚠️ **IMPORTANTE**: En Streamlit Cloud, los archivos se reinician cada vez que la app se redeploya.

### Para Mantener Datos Persistentes:

**OPCIÓN A: Usar Streamlit Cloud Storage (Limitado)**
- Los archivos en el directorio de la app son temporales
- Cuando la app se reinicia, pierdes los datos

**OPCIÓN B: Base de Datos Externa (Recomendado para Producción)**

1. **SQLite + S3/Dropbox**: Guardar lux_sales.db en almacenamiento cloud
2. **PostgreSQL**: Usar servicio como Supabase (gratis) o Railway
3. **Google Sheets**: Para datos simples

### Setup Rápido con Supabase (GRATIS):

```bash
# 1. Crear cuenta en https://supabase.com (gratis)
# 2. Crear nuevo proyecto
# 3. En Streamlit Cloud → Settings → Secrets, añadir:

[supabase]
url = "TU-SUPABASE-URL"
key = "TU-SUPABASE-KEY"
```

---

## 📱 PASO 6: Compartir con Vendedores

Una vez deployado:

1. **Envía la URL** a tus vendedores: `https://lux-sales-dashboard.streamlit.app`

2. **Crear accesos (opcional)**:
   - Streamlit Cloud Free: App pública (cualquiera con URL)
   - Streamlit Cloud Teams ($250/mes): Autenticación con passwords

3. **Para acceso simple con password**:
   - Añadir un login básico en el código (puedo hacerlo)
   - Usuarios/contraseñas en secrets.toml

---

## 🔄 PASO 7: Actualizar la App

Cuando hagas cambios al código:

```bash
# 1. Hacer cambios en los archivos
# 2. Commit y push a GitHub
git add .
git commit -m "Descripción de cambios"
git push

# 3. Streamlit Cloud detecta cambios automáticamente
# 4. Redeploya en ~1 minuto
```

---

## 🐛 Troubleshooting

### Error: "Module not found"
- Añadir el módulo a `requirements.txt`
- Push cambios a GitHub
- Streamlit Cloud reinstalará dependencias

### Error: "File not found" (Excel)
- **Esperado**: El archivo `G:\My Drive\...` no existe en la nube
- **Solución**: Implementar Opción 1, 2 o 3 mencionadas arriba

### App muy lenta
- Base de datos SQLite crece mucho
- Considerar migrar a PostgreSQL
- Limpiar datos viejos

### Datos desaparecen al redeploy
- **Normal** con SQLite en filesystem
- **Solución**: Usar base de datos externa o almacenamiento persistente

---

## 📊 Monitoring

En Streamlit Cloud puedes ver:
- **Logs**: Click en "Manage app" → "Logs"
- **Resource usage**: CPU, memoria
- **Analytics**: Visitas, usuarios activos

---

## 💰 Costos

**Streamlit Cloud Community (FREE):**
- ✅ 1 app privada
- ✅ Apps públicas ilimitadas
- ✅ 1 GB RAM
- ✅ 1 CPU core
- ✅ Perfecto para empezar

**Si necesitas más después:**
- Streamlit Cloud Teams: $250/mes (autenticación, más recursos)
- Self-hosting: Desplegar en tu propio servidor

---

## 🎯 Próximos Pasos Después del Deploy

1. ✅ Probar la app desde un celular
2. ✅ Capacitar a vendedores en cómo usarla
3. ⏳ Decidir solución para datos de costos (Excel → DB o Google Sheets)
4. ⏳ Añadir autenticación simple si lo necesitas
5. ⏳ Completar cálculos de KPIs con visualizaciones

---

**¿Preguntas o problemas durante el deploy?** Avísame en qué paso estás y te ayudo.
