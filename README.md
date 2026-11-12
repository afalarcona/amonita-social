# amonita-social

Contenido de redes sociales de Amonita (amonita.cl). Las imágenes de este repo son públicas porque Metricool las descarga desde aquí para publicarlas en Instagram y Facebook.

## Cómo se produce cada semana

1. Escribir `2026/semana-NN/posts.json` con las láminas (ver `2026/semana-01/` como ejemplo de estilo y textos).
2. Descargar las fuentes en `/tmp/ig`:
   `cd /tmp/ig && npm pack @fontsource/schibsted-grotesk @fontsource/hanken-grotesk && for f in *.tgz; do tar xzf $f && mv package ${f%.tgz}; done`
3. Generar las imágenes: `python3 herramientas/render.py 2026/semana-NN` (Playwright + Chrome; 1080×1350 JPG).
4. Revisar las imágenes a la vista, hacer commit y push a `main`.
5. Programar en Metricool (marca `amonita.cl`, blogId 1816705) con las URL `https://raw.githubusercontent.com/afalarcona/amonita-social/main/...`.
6. Registrar los temas en `HISTORIAL.md`.

## Guía de marca

- Público: dueños y administradores de negocios en Chile (B2B), sobre todo restaurantes y locales de comida.
- Colores: carbón #2D2D2D, acento #D08A3A, texto de acento #9A581C, gris del símbolo #EEEAE5, fondo blanco.
- Tipografías: Schibsted Grotesk 800 (títulos) y Hanken Grotesk (texto).
- Tono: directo, cercano, en español de Chile, sin exagerar. Sin emojis en exceso (2 a 4 por texto).
- Ofertas: **Amonita** (método: levantamos → analizamos → implementamos → medimos; Product Manager como servicio; primera conversación sin costo) y **Amonita para locales** (tienda propia sin comisión por pedido, delivery y retiro, comandas automáticas, caja, club de socios, avisos por WhatsApp, analítica; demo en amonita.cl/locales). Sin Contacto (sincontacto.cl): solo cuando el PM lo apruebe.

## Reglas de contenido

- No inventar clientes, cifras, testimonios ni resultados. No nombrar clientes sin permiso escrito del PM.
- Cifras de la industria solo si están en amonita.cl o tienen una fuente citada; los ejemplos de cálculo se marcan como "ejemplo".
- No publicar precios ("te lo contamos en la demo").
- Mezcla semanal sugerida: 1 post educativo para dueños de locales (operación, ventas, fidelización), 1 sobre Amonita para locales, 1 sobre el método o PM como servicio. Al menos 1 carrusel por semana.
- Cada texto termina con una acción: guardar, comentar, o ir a amonita.cl / amonita.cl/locales.
