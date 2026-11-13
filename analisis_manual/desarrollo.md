# Desarrollo analítico a mano (guion para transcribir en papel)

El enunciado (§7) exige que esto se haga **manualmente**. Este archivo es el guion; el desarrollo explicado paso a paso está en la sección 5 de `Guia_Proyecto_Calculo_Multivariable.pdf`. Los datos están en `datos/hubble_1929.csv`.

## 0. Sumas (verificarlas con calculadora)

| $n$ | $\sum x_i$ | $\sum y_i$ | $\sum x_i^2$ | $\sum x_i y_i$ |
|---|---|---|---|---|
| 24 | 21.873 | 8955 | 29.517795 | 12513.695 |

## 1. Derivadas parciales de $S(a,b) = \sum (y_i - a x_i - b)^2$

$$\frac{\partial S}{\partial a} = -2\sum x_i (y_i - a x_i - b), \qquad \frac{\partial S}{\partial b} = -2\sum (y_i - a x_i - b)$$

## 2. Punto crítico: $\nabla S = 0$ (ecuaciones normales)

$$a\sum x_i^2 + b\sum x_i = \sum x_i y_i \;\Rightarrow\; 29.517795\,a + 21.873\,b = 12513.695$$
$$a\sum x_i + n b = \sum y_i \;\Rightarrow\; 21.873\,a + 24\,b = 8955$$

## 3. Solución

$$a^* = \frac{n\sum x_i y_i - \sum x_i \sum y_i}{n\sum x_i^2 - (\sum x_i)^2} = \frac{300328.68 - 195872.715}{708.42708 - 478.428129} = \frac{104455.965}{229.998951} \approx 454.16$$

$$b^* = \bar{y} - a^*\bar{x} = 373.125 - (454.16)(0.911375) \approx -40.78$$

Error mínimo: $S(a^*, b^*) \approx 1\,193\,442$ (km/s)².

## 4. Hessiano

$$H = \begin{pmatrix} 2\sum x_i^2 & 2\sum x_i \\ 2\sum x_i & 2n \end{pmatrix} = \begin{pmatrix} 59.03559 & 43.746 \\ 43.746 & 48 \end{pmatrix}$$

$$\det H = (59.03559)(48) - (43.746)^2 = 2833.70832 - 1913.712516 \approx 919.996 > 0, \qquad S_{aa} = 59.03559 > 0$$

Conclusión: $(a^*, b^*)$ es un **mínimo**, y es global porque $H$ es constante y definido positivo.

En general $\det H = 4n\sum (x_i - \bar{x})^2 > 0$ siempre que no todos los $x_i$ sean iguales.

## Pendiente

- [ ] Cada integrante repite este desarrollo en papel.
- [ ] Pasar en limpio y guardar aquí las fotos o el escaneo.
- [ ] Anotar los valores de $a$, $b$ y $S_{\min}$ obtenidos a mano (con su redondeo) para la tabla comparativa del §9.
