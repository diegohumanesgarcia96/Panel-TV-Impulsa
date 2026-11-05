# Cómo se actualiza el panel

- `index.html` es la página. No se toca en el día a día.
- `datos.json` son los datos (promociones, Colombia, hitos). Es lo único que cambia.
- Cada vez que Diego pasa un acta o un mail, Claude regenera `datos.json` (`python3 panel.py --datos`) y lo sube al repositorio.
- La TV lee `datos.json` cada 30 minutos sin recargar la página (no sale de pantalla completa) y calcula las cuentas atrás de los hitos con la fecha real: los hitos pasados se marcan "hecho" durante 3 días y después desaparecen.
