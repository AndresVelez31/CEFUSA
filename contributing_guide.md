# 🤝 Guía de Contribución

¡Gracias por querer contribuir a este proyecto! Este documento define el **flujo de trabajo con Git** que seguimos en el equipo para mantener un código limpio, ordenado y fácil de mantener.

## 🌿 Flujo de trabajo con ramas (`git pull`)

### 1️⃣ Crear una rama de feature a partir de `main`

Antes de empezar una nueva funcionalidad:

```bash
git checkout main
git pull origin main     # actualizar tu main local
git checkout -b feature/mi-nueva-funcionalidad
```

### 2️⃣ Trabajar en tu rama

Haz cambios y crea tus commits:

```bash
git add .
git commit -m "Implementa X funcionalidad"
```

### 3️⃣ Mantener tu rama actualizada con `main`

Si alguien más actualizó `main` mientras trabajabas, integra esos cambios:

```bash
git pull origin main
```

🔹 **Esto hace:**
- Descarga cambios de `main` (fetch).
- Los fusiona en tu rama (merge).
- Abre el editor para que edites el mensaje de merge.

### 4️⃣ Resolver conflictos (si aparecen)

Si hay conflictos:

1. Edita los archivos para resolverlos.
2. Marca como resueltos:
   ```bash
   git add <archivo_resuelto>
   ```
3. Finaliza el merge:
   ```bash
   git commit
   ```

### 5️⃣ Subir tu rama al remoto

```bash
git push origin feature/mi-nueva-funcionalidad
```

### 6️⃣ Crear un Pull Request (PR)

1. Abre un **PR hacia** `main` en GitHub/GitLab/Bitbucket.
2. Espera la revisión de al menos un compañero.
3. Una vez aprobado, se hace merge en `main`.

## ✅ Buenas prácticas

- **Usa nombres de ramas descriptivos:**
  - `feature/registro-usuarios`
  - `bugfix/correccion-login`
  - `hotfix/error-produccion`

- **Haz commits claros y concisos:**
  ```bash
  git commit -m "Agrega validación de correo en formulario de registro"
  ```

- **Nunca trabajes directamente sobre `main`.**
- **El `main` siempre debe estar estable y funcionando.**

## 📌 Beneficios de este flujo

Con este flujo nos aseguramos de:

- Mantener `main` siempre limpio.
- Evitar conflictos grandes al integrar cambios.
- Documentar bien la historia del proyecto con merges claros.