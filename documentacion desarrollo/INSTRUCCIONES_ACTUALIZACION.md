# 🔄 Cómo Actualizar el Dashboard en GitHub Pages

## 📋 Cuando Actualices el Dashboard

Cada vez que hagas cambios en el dashboard (nuevas rondas, mejoras visuales, etc.), sigue estos pasos:

---

## 🚀 Método Rápido (3 comandos)

```bash
# 1. Navegar al proyecto
cd C:\Users\alvar\Documents\AlvGolf

# 2. Regenerar datos (si añadiste rondas nuevas)
python generate_dashboard_data.py

# 3. Subir cambios a GitHub
git add dashboard_dynamic.html output/dashboard_data.json
git commit -m "Update: [descripción breve de cambios]"
git push origin main
```

**⏱️ Tiempo total:** ~30 segundos  
**⏱️ GitHub Pages actualiza en:** 1-2 minutos

---

## 📝 Paso a Paso Detallado

### 1️⃣ Regenerar Datos (si es necesario)

**Cuándo:** Después de añadir nuevas rondas de golf

```bash
cd C:\Users\alvar\Documents\AlvGolf
python generate_dashboard_data.py
```

**Output esperado:**
```
[OK] Datos del dashboard generados exitosamente
[FILE] Archivo guardado en: output/dashboard_data.json
[TIME] Ejecución completada en 3.1s
```

---

### 2️⃣ Verificar Cambios Localmente

**Recomendado:** Probar antes de subir

```bash
python start_dashboard_server.py
# Abre: http://localhost:8000/dashboard_dynamic.html
# Verifica que todo funciona correctamente
```

---

### 3️⃣ Ver Qué Archivos Cambiaron

```bash
git status
```

**Ejemplo de output:**
```
modified:   dashboard_dynamic.html
modified:   output/dashboard_data.json
```

---

### 4️⃣ Añadir Cambios al Staging

**Opción A: Añadir archivos específicos**
```bash
git add dashboard_dynamic.html
git add output/dashboard_data.json
```

**Opción B: Añadir todo lo modificado**
```bash
git add .
```

---

### 5️⃣ Hacer Commit

```bash
git commit -m "Update: [descripción de cambios]"
```

**Ejemplos de mensajes:**
```bash
git commit -m "Update: Añadidas rondas de enero 2026"
git commit -m "Update: Corregido bug en gráfico de momentum"
git commit -m "Update: Mejorada responsiveness en móvil"
git commit -m "Update: Nuevas 5 rondas + milestone broke_80"
```

---

### 6️⃣ Subir a GitHub

```bash
git push origin main
```

**Output esperado:**
```
To https://github.com/AlvGolf/AlvGolf-Identity-EngineV3.git
   53fc944..a1b2c3d  main -> main
```

---

### 7️⃣ Verificar Actualización

1. **Espera 1-2 minutos** (GitHub Pages tarda en actualizar)
2. **Abre el dashboard:**
   ```
   https://alvgolf.github.io/AlvGolf-Identity-EngineV3/dashboard_dynamic.html
   ```
3. **Limpia caché del navegador:**
   - Windows: `Ctrl + F5`
   - Mac: `Cmd + Shift + R`

---

## 🔧 Comandos Útiles

### Ver Historial de Commits
```bash
git log --oneline
```

### Ver Diferencias Antes de Commitear
```bash
git diff dashboard_dynamic.html
git diff output/dashboard_data.json
```

### Deshacer Cambios Locales (antes de commit)
```bash
git checkout -- dashboard_dynamic.html
```

### Ver Estado del Repositorio
```bash
git status
```

---

## 📱 Notificar a Usuarios Después de Actualizar

**Mensaje sugerido para WhatsApp:**

```
🔄 Dashboard Actualizado

He actualizado el dashboard con:
- [Describe los cambios]

Refresca la página (Ctrl+F5) para ver los cambios:
🔗 https://alvgolf.github.io/AlvGolf-Identity-EngineV3/

¡Échale un vistazo!
```

---

## ⚠️ Troubleshooting

### Problema: "No veo los cambios después de actualizar"

**Solución:**
1. Verifica que el push fue exitoso: `git log --oneline`
2. Espera 2-3 minutos (GitHub Pages puede tardar)
3. Limpia caché del navegador (Ctrl+F5)
4. Prueba en modo incógnito

### Problema: "Error al hacer push"

**Causa:** Alguien más hizo cambios en GitHub

**Solución:**
```bash
git pull origin main
git push origin main
```

### Problema: "Conflicto al hacer pull"

**Causa:** Cambios locales y remotos incompatibles

**Solución:**
```bash
# Ver archivos en conflicto
git status

# Resolver manualmente o usar la versión remota
git checkout --theirs [archivo]

# Commitear la resolución
git add .
git commit -m "Resuelto conflicto"
git push origin main
```

---

## 📊 Workflow Completo - Cheat Sheet

```bash
# Después de añadir nuevas rondas:
cd C:\Users\alvar\Documents\AlvGolf
python generate_dashboard_data.py
python start_dashboard_server.py  # Probar localmente
git add .
git commit -m "Update: Añadidas [X] rondas nuevas"
git push origin main

# Esperar 1-2 minutos
# Abrir: https://alvgolf.github.io/AlvGolf-Identity-EngineV3/
# Presionar Ctrl+F5 para limpiar caché
```

---

**Tiempo total del workflow:** ~5 minutos (incluyendo testing local)

**Última actualización:** 2026-02-07
