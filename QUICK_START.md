# 🚀 Quick Start - Deploy en 15 Minutos

Sigue estos pasos **exactamente** para evitar problemas:

---

## ✅ PASO 1: Preparar Git (3 min)

Abre **Terminal** en VS Code (Ctrl + `) y copia/pega cada comando:

```bash
cd "c:\Users\USER\OneDrive\Lux\Plan2026\Control_Dashboard"
git init
git add .
git commit -m "Initial commit - Lux Sales Dashboard"
```

**✅ Verifica**: Deberías ver mensaje "X files changed, X insertions(+)"

---

## ✅ PASO 2: Subir a GitHub (5 min)

### Opción A: Website (Recomendado)

1. Ve a: https://github.com/new
2. **Repository name**: `lux-sales-dashboard`
3. **Private** (o Public, tu decides)
4. ❌ **NO marques** ningún checkbox
5. Click **"Create repository"**
6. Copia el bloque de comandos que aparece (sección "push an existing repository")
7. Pega en tu terminal

**Ejemplo de lo que copiarás:**
```bash
git remote add origin https://github.com/TU-USUARIO/lux-sales-dashboard.git
git branch -M main
git push -u origin main
```

**✅ Verifica**: Refresca la página de GitHub, deberías ver tus archivos

---

## ✅ PASO 3: Deploy en Streamlit Cloud (7 min)

1. **Ir a**: https://share.streamlit.io/signup
2. Click **"Continue with GitHub"**
3. Autorizar acceso
4. En el dashboard, click **"New app"**
5. Llenar formulario:
   ```
   Repository: TU-USUARIO/lux-sales-dashboard
   Branch: main
   Main file path: app/dashboard.py
   ```
6. Click **"Deploy!"**
7. **ESPERAR 2-5 minutos** (verás logs de instalación)

**✅ Verifica**: Cuando termine, verás tu app corriendo en el navegador

---

## 🎉 ¡LISTO!

Tu dashboard está en: `https://TU-USUARIO-lux-sales-dashboard.streamlit.app`

**Comparte esa URL con tus vendedores** 📱

---

## 🐛 Si Algo Sale Mal:

### Error en Paso 1: "git: command not found"
```bash
# Instalar Git: https://git-scm.com/download/win
# Reiniciar VS Code después de instalar
```

### Error en Paso 2: "Authentication failed"
```bash
# Opción 1: Usar GitHub Desktop (más fácil)
# Opción 2: Configurar credenciales
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Si pide password, usa Personal Access Token:
# https://github.com/settings/tokens
```

### Error en Paso 3: "Could not find requirements.txt"
```bash
# Verificar que requirements.txt existe:
ls requirements.txt

# Si no existe, crearlo:
echo "streamlit>=1.31.0" > requirements.txt
echo "pandas>=2.0.0" >> requirements.txt
echo "openpyxl>=3.1.0" >> requirements.txt
git add requirements.txt
git commit -m "Add requirements.txt"
git push
```

### App desplegada pero con errores
1. En Streamlit Cloud, click **"Manage app"**
2. Click **"Logs"** para ver qué falló
3. Copiar el error y preguntarme

---

## 📝 Notas Importantes:

⚠️ **Base de Datos**: SQLite se reinicia cada deploy. Para persistencia real, migrar a PostgreSQL.

⚠️ **Excel de Costos**: No funciona en cloud. La pestaña "Gastos" mostrará "No data".

✅ **Lo que SÍ funciona en cloud**:
- Registro de visitas
- Registro de oportunidades  
- Registro de ventas
- Ver historial
- KPIs básicos

---

**¿Atascado?** Dime en qué paso y exactamente qué error ves.
