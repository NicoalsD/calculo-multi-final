# Proyecto final: Cálculo Multivariable (UCC 2026B)

**Regresión lineal y optimización mediante funciones de varias variables**

## ¿De qué trata?

Se elige un **problema real** con datos que sigan una tendencia aproximadamente lineal y se busca la recta $y = ax + b$ que mejor los representa. "La mejor" significa la que minimiza el error cuadrático total:

$$S(a,b) = \sum_{i=1}^{n} (y_i - a x_i - b)^2$$

Lo importante es que **$S$ es una función de dos variables ($a$ y $b$)**. Encontrar la mejor recta equivale a encontrar el mínimo de una superficie, y eso se resuelve con las herramientas del curso: derivadas parciales, gradiente, Hessiano, curvas de nivel y trazas.

**Pregunta central:** *¿Cómo se puede utilizar el Cálculo Multivariable para determinar y analizar el modelo lineal que mejor representa un conjunto de datos?*

Hay que responderla desde tres perspectivas: **analítica (a mano) + geométrica + computacional**. El computador solo **verifica y visualiza**; no reemplaza el desarrollo matemático.

## Problema real elegido: la ley de Hubble

Datos originales de Edwin Hubble (1929): distancia (Mpc) y velocidad radial (km/s) de 24 galaxias. El modelo es $v = a\,d + b$, donde la pendiente $a$ es la constante de Hubble. Fuente y unidades en [`datos/FUENTE.md`](datos/FUENTE.md).

| Resultado | Valor |
|---|---|
| $a^*$ | 454.16 km/s por Mpc |
| $b^*$ | −40.78 km/s |
| $S(a^*, b^*)$ | 1 193 442 (km/s)² |
| $\det H$ | 920.0 (> 0, mínimo) |
| RMSE | 223 km/s |
| $R^2$ | 0.624 |
| Análisis adicional | Opción B: quitar NGC 4382 cambia la pendiente un 11 % |

Todo el desarrollo, los gráficos interpretados, el plan de trabajo y las preguntas de defensa están en **[`Guia_Proyecto_Calculo_Multivariable.pdf`](Guia_Proyecto_Calculo_Multivariable.pdf)**.

## Pasos del proyecto

| # | Fase | Qué hay que hacer | Cómo se hace | Sección del enunciado |
|---|------|-------------------|--------------|-----------------------|
| 1 | Datos | Problema real, tabla con $x$, $y$ y unidades, diagrama de dispersión, ¿parece lineal? | — | §5 |
| 2 | Modelo | Definir $y_{\text{pred},i}$, residuos $e_i$ y $S(a,b)$ | — | §6 |
| 3 | Derivadas parciales | $\partial S/\partial a$, $\partial S/\partial b$ con el procedimiento completo | **A mano** | §7.1 |
| 4 | Punto crítico | $\nabla S = 0$ da un sistema 2×2 (ecuaciones normales) | **A mano** | §7.2 |
| 5 | Parámetros | Resolver el sistema y obtener $a^*$, $b^*$ con los datos reales | **A mano** | §7.3 |
| 6 | Hessiano | Calcular $H$ y justificar que $(a^*, b^*)$ es un mínimo | **A mano** | §7.4 |
| 7 | Geometría | Superficie $z = S(a,b)$, trazas, secciones transversales y curvas de nivel con $(a^*, b^*)$ marcado | Computador | §7.5–7.8 |
| 8 | Código | Programar el método propio: cargar datos, calcular $a^*$, $b^*$, $S_{\min}$, el Hessiano y todos los gráficos | Computador | §8 |
| 9 | Comparación | Tabla Analítico vs Código propio vs Librería (p. ej. `numpy.polyfit`, `scipy.stats.linregress`) con sus diferencias | Ambos | §9 |
| 10 | Recta de ajuste | Superponer la recta a los datos y señalar los puntos más desviados o influyentes | Computador | §10 |
| 11 | Residuos | Gráfico $e_i$ vs $x_i$ e histograma. ¿Están centrados? ¿Hay patrón, atípicos o desviación sistemática? | Computador | §11 |
| 12 | Calidad | RMSE y/o $R^2$, interpretados en el contexto de los datos (no basta con decir "bueno" o "malo") | Computador | §12 |
| 13 | Análisis adicional | **Al menos uno**: A) sensibilidad, B) influencia de un dato, C) comparar con un modelo cuadrático, D) efecto del número de datos | Computador | §13 |

