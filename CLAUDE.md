# Contexto del proyecto

Proyecto final de Cálculo Multivariable (Universidad Cooperativa de Colombia, 2026B, docente M.Sc. Alejandro Molina): regresión lineal $y = ax + b$ formulada como la minimización de $S(a,b) = \sum (y_i - a x_i - b)^2$.

## Fuentes de verdad
- `docs/enunciado_proyecto.md`: enunciado completo (requisitos, secciones §1–§13).
- `docs/rubrica_evaluacion.md`: rúbrica con pesos.
- `docs/originales/*.pdf`: PDFs originales. Ante cualquier duda, el PDF manda.
- `README.md`: resumen y mapa de fases.

## Reglas que no se deben romper
- El desarrollo analítico (derivadas parciales, $\nabla S = 0$, solución del sistema y Hessiano) es **manual**. El código lo verifica; no lo sustituye.
- El código debe implementar el método propio (ecuaciones normales deducidas a mano). Las librerías (`numpy.polyfit`, `scipy.stats.linregress`, `sklearn`) se usan **solo** como verificación adicional en la tabla comparativa (§9).
- Los gráficos obligatorios son: dispersión, recta ajustada junto a otras rectas $(a,b)$, superficie $S(a,b)$, trazas/secciones transversales, curvas de nivel con $(a^*,b^*)$ marcado, residuos vs $x$ e histograma de residuos.
- Hay que hacer al menos uno de los análisis adicionales del §13 (A–D).
- La interpretación de RMSE/$R^2$ debe hacerse en el contexto de los datos, no con juicios genéricos.
- Todo el material entregable va en español.

## Problema elegido
Ley de Hubble con los 24 datos de Hubble (1929): `x` = distancia (Mpc), `y` = velocidad radial (km/s). Resultados: a* ≈ 454.16, b* ≈ −40.78, S mín ≈ 1 193 442, R² ≈ 0.624. Análisis adicional: opción B (influencia de un dato).

## Estructura
`datos/` dataset y fuente · `analisis_manual/` guion del desarrollo a mano · `codigo/` `regresion.py` (método propio), `verificacion.py`, `graficos.py` (figuras por capas en `graficos/pasos/`, cuadrícula común `CUAD`/`LIM`), `graficos_3d.py` (HTML 3D en `presentacion/interactivo/` y cuadros en `presentacion/animacion/`) · `graficos/` figuras · `docs/guia/` fuente Typst del PDF · `presentacion/` diapositivas de la defensa en Beamer (`defensa.tex`).

## Comandos
- Entorno: `.venv/bin/python` (dependencias en `codigo/requirements.txt`).
- Regenerar resultados, figuras y PDF: `.venv/bin/python docs/guia/build.py`.
- Los números del PDF salen de `docs/guia/resultados.json`; no escribirlos a mano en `guia.typ`.
- Diapositivas: `cd presentacion && pdflatex defensa.tex && pdflatex defensa.tex` (con animaciones por pasos); `defensa-handout.tex` genera la versión sin animaciones (las cifras están escritas a mano en el `.tex`; si cambian los resultados, actualizarlas).
