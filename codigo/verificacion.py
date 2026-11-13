"""Verificación del método propio contra librerías y análisis adicional (opción B).

Genera docs/guia/resultados.json, que alimenta el PDF de la guía.
"""
import json

import numpy as np
from scipy import stats

import regresion as rg

SALIDA = rg.RAIZ / "docs" / "guia" / "resultados.json"


def hessiano_numerico(a, b, x, y, h=1e-3):
    """Hessiano por diferencias finitas centradas, para compararlo con el analítico."""
    S = lambda p, q: rg.error_cuadratico(p, q, x, y)
    haa = (S(a + h, b) - 2 * S(a, b) + S(a - h, b)) / h**2
    hbb = (S(a, b + h) - 2 * S(a, b) + S(a, b - h)) / h**2
    hab = (S(a + h, b + h) - S(a + h, b - h) - S(a - h, b + h) + S(a - h, b - h)) / (4 * h**2)
    return [[haa, hab], [hab, hbb]]


def dejar_uno_fuera(x, y):
    """Opción B: recalcula la recta quitando cada punto, uno a la vez."""
    filas = []
    for i in range(len(x)):
        xs, ys = x[:i] + x[i + 1:], y[:i] + y[i + 1:]
        filas.append(rg.ajustar(xs, ys))
    return filas


def main():
    nombres, x, y = rg.cargar_datos()
    n, sx, sy, sxx, sxy = rg.sumas(x, y)

    # 1) Método propio
    a_cod, b_cod = rg.ajustar(x, y)
    S_cod = rg.error_cuadratico(a_cod, b_cod, x, y)

    # 2) "A mano": mismas fórmulas, redondeando como en una calculadora
    a_man = round((n * sxy - sx * sy) / (n * sxx - sx**2), 2)
    b_man = round(sy / n - a_man * sx / n, 2)
    S_man = rg.error_cuadratico(a_man, b_man, x, y)

    # 3) Librerías
    a_np, b_np = np.polyfit(x, y, 1)
    S_np = rg.error_cuadratico(a_np, b_np, x, y)
    lr = stats.linregress(x, y)
    S_sp = rg.error_cuadratico(lr.slope, lr.intercept, x, y)

    def dif(*v):
        return max(v) - min(v)

    # Hessiano
    H = rg.hessiano(x)
    det, traza, (l1, l2) = rg.analizar_hessiano(H)
    Hn = hessiano_numerico(a_cod, b_cod, x, y)
    vp_np = np.linalg.eigvalsh(np.array(H))
    grad = rg.gradiente(a_cod, b_cod, x, y)

    # Calidad
    e = rg.residuos(a_cod, b_cod, x, y)
    rmse = rg.rmse(a_cod, b_cod, x, y)
    r2 = rg.r_cuadrado(a_cod, b_cod, x, y)

    # Opción B
    loo = dejar_uno_fuera(x, y)
    influencia = sorted(
        ({"objeto": nombres[i], "x": x[i], "y": y[i], "e": e[i],
          "a": loo[i][0], "b": loo[i][1],
          "da": loo[i][0] - a_cod, "db": loo[i][1] - b_cod} for i in range(n)),
        key=lambda f: abs(f["da"]), reverse=True)

    print("Tabla comparativa (§9)")
    print(f"{'':6}{'A mano':>16}{'Código propio':>18}{'numpy.polyfit':>18}{'scipy.linregress':>18}{'Dif. máx':>12}")
    for nom, vals in (("a", (a_man, a_cod, a_np, lr.slope)),
                      ("b", (b_man, b_cod, b_np, lr.intercept)),
                      ("Smin", (S_man, S_cod, S_np, S_sp))):
        print(f"{nom:6}{vals[0]:16.6f}{vals[1]:18.6f}{vals[2]:18.6f}{vals[3]:18.6f}{dif(*vals):12.2e}")
    print(f"\nDiferencia código propio vs librerías: a {dif(a_cod, a_np, lr.slope):.2e}, "
          f"b {dif(b_cod, b_np, lr.intercept):.2e}")
    print(f"Gradiente en el mínimo: {grad}")
    print(f"Hessiano analítico: {H}\nHessiano numérico:  {Hn}")
    print(f"det = {det:.4f}, valores propios = {l1:.4f}, {l2:.4f} (numpy: {vp_np})")
    print(f"RMSE = {rmse:.3f}, R² = {r2:.4f}, r = {lr.rvalue:.4f}")
    print("\nInfluencia (los 5 puntos que más cambian la pendiente al quitarlos):")
    for f in influencia[:5]:
        print(f"  {f['objeto']:26} x={f['x']:<6} y={f['y']:<7} a={f['a']:.2f} (Δa={f['da']:+.2f})  b={f['b']:.2f} (Δb={f['db']:+.2f})")

    orden_res = sorted(range(n), key=lambda i: abs(e[i]), reverse=True)
    resultados = {
        "n": n, "sx": sx, "sy": sy, "sxx": sxx, "sxy": sxy,
        "xm": sx / n, "ym": sy / n,
        "a": a_cod, "b": b_cod, "S": S_cod,
        "a_man": a_man, "b_man": b_man, "S_man": S_man,
        "a_np": float(a_np), "b_np": float(b_np), "S_np": S_np,
        "a_sp": lr.slope, "b_sp": lr.intercept, "S_sp": S_sp,
        "da": dif(a_man, a_cod, a_np, lr.slope),
        "db": dif(b_man, b_cod, b_np, lr.intercept),
        "dS": dif(S_man, S_cod, S_np, S_sp),
        "da_lib": dif(a_cod, a_np, lr.slope), "db_lib": dif(b_cod, b_np, lr.intercept),
        "H": H, "Hn": Hn, "det": det, "traza": traza, "l1": l1, "l2": l2,
        "grad": list(grad),
        "rmse": rmse, "r2": r2, "r": lr.rvalue,
        "e_media": sum(e) / n, "e_pos": sum(1 for v in e if v > 0), "e_neg": sum(1 for v in e if v < 0),
        "datos": [{"objeto": nombres[i], "x": x[i], "y": y[i], "x2": x[i] ** 2, "xy": x[i] * y[i],
                   "pred": a_cod * x[i] + b_cod, "e": e[i]} for i in range(n)],
        "mayores_residuos": [{"objeto": nombres[i], "x": x[i], "y": y[i], "e": e[i]} for i in orden_res[:5]],
        "influencia": influencia,
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(resultados, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nResultados guardados en {SALIDA.relative_to(rg.RAIZ)}")


if __name__ == "__main__":
    main()
