// Guía del proyecto final de Cálculo Multivariable.
// Los números salen de resultados.json (generado por codigo/verificacion.py).

#let r = json("resultados.json")

#let f(v, d: 2) = {
  let s = str(calc.round(v, digits: d))
  if d > 0 {
    if not s.contains(".") { s += "." }
    s += "0" * (d - s.split(".").at(1).len())
  }
  s
}
#let sci(v) = {
  let e = calc.floor(calc.log(calc.abs(v)))
  $#f(v / calc.pow(10.0, e), d: 1) times 10^(#e)$
}
#let azul = rgb("#1f4e79")
#let nota(titulo, cuerpo, color: azul) = block(
  width: 100%, inset: 10pt, radius: 3pt, breakable: false,
  fill: color.lighten(90%), stroke: (left: 3pt + color),
)[#text(fill: color, weight: "bold")[#titulo] \ #cuerpo]
#let fig(ruta, pie, ancho: 78%) = figure(image(ruta, width: ancho), caption: pie)
#let m2(a, b, c, d) = math.mat((a, b), (c, d))
#let cb = box(width: 7pt, height: 7pt, stroke: 0.6pt, baseline: 1pt)
#let D = r.n * r.sxx - r.sx * r.sx
#let inf = r.influencia
#let p1068 = inf.find(p => p.objeto == "NGC 1068")

#set document(title: "Guía del proyecto final de Cálculo Multivariable", author: "Grupo de trabajo")
#set page(paper: "us-letter", margin: (x: 2.3cm, y: 2.4cm), numbering: "1",
  header: context if counter(page).get().first() > 1 [
    #set text(8pt, fill: gray)
    Guía del proyecto final · Cálculo Multivariable · UCC 2026B #h(1fr) Ley de Hubble por mínimos cuadrados
  ])
#set text(lang: "es", size: 10.5pt)
#set par(justify: true, leading: 0.62em)
#set heading(numbering: "1.1")
#show heading.where(level: 1): it => block(above: 1.6em, below: 0.9em, text(fill: azul, size: 15pt, it))
#show heading.where(level: 2): it => block(above: 1.3em, below: 0.7em, text(fill: azul, size: 12pt, it))
#set math.equation(numbering: none)
#show figure.caption: set text(9pt)
#show raw.where(block: true): it => block(width: 100%, fill: luma(245), inset: 8pt, radius: 3pt, text(8pt, it))
#set table(stroke: 0.4pt + gray, inset: 5pt)
#show table.cell.where(y: 0): set text(weight: "bold")

// ---------- Portada ----------
#v(1.2cm)
#align(center)[
  #text(11pt, fill: gray)[Universidad Cooperativa de Colombia · Ingeniería de Software · San Juan de Pasto]
  #v(1.2cm)
  #text(24pt, weight: "bold", fill: azul)[Guía del proyecto final \ de Cálculo Multivariable]
  #v(0.5cm)
  #text(14pt)[Regresión lineal y optimización con funciones de varias variables]
  #v(0.9cm)
  #line(length: 40%, stroke: 0.6pt + azul)
  #v(0.9cm)
  #text(15pt, weight: "bold")[Problema real elegido: la ley de Hubble]
  #v(0.2cm)
  #text(11pt)[¿A qué velocidad se alejan las galaxias según su distancia? \ Datos originales de Edwin Hubble (1929), 24 galaxias]
  #v(0.8cm)
  #image("/graficos/02_recta_ajuste.png", width: 60%)
  #v(1fr)
  #text(10pt, fill: gray)[Docente: M.Sc. Alejandro Molina · Periodo 2026B \ Documento de estudio y trabajo del grupo: teoría, desarrollo resuelto, código, plan y preguntas de defensa]
]
#pagebreak()

#nota("Cómo usar esta guía")[
  Este documento trae el proyecto *resuelto de principio a fin* con datos reales, para que lo entiendan y lo puedan defender. No es para entregarlo tal cual: el enunciado exige que el procedimiento analítico lo hagan *a mano*, y el 40 % de la nota es comprensión y respuestas individuales. Lo recomendable es que cada integrante repita el desarrollo de la @analitico en papel y practique las preguntas de la @defensa.
  Los números usan punto decimal, igual que el código en Python.
]
#v(0.5em)
#{
  set text(9pt)
  set par(leading: 0.5em)
  outline(title: "Contenido", depth: 2)
}
#pagebreak()

// ---------- 1 ----------
= Qué pide el proyecto y cómo se califica

== La idea en un párrafo
Hay que tomar un conjunto de datos reales que sigan una tendencia aproximadamente lineal y hallar la recta $y = a x + b$ que mejor los representa. "La mejor" es la que hace mínimo el error cuadrático total
$ S(a, b) = sum_(i=1)^n (y_i - a x_i - b)^2 . $
Lo esencial es que los datos $(x_i, y_i)$ son números fijos y las incógnitas son $a$ y $b$. Por eso $S$ es una *función de dos variables*, y buscar la mejor recta es buscar el punto más bajo de una superficie. Eso se hace con las herramientas del curso: derivadas parciales, gradiente, Hessiano, trazas y curvas de nivel.

La pregunta central que el trabajo debe responder es: _¿cómo se puede utilizar el Cálculo Multivariable para determinar y analizar el modelo lineal que mejor representa un conjunto de datos?_ La respuesta debe unir tres miradas: analítica (a mano), geométrica (superficie y curvas de nivel) y computacional (código que verifica).

== Lo que hay que entregar
#table(columns: (auto, 1fr, auto),
  [Sección], [Qué se pide], [Dónde está aquí],
  [§5], [Problema real, tabla de datos con unidades, diagrama de dispersión y discusión de si es lineal], [@problema],
  [§6], [Modelo, residuos y función de error $S(a,b)$], [@modelo],
  [§7.1–7.4], [*A mano:* derivadas parciales, $nabla S = 0$, resolver el sistema, Hessiano y clasificación del punto crítico], [@analitico],
  [§7.5–7.8], [Superficie de error, trazas, secciones transversales y curvas de nivel con el mínimo marcado], [@geometria],
  [§8], [Programa propio (no solo una función de librería) con datos, parámetros, gráficos y Hessiano], [@codigo],
  [§9], [Tabla comparativa: a mano, código propio y librería], [@comparacion],
  [§10–12], [Análisis de la recta, de los residuos (gráfico e histograma) y medida de calidad (RMSE, $R^2$)], [@analisis],
  [§13], [Al menos un análisis adicional. Elegimos la opción B: influencia de un dato], [@influencia],
)

