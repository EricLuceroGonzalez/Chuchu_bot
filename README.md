# chuchu-bot

Bot de citas literarias. Elige una cita de MongoDB y la publica en **Bluesky** y **Mastodon**.
X queda desactivado (su API es de pago por uso desde 2026).

## Instalación (uv)

```bash
uv sync                 # crea .venv e instala dependencias desde uv.lock
cp .env.example .env    # rellena credenciales
uv run post_citas.py --dry-run   # prueba: no publica ni toca MongoDB
uv run post_citas.py             # publica de verdad
```

## Cron

```cron
0 9,15,21 * * * cd /ruta/al/bot && /home/USUARIO/.local/bin/uv run post_citas.py >> /dev/null 2>&1
```

## Redes

Se eligen con `ENABLED_PLATFORMS` en el `.env` (p. ej. `bluesky,mastodon`).

| Red | Límite | Credenciales |
|---|---|---|
| Bluesky | 300 grafemas, imagen ≤ 1 MB | `BSKY_HANDLE`, `BSKY_APP_PASSWORD` (contraseña de aplicación) |
| Mastodon | 500 caracteres (configurable) | `MASTODON_BASE_URL`, `MASTODON_ACCESS_TOKEN` |
| X (apagado) | 280 | `uv sync --extra x` + variables `X_*` |

Se elige una cita que quepa en **todas** las redes activas, así el texto es idéntico en cada una.
Si una red falla (sin créditos, rate limit…), se registra un aviso y se sigue con las demás.

## MongoDB

Tras publicar se actualiza el documento:

- `enviado` += 1, `publicado = true`, `fecha_ultimo_post`
- `publicaciones.<red> = {id, fecha}` para cada red donde se publicó

## Estructura

```
post_citas.py      # punto de entrada
formatter.py       # construye el texto del post
images.py          # descarga/comprime la portada
connect_DB.py      # conexión a MongoDB (sin cambios)
publishers/
  base.py          # interfaz Publisher
  bluesky.py
  mastodon.py
  x.py             # desactivado
JSON_to_MONGO/     # utilidades de carga de datos (sin cambios)
```
