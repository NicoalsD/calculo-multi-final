# Proyecto de Cálculo Multivariable — Regresión lineal y optimización mediante funciones de varias variables

> Transcripción fiel del enunciado oficial (`docs/originales/enunciado_proyecto_2026B.pdf`, UCC 2026B).
> Las ecuaciones están en LaTeX. Los números entre paréntesis `(n)` corresponden a la numeración de ecuaciones del PDF.

## 1. Planteamiento del problema

En diferentes áreas de la ciencia y la ingeniería es necesario encontrar relaciones matemáticas (modelos matemáticos) que permitan describir un conjunto de datos experimentales o simulados. Una de las aproximaciones más sencillas consiste en buscar una relación lineal de la forma

$$y = ax + b \tag{1}$$

donde $a$ representa la pendiente y $b$ el intercepto. Sin embargo, determinar los valores de $a$ y $b$ que producen el mejor ajuste puede formularse como un problema de optimización de una función de dos variables.

Dado un conjunto de datos

$$(x_1, y_1), (x_2, y_2), \dots, (x_n, y_n) \tag{2}$$

se propone utilizar el modelo $y = ax + b$ (3) y definir la función de error cuadrático

$$S(a,b) = \sum_{i=1}^{n} (y_i - a x_i - b)^2 \tag{4}$$

El objetivo será determinar los valores $a^*$ y $b^*$ que minimizan $S(a,b)$, utilizando inicialmente herramientas de Cálculo Multivariable y, posteriormente, herramientas computacionales para verificar y analizar los resultados.

## 2. Pregunta central del proyecto

El trabajo deberá responder, a partir del análisis matemático y computacional, la siguiente pregunta:

> **¿Cómo se puede utilizar el Cálculo Multivariable para determinar y analizar el modelo lineal que mejor representa un conjunto de datos?**

La respuesta deberá integrar tres perspectivas:

$$\text{análisis analítico} + \text{interpretación geométrica} + \text{análisis computacional} \tag{5}$$

El computador **no** deberá sustituir el desarrollo matemático. Su función será verificar los resultados obtenidos analíticamente, visualizar las funciones de varias variables y permitir un análisis más profundo de los datos.

## 3. Objetivo general

Aplicar conceptos de Cálculo Multivariable para formular, resolver y analizar un problema de regresión lineal mediante la construcción y minimización de una función de error de dos variables, comparando los resultados obtenidos analíticamente de forma manual con los resultados obtenidos mediante herramientas computacionales.

## 4. Objetivos específicos

1. Analizar un conjunto de datos asociado a un problema real de su elección e identificar una posible relación lineal entre las variables involucradas. *(Aclaración: aquí hay que buscar un problema real y recolectar los datos cuyo comportamiento se ajuste a un modelo lineal.)*
2. Formular la función de error cuadrático $S(a,b) = \sum_{i=1}^{n} (y_i - a x_i - b)^2$ (6).
3. Calcular manualmente las derivadas parciales de $S(a,b)$.
4. Utilizar el gradiente para determinar las condiciones necesarias para encontrar el punto crítico.
5. Resolver manualmente el sistema de ecuaciones obtenido para determinar $a^*$ y $b^*$.
6. Calcular y analizar el Hessiano de $S(a,b)$.
7. Determinar mediante el Hessiano si el punto crítico corresponde a un mínimo.
8. Implementar computacionalmente el procedimiento de ajuste.
9. Comparar los resultados analíticos y computacionales.
10. Construir representaciones gráficas que permitan interpretar geométricamente el proceso de minimización.
11. Analizar la calidad del ajuste y las limitaciones del modelo lineal.

## 5. Exploración de los datos

Buscar un problema real y recolectar los datos cuyo comportamiento se ajuste a un modelo lineal. Inicialmente deberán analizar gráficamente la relación entre las variables mediante un diagrama de dispersión, con el propósito de determinar si existe una tendencia aproximadamente lineal.

**Actividades.** Los estudiantes deberán:

- organizar los datos en una tabla;
- identificar las variables $x$ y $y$;
- determinar las unidades de las variables, cuando corresponda;
- construir un gráfico de dispersión de los datos;
- analizar visualmente si existe una posible tendencia aproximadamente lineal.

El gráfico de dispersión deberá permitir discutir si un modelo de la forma $y = ax + b$ (7) es razonable para representar los datos.

## 6. Construcción del modelo

Se propone inicialmente el modelo lineal $y = ax + b$ (8).