== Rúbrica
#table(columns: (auto, 1fr, auto),
  [Criterio], [Aspectos evaluados], [Peso],
  [Comprensión conceptual], [Entendimiento del problema, interpretación física y matemática, respuestas a preguntas], [20 %],
  [Evaluación individual], [Respuestas a preguntas, comprensión individual], [20 %],
  [Gráficos y análisis], [Calidad de gráficos, interpretación, uso en las conclusiones], [20 %],
  [Presentación], [Claridad, diseño, comunicación oral], [15 %],
  [Conclusiones], [Calidad de las conclusiones, reflexión crítica], [15 %],
  [Programación y lógica], [Lógica del algoritmo, pseudocódigo o diagrama de flujo, relación código–modelo], [10 %],
)
#nota("Qué significa esto en la práctica")[
  - El 40 % se gana *hablando*: cualquier integrante debe poder explicar por qué se deriva, qué es el gradiente, de dónde sale el sistema y qué dice el Hessiano.
  - El código vale solo el 10 %, y lo que se mira es la lógica y su relación con las fórmulas, además del pseudocódigo o diagrama de flujo.
  - Los gráficos deben *usarse* para argumentar en las conclusiones, no solo mostrarse.
]

// ---------- 2 ----------
= El problema real: la ley de Hubble <problema>

== Contexto
En 1929 el astrónomo Edwin Hubble reunió dos mediciones de 24 galaxias cercanas: su *distancia* a la Tierra y su *velocidad radial* (la velocidad con que se alejan o se acercan, medida por el corrimiento de su luz hacia el rojo o el azul). Al graficarlas notó que, en general, cuanto más lejos está una galaxia, más rápido se aleja. Esa relación, hoy llamada ley de Hubble,
$ v = H_0 d , $
fue la primera evidencia observacional de que el universo se expande. Es el mismo tipo de ley que la de Hooke ($F = k x$): una relación lineal entre dos magnitudes medidas, cuya pendiente es una constante física.

#table(columns: (auto, 1fr, auto),
  [Variable], [Significado], [Unidad],
  [$x$ (independiente)], [Distancia de la galaxia], [megapársec (Mpc); 1 Mpc ≈ 3.26 millones de años luz],
  [$y$ (dependiente)], [Velocidad radial. Positiva si se aleja, negativa si se acerca], [km/s],
  [$a$ (pendiente)], [Constante de Hubble $H_0$: cuánto aumenta la velocidad por cada Mpc], [km/s por Mpc],
  [$b$ (intercepto)], [Velocidad que el modelo predice a distancia cero. La ley física dice que debería ser 0], [km/s],
)

*Fuente de los datos:* Hubble, E. (1929). _A relation between distance and radial velocity among extra-galactic nebulae_. Proceedings of the National Academy of Sciences, 15(3), 168–173, Tabla 1. Están en `datos/hubble_1929.csv`.

#nota("Por qué es un buen problema para este proyecto")[
  - Son datos reales e históricos, ya publicados: no hay que hacer experimento ni maqueta.
  - La pendiente y el intercepto tienen significado físico claro.
  - Los datos tienen bastante dispersión y algunos puntos alejados, así que el análisis de residuos, de calidad y de influencia de un dato tiene de qué hablar.
  - Permite una reflexión crítica de fondo: la recta de Hubble era correcta como tendencia, pero su pendiente resultó unas 6.5 veces mayor que el valor aceptado hoy (≈ 70 km/s/Mpc) porque las distancias de 1929 estaban mal calibradas. Un buen ajuste matemático no corrige datos sesgados.
]

== Tabla de datos
La tabla incluye las columnas $x^2$ y $x y$ porque sus sumas son lo único que se necesita para resolver el problema a mano.