> ⚠️ **Regla clave:** no se puede usar solo una función de regresión de librería. Primero se programa el método deducido a mano; la librería sirve únicamente como verificación adicional.

### Resultados analíticos de referencia

Esto es lo que debería salir del desarrollo a mano. Sirve para verificar, pero el procedimiento hay que mostrarlo completo.

- $\dfrac{\partial S}{\partial a} = -2\sum x_i (y_i - a x_i - b)$, $\quad \dfrac{\partial S}{\partial b} = -2\sum (y_i - a x_i - b)$
- Ecuaciones normales: $a\sum x_i^2 + b\sum x_i = \sum x_i y_i$, $\quad a\sum x_i + bn = \sum y_i$
- $a^* = \dfrac{n\sum x_i y_i - \sum x_i \sum y_i}{n\sum x_i^2 - (\sum x_i)^2}$, $\quad b^* = \bar{y} - a^*\bar{x}$
- $H = \begin{pmatrix} 2\sum x_i^2 & 2\sum x_i \\ 2\sum x_i & 2n \end{pmatrix}$, que es constante. $\det H = 4\left[n\sum x_i^2 - (\sum x_i)^2\right] > 0$ si no todos los $x_i$ son iguales (desigualdad de Cauchy–Schwarz), y $H_{11} > 0$. Por lo tanto es un **mínimo**, y además global, porque $S$ es un paraboloide convexo con curvas de nivel elípticas.

## Evaluación (resumen)

| Criterio | % |
|----------|---|
| Comprensión conceptual | 20 |
| Evaluación individual (preguntas en la defensa) | 20 |
| Gráficos y análisis | 20 |
| Presentación | 15 |
| Conclusiones | 15 |
| Programación y lógica (incluye pseudocódigo o diagrama de flujo) | 10 |

Detalle en [`docs/rubrica_evaluacion.md`](docs/rubrica_evaluacion.md).

## Estructura del repositorio

```
.
├── Guia_Proyecto_Calculo_Multivariable.pdf  ← guía completa: teoría, desarrollo resuelto, plan y preguntas de defensa
├── README.md                  ← este archivo (explicación general)
├── CLAUDE.md                  ← contexto para asistentes de IA
├── docs/
│   ├── enunciado_proyecto.md  ← enunciado completo en Markdown + LaTeX
│   ├── rubrica_evaluacion.md  ← criterios de evaluación
│   ├── pseudocodigo.md        ← pseudocódigo y diagrama de flujo
│   ├── guia/                  ← fuente del PDF (guia.typ, build.py, resultados.json)
│   └── originales/            ← PDFs originales del docente
├── datos/                     ← hubble_1929.csv + FUENTE.md
├── analisis_manual/           ← guion del desarrollo a mano (derivadas, sistema, Hessiano)
├── codigo/                    ← regresion.py (método propio), verificacion.py, graficos.py
├── graficos/                  ← figuras generadas
└── presentacion/              ← diapositivas / material de la defensa (pendiente)
```

## Cómo ejecutar

```bash
python3 -m venv .venv && .venv/bin/pip install -r codigo/requirements.txt   # solo la primera vez
.venv/bin/python codigo/regresion.py      # método propio: a*, b*, S mínimo, Hessiano, RMSE, R²
.venv/bin/python codigo/verificacion.py   # comparación con numpy/scipy e influencia de cada dato
.venv/bin/python codigo/graficos.py       # regenera las figuras
.venv/bin/python docs/guia/build.py       # regenera todo y recompila el PDF
```