Los datos medidos u observados se representan mediante pares $(x_i, y_i)$, donde $x_i$ es el valor medido de la variable independiente y $y_i$ es el valor observado de la variable dependiente. Para cada $x_i$, el modelo proporciona un valor predicho

$$y_{\text{pred},i} = a x_i + b \tag{9}$$

La diferencia entre el valor observado y el valor predicho se denomina **error** o **residuo** y se define como

$$e_i = y_i - y_{\text{pred},i} = y_i - (a x_i + b) \tag{10}$$

Como algunos errores pueden ser positivos y otros negativos, se utilizará el error cuadrático total

$$S(a,b) = \sum_{i=1}^{n} (e_i)^2 = \sum_{i=1}^{n} (y_i - a x_i - b)^2 \tag{11}$$

## 7. Procedimiento analítico

Esta etapa deberá realizarse **manualmente** antes de utilizar herramientas computacionales (solo para realizar alguna gráfica puede usar computadora).

### 7.1. Derivadas parciales

A partir de la función de error $S(a,b) = \sum_{i=1}^{n} (y_i - a x_i - b)^2$ (12), los estudiantes deberán calcular las derivadas parciales respecto de $a$ y $b$, mostrando el procedimiento empleado.

### 7.2. Condición de punto crítico

Utilizando las derivadas parciales obtenidas, los estudiantes deberán establecer la condición de punto crítico

$$\nabla S(a,b) = \mathbf{0} \tag{13}$$

y obtener el sistema de ecuaciones correspondiente.

### 7.3. Determinación de los parámetros

Los estudiantes deberán resolver algebraicamente el sistema obtenido y determinar los valores de $a^*$ y $b^*$ que minimizan la función de error. El procedimiento deberá realizarse manualmente y presentarse de manera clara en su defensa del trabajo.

### 7.4. Análisis mediante el Hessiano

- Una vez determinado el punto crítico, los estudiantes deberán calcular el Hessiano de la función de error.
- Deberán utilizar el criterio del Hessiano para analizar la naturaleza del punto crítico y justificar matemáticamente si corresponde a un mínimo.
- En la defensa, deberá presentar el procedimiento y los argumentos utilizados para sustentar la conclusión.

### 7.5. Interpretación geométrica

$S(a,b)$ puede representarse como una superficie de tres dimensiones, $z = S(a,b)$. Los estudiantes deberán construir computacionalmente esta superficie y analizar su comportamiento en función de los parámetros $a$ y $b$.

### 7.6. Superficie de error

Deberán representar gráficamente la superficie de error para un intervalo adecuado de valores de $a$ y $b$, e identificar la región en la que se encuentra el mínimo.

### 7.7. Trazas y secciones transversales

- Deberán obtener y analizar algunas trazas de la superficie.
- Deberán seleccionar algunas secciones transversales y representarlas gráficamente, explicando qué información proporcionan sobre el comportamiento de la función de error.

### 7.8. Curvas de nivel

- Deberán construir las curvas de nivel de la función $S(a,b)$, y analizar cómo se distribuyen alrededor del punto mínimo.
- Deberán representar gráficamente algunas curvas de nivel, señalar sobre ellas el punto $(a^*, b^*)$ obtenido y analizar su correspondencia con la región de mínimo error.

A partir de la superficie, las trazas, las secciones transversales y las curvas de nivel, deberán explicar geométricamente cómo se comporta la función de error y cómo puede identificarse el punto correspondiente a los parámetros que producen el mejor ajuste.

## 8. Verificación computacional

Después de completar el procedimiento analítico, implementar el problema mediante una herramienta computacional. El programa deberá:

1. cargar los datos;
2. calcular $a^*$ y $b^*$;
3. calcular $S(a^*, b^*)$;
4. construir un gráfico superpuesto que muestre los datos observados y la recta correspondiente al modelo ajustado. Representar también rectas obtenidas con otros valores $(a, b)$, y comparar su ajuste con el modelo que minimiza la función de error;
5. construir la superficie $S(a,b)$; y representar las curvas de nivel, trazas y secciones transversales y el mínimo $(a^*, b^*)$;
6. calcular el Hessiano;
7. verificar numéricamente las propiedades del Hessiano.

> **Aclaración:** en este trabajo, no deberán limitarse a utilizar una función incorporada de regresión lineal. Primero deberán implementar el procedimiento que dedujeron analíticamente. Posteriormente podrán utilizar una función de regresión incorporada como método adicional de verificación y comparación (es decir, deben programar el método de ajuste, después comparan con alguno que haya en las librerías del lenguaje usado).