#{
  set text(8.5pt)
  table(columns: (auto, 1fr, auto, auto, auto, auto), align: (center, left, right, right, right, right),
    inset: 3.4pt,
    [$i$], [Galaxia], [$x_i$ (Mpc)], [$y_i$ (km/s)], [$x_i^2$], [$x_i y_i$],
    ..r.datos.enumerate().map(((i, p)) => ([#(i + 1)], p.objeto, f(p.x, d: 3), f(p.y, d: 0), f(p.x2, d: 6), f(p.xy, d: 3))).flatten(),
    table.cell(colspan: 2, align: right)[*Sumas ($n = #r.n$)*], [*#f(r.sx, d: 3)*], [*#f(r.sy, d: 0)*], [*#f(r.sxx, d: 6)*], [*#f(r.sxy, d: 3)*],
  )
}

== Diagrama de dispersión
#fig("/graficos/01_dispersion.png", [Diagrama de dispersión de las 24 galaxias.], ancho: 66%)

*Lectura del gráfico.* La nube de puntos sube de izquierda a derecha: las galaxias a 2 Mpc se alejan a velocidades entre 500 y 1090 km/s, mientras que las que están a menos de 0.5 Mpc tienen velocidades entre −220 y 290 km/s. No se aprecia una curvatura clara, así que un modelo $y = a x + b$ es razonable como primera aproximación. También se ve que la dispersión es grande (para una misma distancia de 0.9 Mpc hay velocidades desde −30 hasta 650 km/s) y que cuatro galaxias cercanas tienen velocidad negativa, es decir, se acercan a nosotros. El modelo lineal describirá la tendencia general, no cada galaxia.

// ---------- 3 ----------
= Construcción del modelo <modelo>
Para cada galaxia el modelo predice $y_("pred",i) = a x_i + b$. La diferencia con lo observado es el *residuo*
$ e_i = y_i - (a x_i + b) . $
Unos residuos son positivos (el punto queda por encima de la recta) y otros negativos (por debajo). Si se sumaran directamente se cancelarían, y una recta pésima podría dar suma cero. Por eso se elevan al cuadrado antes de sumar:
$ S(a, b) = sum_(i=1)^n e_i^2 = sum_(i=1)^n (y_i - a x_i - b)^2 . $
Elevar al cuadrado además penaliza más los errores grandes y produce una función suave que se puede derivar (el valor absoluto no es derivable en cero).

#nota("El cambio de papel que hay que tener claro")[
  En la recta $y = a x + b$ la variable es $x$. En $S(a, b)$ es al revés: los $x_i$ y $y_i$ son los #r.n datos, números fijos, y las variables son $a$ y $b$. Cada punto $(a, b)$ del plano es *una recta distinta*, y $S(a,b)$ es la nota (el error) que saca esa recta. Buscamos la recta con el menor error.
]

Si se desarrolla el cuadrado y se agrupan términos, se ve que $S$ es un polinomio de segundo grado en $a$ y $b$:
$ S(a,b) = (sum x_i^2) a^2 + 2 (sum x_i) a b + n b^2 - 2 (sum x_i y_i) a - 2 (sum y_i) b + sum y_i^2 . $
Su gráfica es un paraboloide. Con nuestros datos:
$ S(a,b) = #f(r.sxx, d: 4) a^2 + #f(2 * r.sx, d: 3) a b + #r.n b^2 - #f(2 * r.sxy, d: 2) a - #f(2 * r.sy, d: 0) b + "constante" . $

// ---------- 4 ----------
= Teoría mínima necesaria <teoria>

== Derivadas parciales
La derivada parcial $(partial S)/(partial a)$ mide cuánto cambia $S$ cuando se mueve solo $a$ y se deja $b$ quieto; se calcula derivando respecto de $a$ y tratando $b$ como constante. Lo mismo para $(partial S)/(partial b)$. Geométricamente son las pendientes de la superficie en las direcciones de los ejes $a$ y $b$.

== Gradiente y punto crítico
El gradiente reúne las dos parciales en un vector, $nabla S = ((partial S)/(partial a), (partial S)/(partial b))$, y apunta hacia donde $S$ crece más rápido. En el fondo de un valle la superficie es horizontal en todas las direcciones, así que ahí las dos parciales valen cero:
$ nabla S (a, b) = (0, 0) . $
Los puntos que cumplen esto se llaman *puntos críticos*. Es una condición necesaria para un mínimo, pero no suficiente: también la cumplen los máximos y los puntos de silla. Por eso hace falta el Hessiano.

== Hessiano y criterio de la segunda derivada
El Hessiano es la matriz de las segundas derivadas parciales:
$ H = mat(S_(a a), S_(a b); S_(b a), S_(b b)) . $
Mide la curvatura de la superficie. Sea $D = det H = S_(a a) S_(b b) - S_(a b)^2$ evaluado en el punto crítico:
#table(columns: (auto, 1fr),
  [Condición], [Conclusión],
  [$D > 0$ y $S_(a a) > 0$], [Mínimo local: la superficie se curva hacia arriba en todas las direcciones],
  [$D > 0$ y $S_(a a) < 0$], [Máximo local],
  [$D < 0$], [Punto de silla: sube en una dirección y baja en otra],
  [$D = 0$], [El criterio no decide],
)
Una forma equivalente: si los dos valores propios de $H$ son positivos, la matriz es _definida positiva_ y el punto es un mínimo.

== Trazas, secciones y curvas de nivel
- Una *sección transversal* es el corte de la superficie con un plano vertical: se fija una variable (por ejemplo $b = b_0$) y queda una curva de una sola variable, $S(a, b_0)$. Cuando el plano es uno de los planos coordenados ($a = 0$ o $b = 0$) el corte se llama *traza*.
- Una *curva de nivel* es el conjunto de puntos $(a, b)$ donde $S$ vale lo mismo, $S(a,b) = k$. Es el corte con un plano horizontal visto desde arriba, como las curvas de un mapa topográfico.

// ---------- 5 ----------
= Procedimiento analítico (a mano) <analitico>
#nota("Importante", color: rgb("#c0392b"))[
  Esta sección es la que deben reproducir en papel, con su propia letra, y saber explicar paso a paso. El enunciado exige que se haga manualmente antes de usar el computador.
]

== Derivadas parciales
Se aplica la regla de la cadena a cada término $(y_i - a x_i - b)^2$: se baja el 2, se deja el paréntesis y se multiplica por la derivada de lo de adentro.

Respecto de $a$, la derivada de $(y_i - a x_i - b)$ es $-x_i$:
$ (partial S)/(partial a) = sum_(i=1)^n 2 (y_i - a x_i - b)(-x_i) = -2 sum_(i=1)^n x_i (y_i - a x_i - b) . $
Respecto de $b$, la derivada de $(y_i - a x_i - b)$ es $-1$:
$ (partial S)/(partial b) = sum_(i=1)^n 2 (y_i - a x_i - b)(-1) = -2 sum_(i=1)^n (y_i - a x_i - b) . $

== Condición de punto crítico
Se iguala el gradiente a cero. Dividiendo por $-2$ y repartiendo la suma:
$ sum x_i y_i - a sum x_i^2 - b sum x_i = 0 , quad quad sum y_i - a sum x_i - n b = 0 . $
Reordenando queda un sistema lineal de dos ecuaciones con dos incógnitas, las *ecuaciones normales*:
$ a sum x_i^2 + b sum x_i &= sum x_i y_i \
  a sum x_i + n b &= sum y_i $
Con las sumas de la tabla de datos:
$ #f(r.sxx, d: 6) a + #f(r.sx, d: 3) b &= #f(r.sxy, d: 3) \
  #f(r.sx, d: 3) a + #r.n b &= #f(r.sy, d: 0) $

== Solución del sistema
De la segunda ecuación se despeja $b$:
$ b = (sum y_i - a sum x_i)/n = overline(y) - a overline(x) . $
Sustituyendo en la primera y despejando $a$ (o usando la regla de Cramer) se obtiene
$ a^* = (n sum x_i y_i - sum x_i sum y_i)/(n sum x_i^2 - (sum x_i)^2) , quad quad b^* = overline(y) - a^* overline(x) . $
Sustitución numérica:
$ a^* = (#r.n (#f(r.sxy, d: 3)) - (#f(r.sx, d: 3))(#f(r.sy, d: 0)))/(#r.n (#f(r.sxx, d: 6)) - (#f(r.sx, d: 3))^2)
      = (#f(r.n * r.sxy, d: 2) - #f(r.sx * r.sy, d: 3))/(#f(r.n * r.sxx, d: 5) - #f(r.sx * r.sx, d: 6))
      = (#f(r.n * r.sxy - r.sx * r.sy, d: 3))/(#f(D, d: 6)) = #f(r.a, d: 2) . $
Las medias son $overline(x) = #f(r.sx, d: 3) \/ #r.n = #f(r.xm, d: 6)$ y $overline(y) = #f(r.sy, d: 0) \/ #r.n = #f(r.ym, d: 3)$, de modo que
$ b^* = #f(r.ym, d: 3) - (#f(r.a, d: 2))(#f(r.xm, d: 6)) = #f(r.b, d: 2) . $

#nota("Resultado")[
  $ a^* approx #f(r.a, d: 2) "km/s por Mpc" , quad b^* approx #f(r.b, d: 2) "km/s" , quad quad "recta: " y = #f(r.a, d: 2) x - #f(calc.abs(r.b), d: 2) . $
  El error mínimo es $S(a^*, b^*) approx #f(r.S, d: 0)$ (km/s)².
]

*Interpretación.* Por cada megapársec adicional de distancia, la velocidad de alejamiento aumenta en promedio unos #f(r.a, d: 0) km/s. Hubble reportó 465 y 513 km/s/Mpc con un ajuste que además corregía el movimiento del Sol, así que nuestro valor es coherente con el suyo. El intercepto de #f(r.b, d: 0) km/s es pequeño frente a las velocidades de los datos (hasta 1090 km/s), compatible con la idea física de que a distancia cero la velocidad es cero.

De la segunda ecuación normal sale un hecho útil: $overline(y) = a^* overline(x) + b^*$, es decir, la recta óptima siempre pasa por el punto de las medias $(overline(x), overline(y)) = (#f(r.xm, d: 3), #f(r.ym, d: 1))$.

== Hessiano
Se derivan otra vez las parciales:
$ S_(a a) = (partial)/(partial a) [-2 sum x_i (y_i - a x_i - b)] = 2 sum x_i^2 , quad
  S_(b b) = 2 n , quad
  S_(a b) = S_(b a) = 2 sum x_i . $
$ H = mat(2 sum x_i^2, 2 sum x_i; 2 sum x_i, 2 n) = #m2(f(r.H.at(0).at(0), d: 5), f(r.H.at(0).at(1), d: 3), f(r.H.at(1).at(0), d: 3), f(r.H.at(1).at(1), d: 0)) . $
El Hessiano *no depende de $a$ ni de $b$*: la superficie tiene la misma curvatura en todas partes, lo que es propio de un paraboloide. Tampoco depende de los $y_i$, solo de los $x_i$.

== Clasificación del punto crítico
$ D = det H = (#f(r.H.at(0).at(0), d: 5))(#f(r.H.at(1).at(1), d: 0)) - (#f(r.H.at(0).at(1), d: 3))^2 = #f(r.det, d: 4) > 0 , quad quad S_(a a) = #f(r.H.at(0).at(0), d: 5) > 0 . $
Como $D > 0$ y $S_(a a) > 0$, el punto crítico $(a^*, b^*)$ es un *mínimo*. Los valores propios de $H$ son $lambda_1 = #f(r.l1, d: 3)$ y $lambda_2 = #f(r.l2, d: 3)$, ambos positivos, lo que confirma que $H$ es definida positiva.

*Por qué esto pasa siempre, no solo con estos datos.* En general
$ D = 4 [n sum x_i^2 - (sum x_i)^2] = 4 n sum (x_i - overline(x))^2 . $
Una suma de cuadrados nunca es negativa, y solo vale cero si todos los $x_i$ son iguales. Con al menos dos valores distintos de $x$ el determinante es positivo, y $S_(a a) = 2 sum x_i^2 > 0$. Conclusión: la regresión lineal siempre tiene un único punto crítico y siempre es un mínimo.

*Por qué el mínimo es global.* Como $S$ es un polinomio de grado 2, su desarrollo de Taylor alrededor de $(a^*, b^*)$ es exacto, y el término de primer orden se anula porque el gradiente es cero:
$ S(a, b) = S(a^*, b^*) + 1/2 mat(Delta a, Delta b) H vec(Delta a, Delta b) , quad Delta a = a - a^* , space Delta b = b - b^* . $
Al ser $H$ definida positiva, el segundo término es positivo para cualquier desplazamiento. Ninguna otra recta puede tener un error menor.

// ---------- 6 ----------
= Interpretación geométrica <geometria>

== Superficie de error
#fig("/graficos/03_superficie.png", [Superficie $z = S(a, b)$ con el mínimo marcado en rojo y las curvas de nivel proyectadas en el piso.], ancho: 70%)
La superficie es un paraboloide abierto hacia arriba, con forma de valle alargado. Tiene un solo punto más bajo, en $(a^*, b^*) = (#f(r.a, d: 1), #f(r.b, d: 1))$, donde la altura es $S_"mín" approx #f(r.S / 1e6, d: 2) times 10^6$. Hay que notar que el mínimo no es cero: ninguna recta pasa por los 24 puntos a la vez, así que siempre queda un error.

== Trazas y secciones transversales
#fig("/graficos/04_trazas.png", [Cortes verticales de la superficie. Izquierda: $b$ fijo. Derecha: $a$ fijo. Las líneas punteadas negras son las trazas (planos $b = 0$ y $a = 0$).], ancho: 100%)

Si se fija $b = b_0$, queda $S(a, b_0)$, una parábola en $a$ con segunda derivada $S_(a a) = 2 sum x_i^2 = #f(r.H.at(0).at(0), d: 2)$. Si se fija $a = a_0$, queda una parábola en $b$ con segunda derivada $S_(b b) = 2 n = #(2 * r.n)$. Lo que muestran los cortes:
- *Todas las secciones son parábolas que abren hacia arriba*, con la misma abertura dentro de cada panel. Es el Hessiano constante visto en una dimensión.
- *La sección que pasa por el óptimo (línea roja) es la más baja*, y su vértice está exactamente en $a^*$ (izquierda) o en $b^*$ (derecha).
- *Al cambiar el valor fijado, el vértice se desplaza.* Con $b$ mayor, el mejor $a$ es menor, y viceversa. Esto ocurre porque el término cruzado $S_(a b) = 2 sum x_i$ no es cero: los dos parámetros se compensan entre sí. Si se sube el intercepto, la recta debe inclinarse menos para seguir cerca de los puntos.
- *Las trazas tienen significado propio.* La traza $b = 0$ corresponde a obligar a la recta a pasar por el origen, que es la ley de Hubble pura $v = H_0 d$; su mínimo está en $a = sum x_i y_i \/ sum x_i^2 = #f(r.sxy / r.sxx, d: 1)$ km/s/Mpc. La traza $a = 0$ corresponde a una recta horizontal (la velocidad no depende de la distancia); su mínimo está en $b = overline(y) = #f(r.ym, d: 1)$, y su altura mínima es mucho mayor que $S_"mín"$, lo que muestra cuánto se gana al permitir la pendiente.

== Curvas de nivel
#fig("/graficos/05_curvas_nivel.png", [Curvas de nivel de $S(a,b)$ con el punto $(a^*, b^*)$.], ancho: 66%)
- Las curvas de nivel son *elipses concéntricas* y su centro común es $(a^*, b^*)$. Cada elipse reúne todas las rectas que tienen el mismo error.
- Los valores crecen hacia afuera: alejarse del centro en cualquier dirección aumenta el error. Así se identifica el mínimo en un mapa de contornos: es el punto que queda encerrado por todas las curvas.
- Las elipses están *inclinadas hacia abajo a la derecha*. Es la misma compensación entre $a$ y $b$ que se vio en las secciones: a lo largo del eje largo de la elipse se puede aumentar $a$ y disminuir $b$ sin que el error cambie mucho.
- Son *alargadas* porque la curvatura es distinta según la dirección. La relación entre los ejes es $sqrt(lambda_2 \/ lambda_1) approx #f(calc.sqrt(r.l2 / r.l1), d: 1)$: el valle es unas tres veces más ancho en una dirección que en la otra. En la dirección ancha los datos determinan peor la combinación de parámetros.
- El gradiente es perpendicular a las curvas de nivel y apunta hacia afuera; en el centro se anula. Es la condición $nabla S = 0$ vista en el mapa.

// ---------- 7 ----------
= Verificación computacional <codigo>

== Estructura del programa
#table(columns: (auto, 1fr),
  [Archivo], [Qué hace],
  [`codigo/regresion.py`], [Método propio. Cada función es un paso del desarrollo a mano: sumas, solución de las ecuaciones normales, $S$, gradiente, Hessiano, residuos, RMSE y $R^2$. No usa funciones de regresión de librería],
  [`codigo/verificacion.py`], [Compara con `numpy.polyfit` y `scipy.stats.linregress`, comprueba el Hessiano numéricamente y hace el análisis de influencia],
  [`codigo/graficos.py`], [Genera todas las figuras en `graficos/`],
)
Para ejecutarlo: `.venv/bin/python codigo/regresion.py`, y lo mismo con los otros dos archivos.

== Relación entre el código y el modelo
#table(columns: (1fr, 1fr),
  [Matemática], [Código],
  [$sum x_i, sum y_i, sum x_i^2, sum x_i y_i$], [`sumas(x, y)`: un ciclo que acumula las cuatro sumas],
  [Solución de $nabla S = 0$], [`ajustar(x, y)`: aplica las fórmulas de $a^*$ y $b^*$],
  [$S(a,b) = sum (y_i - a x_i - b)^2$], [`error_cuadratico(a, b, x, y)`],
  [$nabla S$], [`gradiente(a, b, x, y)`: debe dar (0, 0) en el óptimo],
  [$H$, $det H$ y valores propios], [`hessiano(x)` y `analizar_hessiano(H)`],
  [$e_i$, RMSE, $R^2$], [`residuos`, `rmse`, `r_cuadrado`],
)

== Pseudocódigo
```
INICIO
  leer el archivo de datos → listas x, y
  n ← cantidad de datos
  Sx ← 0; Sy ← 0; Sxx ← 0; Sxy ← 0
  PARA cada par (xi, yi):
      Sx ← Sx + xi;        Sy ← Sy + yi
      Sxx ← Sxx + xi·xi;   Sxy ← Sxy + xi·yi
  det ← n·Sxx − Sx·Sx
  SI det = 0: informar "todos los x son iguales" y terminar
  a ← (n·Sxy − Sx·Sy) / det
  b ← (Sxx·Sy − Sx·Sxy) / det
  Smin ← suma de (yi − a·xi − b)² para todos los datos
  H ← [[2·Sxx, 2·Sx], [2·Sx, 2·n]]
  D ← H11·H22 − H12²
  SI D > 0 y H11 > 0: informar "el punto crítico es un mínimo"
  calcular residuos, RMSE y R²
  comparar a, b, Smin con la función de la librería
  generar los gráficos
FIN
```

== Diagrama de flujo
#{
  let caja(t, c: azul.lighten(88%)) = rect(width: 9cm, inset: 6pt, radius: 4pt, fill: c, stroke: 0.6pt + azul, align(center, text(9pt, t)))
  let fl = align(center, text(11pt, fill: azul, sym.arrow.b))
  align(center, block(breakable: false, stack(spacing: 3pt,
    caja([*Inicio:* cargar los datos $(x_i, y_i)$], c: azul.lighten(70%)), fl,
    caja([Calcular $n$, $sum x$, $sum y$, $sum x^2$, $sum x y$]), fl,
    caja([¿$n sum x^2 - (sum x)^2 != 0$? Si no, terminar con error], c: rgb("#fdf2d0")), fl,
    caja([Resolver las ecuaciones normales: $a^*$, $b^*$]), fl,
    caja([Calcular $S(a^*, b^*)$ y comprobar $nabla S approx 0$]), fl,
    caja([Calcular $H$, $det H$ y valores propios; confirmar mínimo]), fl,
    caja([Residuos, RMSE, $R^2$ e influencia de cada dato]), fl,
    caja([Comparar con `polyfit` y `linregress`]), fl,
    caja([*Fin:* generar gráficos y tabla de resultados], c: azul.lighten(70%)),
  )))
}

== Verificación numérica del Hessiano
El programa comprueba el Hessiano de tres maneras:
+ *Analítico*, con las fórmulas: $H = #m2(f(r.H.at(0).at(0), d: 4), f(r.H.at(0).at(1), d: 3), f(r.H.at(1).at(0), d: 3), f(r.H.at(1).at(1), d: 0))$.
+ *Numérico*, aproximando las segundas derivadas con diferencias finitas sobre $S$ (sin usar las fórmulas): $#m2(f(r.Hn.at(0).at(0), d: 4), f(r.Hn.at(0).at(1), d: 3), f(r.Hn.at(1).at(0), d: 3), f(r.Hn.at(1).at(1), d: 4))$. Coincide con el analítico salvo el error de redondeo del método.
+ *Propiedades:* es simétrico, $det H = #f(r.det, d: 2) > 0$, $H_(11) > 0$ y los valores propios (#f(r.l1, d: 3) y #f(r.l2, d: 3)) son positivos.
Además, el gradiente evaluado en $(a^*, b^*)$ da (#sci(r.grad.at(0)), #sci(r.grad.at(1))), que es cero salvo redondeo de la máquina.

// ---------- 8 ----------
= Comparación entre métodos <comparacion>
#table(columns: (auto, 1fr, 1fr, 1fr, 1fr, auto), align: (left, right, right, right, right, right),
  [Parámetro], [A mano], [Código propio], [`numpy.polyfit`], [`scipy linregress`], [Dif. máxima],
  [$a$], [#f(r.a_man, d: 2)], [#f(r.a, d: 6)], [#f(r.a_np, d: 6)], [#f(r.a_sp, d: 6)], [#sci(r.da)],
  [$b$], [#f(r.b_man, d: 2)], [#f(r.b, d: 6)], [#f(r.b_np, d: 6)], [#f(r.b_sp, d: 6)], [#sci(r.db)],
  [$S_"mín"$], [#f(r.S_man, d: 4)], [#f(r.S, d: 4)], [#f(r.S_np, d: 4)], [#f(r.S_sp, d: 4)], [#sci(r.dS)],
)
*Análisis de las diferencias.*
- El código propio y las dos librerías coinciden hasta unas #sci(r.db_lib) unidades. Esa diferencia es puro redondeo de punto flotante: las librerías resuelven el mismo problema con otro algoritmo (descomposiciones matriciales en lugar de las fórmulas cerradas).
- La columna "a mano" difiere en la tercera cifra decimal porque ahí se redondeó a dos decimales, como se haría con calculadora. No es un error del método sino del redondeo.
- $S_"mín"$ casi no cambia aunque $a$ y $b$ cambien en milésimas. Tiene explicación en el cálculo: en el mínimo el gradiente es cero, así que un cambio pequeño en los parámetros produce un cambio de segundo orden en $S$. El fondo del valle es plano.

#nota("Pendiente para el grupo")[
  La columna "a mano" de esta tabla se generó redondeando a dos decimales. Deben reemplazarla por los valores que obtengan en su propio desarrollo en papel; si redondean distinto, la diferencia máxima cambiará un poco.
]

// ---------- 9 ----------
= Análisis de resultados <analisis>

== Recta de ajuste
#fig("/graficos/02_recta_ajuste.png", [Datos, recta óptima (roja) y tres rectas con otros valores de $(a, b)$, con su error $S$.], ancho: 72%)
- *Tendencia general.* La recta $y = #f(r.a, d: 1) x - #f(calc.abs(r.b), d: 1)$ atraviesa la nube por el centro y recoge bien la tendencia creciente. No describe cada galaxia: hay puntos a varios cientos de km/s de la recta.
- *Comparación con otras rectas.* Las tres rectas punteadas tienen errores entre 1.5 y 2.2 veces mayores que la óptima. Una pendiente mayor o menor, o la misma pendiente desplazada hacia arriba, siempre empeoran $S$. Cada una de estas rectas es un punto del plano $(a, b)$ que queda en una curva de nivel más externa.
- *Puntos con mayor desviación.* #r.mayores_residuos.slice(0, 3).map(p => [#p.objeto ($x = #f(p.x, d: 1)$, residuo #f(p.e, d: 0) km/s)]).join(", ", last: " y ").
- *Puntos que pueden influir.* Las cuatro galaxias a 2 Mpc y las dos Nubes de Magallanes (casi a distancia cero) están en los extremos del eje $x$, así que tienen mucha palanca sobre la pendiente. Se estudia en la @influencia.

== Residuos
#grid(columns: (1fr, 1fr), gutter: 8pt,
  fig("/graficos/06_residuos.png", [Residuos $e_i$ en función de $x_i$.], ancho: 100%),
  fig("/graficos/07_histograma_residuos.png", [Histograma de los residuos.], ancho: 100%),
)
- *¿Centrados en cero?* Sí: la media de los residuos es cero y hay #r.e_pos positivos y #r.e_neg negativos. Ojo: que la suma sea cero no es mérito de los datos, es consecuencia directa de la ecuación $(partial S)/(partial b) = 0$, que dice justamente $sum e_i = 0$. Pasa en toda regresión lineal con intercepto. El histograma tiene su barra más alta junto a cero y es más o menos simétrico.
- *¿Tendencia o patrón?* No hay una curva global (los residuos no forman una U ni una rampa), lo que apoya el modelo lineal. Tampoco hay correlación entre $e_i$ y $x_i$, por la otra ecuación normal: $sum x_i e_i = 0$.
- *¿Cambia la dispersión con $x$?* No de forma clara. La dispersión es grande en todo el rango (entre −400 y +500 km/s) y el mayor abanico está en la zona media, alrededor de 0.9 a 1.0 Mpc, no en un extremo.
- *¿Valores atípicos?* Los residuos más grandes son los de #r.mayores_residuos.at(0).objeto (#f(r.mayores_residuos.at(0).e, d: 0)), #r.mayores_residuos.at(1).objeto (#f(r.mayores_residuos.at(1).e, d: 0)) y #r.mayores_residuos.at(2).objeto (#f(r.mayores_residuos.at(2).e, d: 0)). Están a unas dos veces el RMSE, así que son desviaciones grandes pero no absurdas; no hay motivo para descartarlos.
- *¿Desviación sistemática en alguna región?* Sí, en las galaxias más cercanas. Las cuatro que están entre 0.2 y 0.3 Mpc tienen todas residuo negativo (entre −150 y −300 km/s) y las dos Nubes de Magallanes, a 0.03 Mpc, lo tienen positivo. Tiene explicación física: a distancias tan cortas la expansión es débil y domina el movimiento propio de cada galaxia por la gravedad del vecindario (Andromeda, NGC 224, de hecho se acerca a nosotros). El modelo lineal no representa bien esa región.

*Conclusión del análisis.* El comportamiento de los residuos es compatible con un modelo lineal para la tendencia general, con dos reservas: mucha dispersión alrededor de la recta y una zona cercana donde el modelo falla de forma sistemática.

== Calidad del modelo
$ "RMSE" = sqrt(1/n sum e_i^2) = sqrt((#f(r.S, d: 0))/(#r.n)) approx #f(r.rmse, d: 0) "km/s" , quad quad
  R^2 = 1 - (sum (y_i - hat(y)_i)^2)/(sum (y_i - overline(y))^2) approx #f(r.r2, d: 3) . $
- *RMSE.* Es el tamaño típico del error de la recta, en las mismas unidades que $y$. Al predecir la velocidad de una galaxia a partir de su distancia, el modelo se equivoca típicamente en unos #f(r.rmse, d: 0) km/s. Es mucho frente a una velocidad media de #f(r.ym, d: 0) km/s: la recta no sirve para predecir con precisión una galaxia individual.
- *$R^2$.* Compara el error de la recta con el de un modelo sin pendiente ($y = overline(y)$, la traza $a = 0$ de la superficie). Un valor de #f(r.r2, d: 2) significa que la distancia explica cerca del #f(r.r2 * 100, d: 0) % de la variación de las velocidades; el #f((1 - r.r2) * 100, d: 0) % restante se debe a los movimientos propios de las galaxias y a los errores en las distancias. El coeficiente de correlación es $r = #f(r.r, d: 2)$.
- *En relación con el propósito.* El objetivo de Hubble no era predecir cada velocidad sino establecer si existe una relación creciente y estimar su pendiente. Para eso el modelo es suficiente: la tendencia es clara pese al ruido. Para predicción fina no lo sería. Además, un $R^2$ mayor no habría vuelto correcta la pendiente, porque el problema de fondo estaba en las distancias y eso ninguna medida de ajuste lo detecta.

// ---------- 10 ----------
= Análisis adicional: influencia de un dato (opción B) <influencia>
Se retira temporalmente una galaxia, se recalcula la regresión con las 23 restantes y se repite para cada una de las 24. Así se ve cuánto depende la recta de cada observación.

#fig("/graficos/08_influencia.png", [Izquierda: recta con todos los datos y sin el dato más influyente. Derecha: cambio de la pendiente al quitar cada galaxia.], ancho: 100%)

#table(columns: (1fr, auto, auto, auto, auto, auto, auto), align: (left, right, right, right, right, right, right),
  [Galaxia retirada], [$x$], [$y$], [$a$ nuevo], [$Delta a$], [$b$ nuevo], [$Delta b$],
  ..inf.slice(0, 5).map(p => (p.objeto, f(p.x, d: 3), f(p.y, d: 0), f(p.a, d: 1), f(p.da, d: 1), f(p.b, d: 1), f(p.db, d: 1))).flatten(),
  [Con los 24 datos], [], [], [#f(r.a, d: 1)], [], [#f(r.b, d: 1)], [],
)

- *El dato más influyente es #inf.at(0).objeto.* Está a 2 Mpc, el extremo derecho, y su velocidad (500 km/s) es baja para esa distancia. Al quitarlo la pendiente pasa de #f(r.a, d: 0) a #f(inf.at(0).a, d: 0) km/s/Mpc, un cambio del #f(calc.abs(inf.at(0).da) / r.a * 100, d: 0) %. Un solo punto de 24 mueve la constante de Hubble en esa proporción.
- *Los puntos influyentes están en los extremos de $x$.* Los cinco de la tabla están a 2 Mpc o a menos de 0.3 Mpc, salvo uno a 1.7 Mpc. Un punto lejos de $overline(x)$ actúa como una palanca larga sobre la recta.
- *Residuo grande no significa influencia grande.* NGC 1068 tiene el mayor residuo de todos (#f(p1068.e, d: 0) km/s), pero quitarlo cambia la pendiente solo en #f(p1068.da, d: 1) km/s/Mpc. Como está cerca de $overline(x)$, casi no tiene palanca: al quitarlo la recta se desplaza hacia abajo, cambiando el intercepto y no la inclinación. La influencia depende de las dos cosas a la vez: qué tan lejos está el punto de la recta y qué tan lejos está del centro de los datos.
- *En conjunto la recta es estable.* Al quitar cualquier dato la pendiente queda entre #f(calc.min(..inf.map(p => p.a)), d: 0) y #f(calc.max(..inf.map(p => p.a)), d: 0) km/s/Mpc, siempre positiva y del mismo orden. La conclusión cualitativa (las galaxias lejanas se alejan más rápido) no depende de ninguna observación en particular; el valor exacto de la pendiente sí es sensible a unos pocos puntos.

// ---------- 11 ----------
= Conclusiones y reflexión crítica
+ *El Cálculo Multivariable convierte "la mejor recta" en un problema con solución exacta.* Al ver el error como función de dos variables $S(a,b)$, la condición $nabla S = 0$ da un sistema lineal 2×2 cuya solución es única. Para los datos de Hubble, $a^* approx #f(r.a, d: 1)$ km/s/Mpc y $b^* approx #f(r.b, d: 1)$ km/s.
+ *El Hessiano garantiza que es un mínimo, y global.* $H$ es constante y definido positivo ($det H = #f(r.det, d: 0) > 0$, $S_(a a) > 0$) siempre que haya al menos dos valores distintos de $x$. La superficie es un paraboloide con un único punto más bajo.
+ *La geometría confirma el análisis.* La superficie tiene forma de valle, las secciones son parábolas y las curvas de nivel son elipses centradas en $(a^*, b^*)$. Su inclinación muestra que pendiente e intercepto se compensan, y su alargamiento muestra que hay combinaciones de parámetros peor determinadas que otras.
+ *El computador verifica, no reemplaza.* El método programado coincide con `numpy` y `scipy` hasta el redondeo de máquina, y con el cálculo a mano hasta el redondeo de la calculadora.
+ *El modelo lineal captura la tendencia pero no cada dato.* Con RMSE ≈ #f(r.rmse, d: 0) km/s y $R^2 approx #f(r.r2, d: 2)$, la distancia explica algo más de la mitad de la variación de las velocidades. Los residuos no muestran curvatura global, pero sí una desviación sistemática en las galaxias cercanas, donde dominan los movimientos locales.
+ *Unos pocos datos pesan mucho.* Quitar una sola galaxia en el extremo cambia la pendiente hasta en un #f(calc.abs(inf.at(0).da) / r.a * 100, d: 0) %.

*Limitaciones.*
- Mínimos cuadrados encuentra la mejor recta _para los datos que se le dan_. Las distancias de 1929 estaban subestimadas, y por eso la pendiente es unas 6.5 veces el valor moderno (≈ 70 km/s/Mpc). Con $H_0 = #f(r.a, d: 0)$ la edad estimada del universo, $1 \/ H_0$, sería de unos #f(977.8 / r.a, d: 1) mil millones de años, menos que la edad de la Tierra. Un ajuste excelente no corrige un error sistemático de medición.
- El método supone que todo el error está en $y$. Aquí las distancias $x$ también tienen errores grandes.
- Al elevar al cuadrado, los puntos alejados pesan mucho, lo que hace al método sensible a valores extremos.
- La muestra es pequeña (24 galaxias) y cubre solo hasta 2 Mpc. Extrapolar la recta a distancias mucho mayores no está justificado por estos datos.
- El intercepto no es exactamente cero, aunque la ley física lo exige. Un modelo sin intercepto, $y = a x$, daría $a approx #f(r.sxy / r.sxx, d: 0)$ km/s/Mpc.

// ---------- 12 ----------
= Plan de trabajo <plan>
== Etapas
#table(columns: (auto, 1fr, 1fr),
  [Etapa], [Tareas], [Resultado],
  [1. Entender], [Leer esta guía completa. Cada uno repite en papel las derivadas, el sistema y el Hessiano con sus fórmulas generales], [Todos pueden explicar la @analitico sin mirar],
  [2. Cálculo a mano], [Copiar la tabla de datos, verificar las cuatro sumas con calculadora, resolver el sistema con números y calcular $det H$. Pasarlo en limpio (hojas escaneadas o fotos nítidas)], [Desarrollo manual listo para mostrar en la defensa],
  [3. Código], [Ejecutar los tres programas, leer `regresion.py` línea por línea y relacionar cada función con su fórmula. Actualizar la columna "a mano" de la tabla comparativa], [Código entendido y tabla del §9 con sus valores],
  [4. Análisis], [Redactar con sus palabras la lectura de cada gráfico, de los residuos, de RMSE y $R^2$, y de la influencia de un dato], [Texto de análisis y conclusiones],
  [5. Presentación], [Armar las diapositivas, repartir quién expone qué y ensayar con cronómetro. Hacerse entre ustedes las preguntas de la @defensa], [Diapositivas y ensayo completo],
)

== Reparto sugerido (ajustar al número de integrantes)
#table(columns: (auto, 1fr),
  [Rol], [Responsabilidad principal],
  [Datos y contexto], [Historia y física de la ley de Hubble, fuente, tabla, dispersión],
  [Desarrollo analítico], [Derivadas, gradiente, sistema, Hessiano, justificación del mínimo],
  [Geometría y gráficos], [Superficie, trazas, curvas de nivel y su interpretación],
  [Código y verificación], [Programa, pseudocódigo, diagrama de flujo, tabla comparativa],
  [Análisis y conclusiones], [Residuos, RMSE, $R^2$, influencia de un dato, limitaciones],
)
El reparto es para preparar y exponer. En las preguntas individuales cualquiera puede recibir una pregunta sobre cualquier parte, así que todos deben estudiar todo.

== Estructura sugerida de la presentación
+ Título y pregunta central.
+ El problema: qué midió Hubble, variables y unidades.
+ Tabla de datos y diagrama de dispersión.
+ Modelo y función de error $S(a,b)$.
+ Derivadas parciales y gradiente igual a cero.
+ Sistema de ecuaciones y solución: $a^*$, $b^*$.
+ Hessiano y demostración de que es un mínimo.
+ Superficie de error.
+ Trazas, secciones y curvas de nivel.
+ Código: diagrama de flujo y relación con las fórmulas.
+ Tabla comparativa.
+ Recta de ajuste y residuos.
+ Calidad del modelo e influencia de un dato.
+ Conclusiones y limitaciones.

== Lista de chequeo antes de entregar
#grid(columns: (1fr, 1fr), gutter: 6pt, row-gutter: 7pt,
  [#cb Problema real, fuente citada y unidades], [#cb Tabla de datos y diagrama de dispersión],
  [#cb Derivadas parciales hechas a mano], [#cb Sistema $nabla S = 0$ resuelto a mano],
  [#cb Hessiano y clasificación del punto crítico], [#cb Superficie de error con el mínimo],
  [#cb Trazas y secciones transversales], [#cb Curvas de nivel con $(a^*, b^*)$ marcado],
  [#cb Código con método propio], [#cb Pseudocódigo o diagrama de flujo],
  [#cb Recta óptima junto a otras rectas], [#cb Hessiano verificado numéricamente],
  [#cb Tabla comparativa con valores propios a mano], [#cb Gráfico de residuos e histograma],
  [#cb RMSE y $R^2$ interpretados en contexto], [#cb Análisis adicional (opción B)],
  [#cb Conclusiones con limitaciones], [#cb Ensayo de la defensa con preguntas],
)

// ---------- 13 ----------
= Preguntas tipo defensa <defensa>
#let q(p, resp) = block(breakable: false, below: 0.9em)[*#p* \ #resp]

== Sobre el planteamiento
#q[¿Por qué $S$ es una función de dos variables si los datos tienen $x$ y $y$?][Porque los datos son números fijos. Lo que podemos cambiar es la recta, y una recta queda determinada por $a$ y $b$. $S$ le asigna a cada recta su error.]
#q[¿Por qué se elevan los residuos al cuadrado?][Para que los positivos y negativos no se cancelen, para penalizar más los errores grandes y para que la función sea derivable. Con valor absoluto no podríamos derivar en cero.]
#q[¿Qué significan físicamente $a$ y $b$ en su problema?][$a$ es la constante de Hubble: cuántos km/s aumenta la velocidad de alejamiento por cada megapársec. $b$ es la velocidad que el modelo predice a distancia cero; físicamente debería ser cero.]
#q[¿Por qué creen que un modelo lineal es razonable?][El diagrama de dispersión muestra una tendencia creciente sin curvatura evidente, los residuos no forman un patrón curvo y existe una ley física (la expansión uniforme) que predice proporcionalidad.]

== Sobre el desarrollo analítico
#q[¿Cómo derivaron $S$ respecto de $a$?][Con la regla de la cadena en cada término: $2 (y_i - a x_i - b)$ por la derivada de adentro, que es $-x_i$, tratando $b$ como constante. La derivada de una suma es la suma de las derivadas.]
#q[¿Qué es el gradiente y por qué se iguala a cero?][Es el vector de las derivadas parciales; indica la dirección de mayor crecimiento. En un mínimo la superficie es horizontal en todas las direcciones, así que las dos parciales son cero.]
#q[¿$nabla S = 0$ basta para afirmar que es un mínimo?][No. También se cumple en máximos y puntos de silla. Por eso usamos el Hessiano.]
#q[¿Qué es el Hessiano y qué les dijo?][La matriz de segundas derivadas; mide la curvatura. Su determinante es positivo y $S_(a a) > 0$, así que el punto crítico es un mínimo.]
#q[¿Por qué el Hessiano no depende de $a$ ni de $b$?][Porque $S$ es un polinomio de grado 2 en $a$ y $b$: al derivar dos veces quedan constantes. La superficie tiene la misma curvatura en todo punto.]
#q[¿Podría el determinante ser negativo o cero con otros datos?][Negativo nunca: $det H = 4 n sum (x_i - overline(x))^2$, que es una suma de cuadrados. Cero solo si todos los $x_i$ son iguales; en ese caso hay infinitas rectas con el mismo error y no hay solución única.]
#q[¿El mínimo es local o global?][Global. $S$ es cuadrática, así que $S(a,b) = S_"mín"$ más un término cuadrático con $H$ definida positiva, que es positivo fuera del punto crítico.]
#q[¿Por qué la recta pasa por $(overline(x), overline(y))$?][Porque la ecuación $(partial S)/(partial b) = 0$ dividida por $n$ dice $overline(y) = a overline(x) + b$.]

== Sobre la geometría
#q[¿Qué forma tiene la superficie y por qué?][Un paraboloide elíptico que abre hacia arriba, porque $S$ es cuadrática con Hessiano definido positivo.]
#q[¿Qué representa un punto de la superficie?][Una recta candidata, con parámetros $(a, b)$, y la altura es el error de esa recta. El punto más bajo es la recta de mejor ajuste.]
#q[¿Por qué las curvas de nivel son elipses inclinadas?][Son elipses porque $S$ es cuadrática con mínimo. Están inclinadas porque $S_(a b) = 2 sum x_i != 0$: si sube el intercepto, la pendiente debe bajar para compensar.]
#q[¿Qué información dan las secciones transversales?][Que al fijar un parámetro, el error es una parábola en el otro, con un único mínimo. La sección por el óptimo es la más baja y, al cambiar el valor fijado, el vértice se desplaza.]
#q[¿El mínimo de la superficie vale cero?][No. Valdría cero solo si todos los puntos estuvieran exactamente sobre una recta. Aquí vale cerca de #f(r.S / 1e6, d: 2) millones (km/s)².]

== Sobre el código y los resultados
#q[¿Usaron una función de regresión ya hecha?][Solo para comparar. El método principal lo programamos nosotros: calcula las sumas y aplica las fórmulas que salieron de $nabla S = 0$.]
#q[¿Por qué hay diferencias pequeñas entre los métodos?][Entre el código y las librerías, por redondeo de punto flotante y porque usan otro algoritmo. Con el cálculo a mano, por el redondeo de la calculadora.]
#q[¿Cómo verificaron numéricamente el Hessiano?][Con diferencias finitas sobre $S$, calculando sus valores propios y comprobando que el gradiente en el óptimo es prácticamente cero.]
#q[¿Qué les dice el RMSE?][Que el error típico de la recta es de unos #f(r.rmse, d: 0) km/s, grande frente a una velocidad media de #f(r.ym, d: 0) km/s.]
#q[¿Un $R^2$ de #f(r.r2, d: 2) es bueno o malo?][Depende del propósito. Indica que la distancia explica cerca del #f(r.r2 * 100, d: 0) % de la variación. Alcanza para mostrar que la tendencia existe, no para predecir galaxias individuales.]
#q[¿Por qué los residuos suman cero?][Porque es exactamente lo que dice la ecuación $(partial S)/(partial b) = 0$. Ocurre siempre que el modelo tiene intercepto.]
#q[¿Hay desviaciones sistemáticas?][Sí, en las galaxias más cercanas: las de 0.2 a 0.3 Mpc quedan todas por debajo de la recta. A esas distancias pesa más el movimiento local que la expansión.]
#q[¿Qué dato influye más y por qué?][#inf.at(0).objeto, a 2 Mpc. Está en un extremo de $x$ y tiene velocidad baja; al quitarlo la pendiente sube un #f(calc.abs(inf.at(0).da) / r.a * 100, d: 0) %. La influencia combina estar lejos del centro en $x$ y lejos de la recta en $y$.]
#q[Si el ajuste es correcto, ¿por qué la constante no coincide con la actual?][Porque el método minimiza el error respecto a los datos dados, y las distancias de 1929 estaban subestimadas. Es una limitación de los datos, no del cálculo.]

#pagebreak()
// ---------- Anexo ----------
= Anexo: código del método propio
Archivo `codigo/regresion.py` completo.
#raw(read("/codigo/regresion.py"), lang: "python", block: true)
