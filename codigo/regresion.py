"""Regresión lineal por mínimos cuadrados: implementación PROPIA.

Cada función corresponde a un paso del desarrollo analítico:

    S(a,b) = Σ (y_i - a x_i - b)²
    ∇S = 0  →  a Σx² + b Σx = Σxy
               a Σx  + b n  = Σy
    H = [[2Σx², 2Σx], [2Σx, 2n]]

No se usa ninguna función de regresión de librería en este archivo.
"""
import csv
import math
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RUTA_DATOS = RAIZ / "datos" / "hubble_1929.csv"


def cargar_datos(ruta=RUTA_DATOS):
    """Lee el CSV y devuelve (nombres, x, y) como listas."""
    nombres, x, y = [], [], []
    with open(ruta, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            nombres.append(fila["objeto"])
            x.append(float(fila["distancia_Mpc"]))
            y.append(float(fila["velocidad_km_s"]))
    return nombres, x, y


def sumas(x, y):
    """Calcula n, Σx, Σy, Σx², Σxy: lo único que necesitan las ecuaciones normales."""
    n = len(x)
    sx = sy = sxx = sxy = 0.0
    for xi, yi in zip(x, y):
        sx += xi
        sy += yi
        sxx += xi * xi
        sxy += xi * yi
    return n, sx, sy, sxx, sxy


def ajustar(x, y):
    """Resuelve ∇S = 0 (regla de Cramer sobre el sistema 2×2) y devuelve (a*, b*)."""
    n, sx, sy, sxx, sxy = sumas(x, y)
    determinante = n * sxx - sx * sx
    if determinante == 0:
        raise ValueError("Todos los x son iguales: el sistema no tiene solución única.")
    a = (n * sxy - sx * sy) / determinante
    b = (sxx * sy - sx * sxy) / determinante
    return a, b


def error_cuadratico(a, b, x, y):
    """S(a,b) = Σ (y_i - a x_i - b)²."""
    return sum((yi - a * xi - b) ** 2 for xi, yi in zip(x, y))


def gradiente(a, b, x, y):
    """(∂S/∂a, ∂S/∂b) = (-2 Σ x_i e_i, -2 Σ e_i)."""
    dSa = dSb = 0.0
    for xi, yi in zip(x, y):
        e = yi - a * xi - b
        dSa += -2 * xi * e
        dSb += -2 * e
    return dSa, dSb


def hessiano(x):
    """Matriz de segundas derivadas de S. Es constante: no depende de a ni de b."""
    n = len(x)
    sx = sum(x)
    sxx = sum(xi * xi for xi in x)
    return [[2 * sxx, 2 * sx], [2 * sx, 2 * n]]


def analizar_hessiano(H):
    """Devuelve determinante, traza y valores propios de una matriz simétrica 2×2."""
    det = H[0][0] * H[1][1] - H[0][1] * H[1][0]
    traza = H[0][0] + H[1][1]
    raiz = math.sqrt(traza * traza - 4 * det)
    return det, traza, ((traza - raiz) / 2, (traza + raiz) / 2)


def residuos(a, b, x, y):
    """e_i = y_i - (a x_i + b)."""
    return [yi - (a * xi + b) for xi, yi in zip(x, y)]


def rmse(a, b, x, y):
    return math.sqrt(error_cuadratico(a, b, x, y) / len(x))


def r_cuadrado(a, b, x, y):
    media = sum(y) / len(y)
    total = sum((yi - media) ** 2 for yi in y)
    return 1 - error_cuadratico(a, b, x, y) / total


if __name__ == "__main__":
    nombres, x, y = cargar_datos()
    n, sx, sy, sxx, sxy = sumas(x, y)
    a, b = ajustar(x, y)
    H = hessiano(x)
    det, traza, (l1, l2) = analizar_hessiano(H)
    ga, gb = gradiente(a, b, x, y)

    print(f"n = {n}")
    print(f"Σx = {sx:.4f}   Σy = {sy:.1f}   Σx² = {sxx:.6f}   Σxy = {sxy:.4f}")
    print(f"a* = {a:.6f} km/s/Mpc")
    print(f"b* = {b:.6f} km/s")
    print(f"S(a*, b*) = {error_cuadratico(a, b, x, y):.4f}")
    print(f"Gradiente en (a*, b*) = ({ga:.2e}, {gb:.2e})")
    print(f"Hessiano = {H}")
    print(f"det H = {det:.4f}   H11 = {H[0][0]:.4f}   valores propios = {l1:.4f}, {l2:.4f}")
    print(f"RMSE = {rmse(a, b, x, y):.4f} km/s   R² = {r_cuadrado(a, b, x, y):.6f}")
