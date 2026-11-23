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

## Versión Excel (formato Impulsa)
- `python3 panel_excel.py <Plantilla_Impulsa.xlsx> <salida.xlsx>` genera el mismo panel en Excel (Portada · Panel · Hitos) a partir de `datos.json`. Se regenera con cada actualización de datos si Diego lo pide.

## Avance de obra en la etiqueta

- Las etiquetas verdes de obra ("En obra · 89 %", "T1 en obra · 16 %") se rellenan solas hasta el porcentaje que aparece en el texto de `fase`/`estado`. Basta con actualizar ese texto.

## Enlace a Google Maps (20/11/2026, en los cuatro paneles)
Cada promoción puede llevar en datos.json los campos `maps` (URL de Google Maps) y `maps_precision` (exacta / calle / zona). Los paneles pintan un icono de ubicación junto a la localidad que abre ese enlace en una pestaña nueva. Los paneles horizontales, abiertos en un teléfono, redirigen a su versión vertical.

## Enlaces y orientación automática (20/11/2026)

- Enlaces para compartir (se adaptan solos a la pantalla): General = `general-horizontal.html` · Madrid con hitos = `horizontal.html`. En teléfonos y pantallas verticales abren la versión vertical (`general.html?auto` / `index.html?auto`) y vuelven a la horizontal si la pantalla es apaisada.
- Las versiones verticales abiertas directamente (teles: raíz/`index.html` y `general.html`) quedan fijas; solo cambian si llevan `?auto`.
- El script va al principio del `<head>` de `index.html` y `horizontal.html`; `build.py` lo adapta para las dos páginas generales. No tocar los nombres de archivo: son los enlaces ya enviados.
- Paneles horizontales: las medidas usan `calc(N * var(--u))` con `--u: min(1vh, 0.5625vw)` (no `vh` directo), para que en pantallas menos apaisadas que 16:9 no se corten nombres. En 16:9 o más ancho es idéntico. En móvil no se muestran las horas (decisión 20/11).
- 23/11/2026: alta de Arcosur E-38 (174 viv, oferta aceptada) en Aragón. El panel vertical de Madrid quita solo los hitos más lejanos (mínimo 3) si la lista de promociones no cabe en la tele (`ajustaHitos`).
- 23/11/2026: fecha de entrega y retraso por promoción. En `datos.json`, cada promoción admite `entrega` ("AAAA-MM"), `retraso_meses` (número; si es mayor que 0 se pinta en rojo "Retraso N meses") y `entrega_nota` (texto corto, p. ej. "T1"). Sin `entrega` no se muestra nada. Teles verticales: en el hueco entre nombre y fase; horizontal de Madrid: en la línea de la localidad; horizontal General y móvil: línea propia bajo la localidad.
- 23/11/2026: Colombia se muestra como el resto, ventas sobre viviendas totales (75/278, 31/990), y la cabecera lleva el total de la zona. El campo `pe` de datos.json ya no se usa en pantalla.
- 23/11/2026: paneles de Madrid con "Objetivos semanales" (izquierda / arriba) y "Próximos hitos" (derecha / abajo). Los objetivos salen de `objetivos.lista` en datos.json (ambito, texto y fecha opcional "AAAA-MM-DD" o "AAAA-MM") y se actualizan con cada acta de coordinadores. Un hito con `"objetivo": true` no se pinta en hitos mientras haya objetivos (su fecha va en el objetivo). Mínimo 4 hitos a la vista. Sin `objetivos`, el panel vuelve a mostrar solo hitos. Fechas de entrega en naranja.

## 23/11/2026 · Solo objetivos (en prueba)
- `var SOLO_OBJ` en index.html y horizontal.html: `false` = objetivos + hitos (definitivo actual); `true` = solo objetivos semanales (vertical a 2 columnas, horizontal a toda la columna). regen_prueba.py lo pone a `true` en prueba.html y prueba-horizontal.html. Pasar a definitivo = cambiar a `true` en las dos fuentes, tras ok y auditoría.
- Entrega Catedral · Nova Arcosur: abr 2029 (planificación v4 de 18/11/2026).
- 23/11 11:25: Diego aclara que quería el título "Objetivos" (no quitar hitos). Título cambiado en definitivos; SOLO_OBJ queda en false en todas las páginas (regen_prueba ya no lo activa).
- 23/11 11:47: el bloque "Próximos hitos" pasa a llamarse "Agenda" (Madrid).
- 23/11 11:48: se quita la palabra "Entrega"; queda solo la fecha en naranja (Danubio conserva "T1" porque la fecha es solo de la Torre 1). Cuatro paneles.

## REGLA (Diego, 23/11/2026 11:53): auditoría con cada cambio
Los paneles se consideran definitivos. Cualquier cambio (diseño, texto o dato) va seguido de auditoría antes de darlo por hecho: audE.js (41 pantallas, recortes/solapes/encaje), ob3.js (objetivos y agenda, ≥4 hitos), fun.js (cifras, enlaces, sin datos, 1-dic, naranja), ori4.js (vertical/horizontal) y captura visual revisada. Se informa a Diego del resultado y de los fallos corregidos.
- 23/11 11:55: entregas Arcosur E-38 jul 2029 y Llevant Parc ene 2027 (dato de Diego). Auditado.

## 23/11/2026 12:07 · Logos por zona (solo en prueba)
- Carpeta `logos/` (madrid, aragon, cataluna, andalucia, colombia .png (Colombia = símbolo HC gris-naranja + nombre en gris, compuesto en horizontal a partir de 2.1.png y 1.5.png), 160 px de alto, fondo transparente; origen: Escritorio › LOGOS, solo lectura). regen_prueba.py añade `logoZ()` y el CSS `.zl` a las cuatro prueba*.html. A color por defecto; con `?gris` en la dirección, en gris. En modo oscuro salen en blanco. Auditoría 12:15 (Diego vio fallo): logos alineados en columna (`.zn` min-width 6.5em), tamaños igualados (Solucions 0.92, Colombia 0.84) y `?gris` conservado al redirigir en móvil. Pendiente decisión de Diego (color/gris, Madrid sí/no, Solucions o Fem Ciutat).

## 23/11/2026 12:23 · Logos por zona — DEFINITIVO (a color)
- En las fuentes index.html y horizontal.html (y por build.py en los generales): `logoZ()` + `<i class="zn">` (ancho fijo 6.5em para que todos los logos arranquen en la misma vertical) + `.zl` (alto 1.23em × factor por logo: Solucions 0.92, Colombia 0.84). Modo oscuro: logos en blanco. Si un logo no carga, la cabecera queda como antes (alt vacío).
- Archivos en `logos/` (madrid, aragon, cataluna, andalucia, colombia). Colombia = símbolo HC + nombre en gris. Origen: Escritorio › LOGOS (solo lectura).
- Añadir zona nueva: poner su PNG (160 px de alto, fondo transparente) en `logos/` y añadirla al mapa `M` de `logoZ()` en las dos fuentes.
- Auditoría final 23/11: 42 pantallas de logos + 41 generales + 14 de objetivos/agenda + funcionamiento + orientación + robustez (re-render, sin logos, modo oscuro, zoom 125/150 %): 0 fallos.
