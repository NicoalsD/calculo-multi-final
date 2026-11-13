"""Genera todas las figuras del proyecto en graficos/."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import regresion as rg

SALIDA = rg.RAIZ / "graficos"
AZUL, ROJO, GRIS, VERDE, NARANJA = "#1f4e79", "#c0392b", "#7f8c8d", "#2e7d32", "#e67e22"
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 200, "font.size": 10,
                     "axes.grid": True, "grid.alpha": 0.3, "axes.spines.top": False,
                     "axes.spines.right": False})

nombres, x, y = rg.cargar_datos()
a, b = rg.ajustar(x, y)
Smin = rg.error_cuadratico(a, b, x, y)
xa, ya = np.array(x), np.array(y)
EJE_X, EJE_Y = "Distancia $x$ (Mpc)", "Velocidad de recesión $y$ (km/s)"


def S_malla(A, B):
    """S(a,b) evaluada sobre una malla de valores de a y b."""
    return ((ya[None, None, :] - A[..., None] * xa[None, None, :] - B[..., None]) ** 2).sum(axis=-1)


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(SALIDA / nombre)
    plt.close(fig)
    print("  ", nombre)


def fig_dispersion():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.scatter(xa, ya, color=AZUL, zorder=3)
    ax.axhline(0, color=GRIS, lw=0.8)
    ax.set(xlabel=EJE_X, ylabel=EJE_Y, title="Datos de Hubble (1929): 24 galaxias")
    guardar(fig, "01_dispersion.png")


def fig_rectas():
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    xs = np.linspace(0, 2.1, 50)
    ax.scatter(xa, ya, color=AZUL, zorder=3, label="Datos observados")
    otras = [(a + 250, b - 150, NARANJA), (a - 250, b + 200, VERDE), (a, b + 250, GRIS)]
    for p, q, c in otras:
        ax.plot(xs, p * xs + q, "--", color=c, lw=1.3,
                label=f"a={p:.0f}, b={q:.0f}  →  S={rg.error_cuadratico(p, q, x, y):,.0f}")
    ax.plot(xs, a * xs + b, color=ROJO, lw=2.2,
            label=f"Óptima: a*={a:.1f}, b*={b:.1f}  →  S={Smin:,.0f}")
    ax.set(xlabel=EJE_X, ylabel=EJE_Y, title="Recta de mínimos cuadrados frente a otras rectas")
    ax.legend(fontsize=8)
    guardar(fig, "02_recta_ajuste.png")


def fig_superficie():
    A, B = np.meshgrid(np.linspace(a - 500, a + 500, 90), np.linspace(b - 500, b + 500, 90))
    Z = S_malla(A, B)
    fig = plt.figure(figsize=(7, 5.2))
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(A, B, Z / 1e6, cmap="viridis", alpha=0.85, linewidth=0)
    ax.contour(A, B, Z / 1e6, 12, zdir="z", offset=0, cmap="viridis", linewidths=0.7)
    ax.scatter([a], [b], [Smin / 1e6], color=ROJO, s=50, depthshade=False)
    ax.plot([a, a], [b, b], [0, Smin / 1e6], color=ROJO, lw=1)
    ax.set(xlabel="a (km/s/Mpc)", ylabel="b (km/s)", zlabel="S(a,b)  (×10⁶)",
           title="Superficie de error z = S(a, b)")
    ax.set_zlim(0)
    ax.view_init(elev=28, azim=-58)
    guardar(fig, "03_superficie.png")


def fig_trazas():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.9))
    aa = np.linspace(a - 500, a + 500, 200)
    for q, c, est in ((b, ROJO, "-"), (0, "black", ":"), (b + 200, NARANJA, "--"), (b - 200, VERDE, "--")):
        ax1.plot(aa, [rg.error_cuadratico(p, q, x, y) / 1e6 for p in aa], est, color=c,
                 label=f"b = {q:.0f}" + ("  (b*)" if q == b else "  (traza)" if q == 0 else ""))
    ax1.axvline(a, color=GRIS, lw=0.8, ls=":")
    ax1.set(xlabel="a (km/s/Mpc)", ylabel="S  (×10⁶)", title="Traza y secciones con b fijo: S(a, b₀)")
    ax1.legend(fontsize=8)
    bb = np.linspace(b - 500, b + 500, 200)
    for p, c, est in ((a, ROJO, "-"), (0, "black", ":"), (a + 200, NARANJA, "--"), (a - 200, VERDE, "--")):
        ax2.plot(bb, [rg.error_cuadratico(p, q, x, y) / 1e6 for q in bb], est, color=c,
                 label=f"a = {p:.0f}" + ("  (a*)" if p == a else "  (traza)" if p == 0 else ""))
    ax2.axvline(b, color=GRIS, lw=0.8, ls=":")
    ax2.set(xlabel="b (km/s)", ylabel="S  (×10⁶)", title="Traza y secciones con a fijo: S(a₀, b)")
    ax2.legend(fontsize=8)
    guardar(fig, "04_trazas.png")


def fig_curvas_nivel():
    A, B = np.meshgrid(np.linspace(a - 500, a + 500, 300), np.linspace(b - 500, b + 500, 300))
    Z = S_malla(A, B)
    niveles = Smin + np.array([0.02, 0.1, 0.25, 0.5, 1, 1.75, 2.75, 4, 6]) * 1e6
    fig, ax = plt.subplots(figsize=(6.4, 5))
    cs = ax.contour(A, B, Z, levels=niveles, cmap="viridis")
    ax.clabel(cs, fmt=lambda v: f"{v / 1e6:.2f}", fontsize=7)
    ax.plot(a, b, "o", color=ROJO, label=f"(a*, b*) = ({a:.1f}, {b:.1f})")
    ax.axvline(a, color=GRIS, lw=0.7, ls=":")
    ax.axhline(b, color=GRIS, lw=0.7, ls=":")
    ax.set(xlabel="a (km/s/Mpc)", ylabel="b (km/s)",
           title="Curvas de nivel de S(a, b)  (valores ×10⁶)")
    ax.legend(fontsize=8, loc="upper right")
    guardar(fig, "05_curvas_nivel.png")


def fig_residuos():
    e = np.array(rg.residuos(a, b, x, y))
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.axhline(0, color=ROJO, lw=1.2)
    ax.vlines(xa, 0, e, color=GRIS, lw=0.8)
    ax.scatter(xa, e, color=AZUL, zorder=3)
    for i in np.argsort(-np.abs(e))[:3]:
        ax.annotate(nombres[i], (xa[i], e[i]), textcoords="offset points", xytext=(6, 4), fontsize=7)
    ax.set(xlabel=EJE_X, ylabel="Residuo $e_i$ (km/s)", title="Residuos en función de la distancia")
    guardar(fig, "06_residuos.png")

    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.hist(e, bins=np.arange(-500, 700, 100), color=AZUL, edgecolor="white")
    ax.axvline(0, color=ROJO, lw=1.2)
    ax.set(xlabel="Residuo $e_i$ (km/s)", ylabel="Número de galaxias", title="Histograma de los residuos")
    guardar(fig, "07_histograma_residuos.png")


def fig_influencia():
    n = len(x)
    loo = [rg.ajustar(x[:i] + x[i + 1:], y[:i] + y[i + 1:]) for i in range(n)]
    da = np.array([p - a for p, _ in loo])
    k = int(np.argmax(np.abs(da)))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4), gridspec_kw={"width_ratios": [1.15, 1]})
    xs = np.linspace(0, 2.1, 50)
    ax1.scatter(xa, ya, color=AZUL, zorder=3)
    ax1.scatter([xa[k]], [ya[k]], s=130, facecolors="none", edgecolors=ROJO, lw=1.8, zorder=4,
                label=f"Punto retirado: {nombres[k]}")
    ax1.plot(xs, a * xs + b, color=ROJO, lw=2, label=f"Con los 24 datos: a={a:.1f}, b={b:.1f}")
    ax1.plot(xs, loo[k][0] * xs + loo[k][1], "--", color=VERDE, lw=2,
             label=f"Sin ese punto: a={loo[k][0]:.1f}, b={loo[k][1]:.1f}")
    ax1.set(xlabel=EJE_X, ylabel=EJE_Y, title="Recta con y sin el dato más influyente")
    ax1.legend(fontsize=7.5)
    colores = [ROJO if i == k else AZUL for i in range(n)]
    ax2.bar(range(1, n + 1), da, color=colores)
    ax2.axhline(0, color="black", lw=0.8)
    ax2.set(xlabel="Galaxia retirada (n.º de fila en la tabla)", ylabel="Cambio en la pendiente Δa (km/s/Mpc)",
            title="Efecto de quitar cada dato")
    ax2.set_xticks(range(1, n + 1, 2))
    guardar(fig, "08_influencia.png")


if __name__ == "__main__":
    SALIDA.mkdir(exist_ok=True)
    print("Figuras generadas en graficos/:")
    fig_dispersion()
    fig_rectas()
    fig_superficie()
    fig_trazas()
    fig_curvas_nivel()
    fig_residuos()
    fig_influencia()