## 9. Comparación entre el procedimiento analítico y computacional

Los resultados obtenidos mediante el procedimiento analítico realizado manualmente deberán compararse con los resultados obtenidos mediante la implementación computacional desarrollada por los estudiantes y con los resultados proporcionados por las funciones disponibles en las bibliotecas del lenguaje utilizado. Deberán comparar los valores de $a^*$, $b^*$ y $S_{\min}$ obtenidos por cada método, y analizar las posibles diferencias.

Se deberá construir una tabla similar a:

| Parámetro  | Analítico          | Código propio      | Biblioteca de Python | Diferencia máxima |
|------------|--------------------|--------------------|----------------------|-------------------|
| $a$        | $a_{\text{man}}$   | $a_{\text{cod}}$   | $a_{\text{lib}}$     | $\Delta a$        |
| $b$        | $b_{\text{man}}$   | $b_{\text{cod}}$   | $b_{\text{lib}}$     | $\Delta b$        |
| $S_{\min}$ | $S_{\text{man}}$   | $S_{\text{cod}}$   | $S_{\text{lib}}$     | $\Delta S$        |

## 10. Análisis de la recta de ajuste

Una vez obtenidos los parámetros óptimos se construirá la recta

$$y = a^* x + b^* \tag{14}$$

La recta deberá superponerse al conjunto de datos y los estudiantes deberán analizar:

- qué tan bien representa la recta la tendencia general de los datos;
- cuáles puntos presentan mayor desviación respecto a la recta;
- si existen puntos alejados de la tendencia general que puedan influir en el ajuste.

## 11. Análisis de los residuos

Para cada dato deberán calcularse los residuos

$$e_i = y_i - (a^* x_i + b^*) \tag{15}$$

Deberán construirse:

- un gráfico de los residuos $e_i$ en función de $x_i$;
- un histograma de los residuos.

A partir de estas representaciones, analizar:

- si los residuos están aproximadamente centrados alrededor de cero;
- si presentan alguna tendencia o patrón;
- si aumenta o disminuye su dispersión con $x_i$;
- si existen valores atípicos;
- si existe alguna región donde el modelo lineal presenta desviaciones sistemáticas.

> **Aclaración:** se considerará que existe una desviación sistemática cuando los residuos presenten algún patrón o tendencia en función de $x_i$, en lugar de distribuirse aproximadamente alrededor de cero sin una estructura evidente. Por ejemplo, puede ocurrir que los residuos sean predominantemente negativos en una región de los datos y positivos en otra, o que presenten un patrón curvo. Este tipo de comportamiento puede indicar que el modelo lineal no representa adecuadamente alguna región del conjunto de datos.

El análisis deberá ser interpretativo y permitir determinar si el comportamiento de los residuos es compatible con un modelo lineal adecuado para los datos.

## 12. Evaluación de la calidad del modelo

Calcular al menos una medida cuantitativa de la calidad del ajuste. Por ejemplo, la raíz del error cuadrático medio:

$$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} e_i^2} \tag{16}$$

También podrán calcular el coeficiente de determinación:

$$R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2} \tag{17}$$

Explicar qué representa cada medida para el conjunto de datos estudiado.

No será suficiente afirmar que un determinado valor de $R^2$ es "bueno" o "malo". Deberán relacionarlo con la distribución observada de los datos y con el propósito del modelo.

## 13. Análisis adicional

Cada grupo deberá realizar **al menos uno** de los siguientes análisis.

### 13.1. Opción A: Sensibilidad de los parámetros

Modificar ligeramente algunos de los datos y estudiar cómo cambian $a^*$ y $b^*$ (18). Discutir qué tan sensible es el modelo a pequeñas modificaciones de los datos.

### 13.2. Opción B: Influencia de un dato

Eliminar temporalmente uno de los puntos y volver a calcular la regresión. Deberán analizar cómo cambia la recta de ajuste y determinar si existen observaciones con una influencia particularmente importante.

### 13.3. Opción C: Comparación con otro modelo

Comparar el modelo lineal $y = ax + b$ (19) con otro modelo sencillo apropiado para los datos, por ejemplo,

$$y = ax^2 + bx + c \tag{20}$$

Deberán comparar los errores y discutir si el modelo más complejo realmente proporciona una representación significativamente diferente de los datos.

### 13.4. Opción D: Efecto del número de datos

Realizar el ajuste utilizando diferentes cantidades de datos y analizar cómo cambian los parámetros obtenidos.
