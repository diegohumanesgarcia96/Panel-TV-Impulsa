# Cómo se actualiza el panel

## Las 4 páginas
| Página | Formato | Para | Hitos |
|---|---|---|---|
| `index.html` | vertical 9:16 | Madrid | sí |
| `horizontal.html` | horizontal 16:9 | Madrid | sí |
| `general.html` | vertical 9:16 | Panel TV General Impulsa (todas las sedes) | no |
| `general-horizontal.html` | horizontal 16:9 | Panel TV General Impulsa (todas las sedes) | no |

- `index.html` y `horizontal.html` son las páginas fuente. `general.html` y `general-horizontal.html` se generan con `python3 build.py` (quita los hitos y reparte las zonas); no se editan a mano.
- `datos.json` son los datos (promociones, Colombia, hitos). Es lo único que cambia en el día a día; las 4 páginas lo leen.
- Cada vez que Diego pasa un acta o un mail, Claude actualiza `datos.json` y lo sube al repositorio.
- Las TV leen `datos.json` cada 30 minutos sin recargar la página (no salen de pantalla completa) y calculan las cuentas atrás de los hitos con la fecha real: los hitos pasados se marcan "hecho" durante 3 días y después desaparecen.
- Pantalla completa: botón ⛶ abajo a la derecha o tecla F.
- Cambios de diseño: primero en `prueba*.html` para verlos en la TV; con el ok de Diego se pasan a las páginas fuente y se ejecuta `build.py`.
