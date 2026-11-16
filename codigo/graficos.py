"""Genera todas las figuras del proyecto en graficos/.

Cada figura se dibuja por capas: graficos/NN_nombre.png es la figura de la guía y
graficos/pasos/nombre-k.png muestra las capas 1..k (la presentación las va revelando).
Todas comparten la misma cuadrícula (CUAD) y los mismos límites (LIM) por variable,
así una misma magnitud se lee igual en todas las gráficas.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.legend import Legend
from matplotlib.patches import Rectangle
from matplotlib.ticker import MultipleLocator

import regresion as rg

SALIDA = rg.RAIZ / "graficos"
PASOS = SALIDA / "pasos"
AZUL, ROJO, GRIS, VERDE, NARANJA = "#1f4e79", "#c0392b", "#7f8c8d", "#2e7d32", "#e67e22"
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 200, "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})

nombres, x, y = rg.cargar_datos()
a, b = rg.ajustar(x, y)
Smin = rg.error_cuadratico(a, b, x, y)
xa, ya = np.array(x), np.array(y)
e = ya - (a * xa + b)
RMSE = rg.rmse(a, b, x, y)
EJE_X, EJE_Y = "Distancia $x$ (Mpc)", "Velocidad de recesión $y$ (km/s)"
EJE_A, EJE_B, EJE_S = "a (km/s/Mpc)", "b (km/s)", "S(a,b)  (×10⁶)"

# Cuadrícula común: (paso mayor, paso menor) por magnitud. y y los residuos son km/s: misma cuadrícula.
CUAD = {"x": (0.5, 0.1), "y": (200, 50), "e": (200, 50), "a": (100, 25), "b": (100, 25), "S": (1, 0.25)}
LIM = {"x": (0, 2.1), "y": (-300, 1200), "e": (-500, 600), "a": (50, 850), "b": (-450, 450)}
H = np.array(rg.hessiano(x))
LAM, VEC = np.linalg.eigh(H)  # LAM[0] ≈ 9.43 (dirección del valle), LAM[1] ≈ 97.61


def idx(nombre):
    return nombres.index(nombre)


def S_malla(A, B):
    """S(a,b) evaluada sobre una malla de valores de a y b."""
    return ((ya[None, None, :] - A[..., None] * xa[None, None, :] - B[..., None]) ** 2).sum(axis=-1)


def malla(n=200):
    return np.meshgrid(np.linspace(*LIM["a"], n), np.linspace(*LIM["b"], n))


def ejes(ax, ex=None, ey=None, ez=None):
    """Límites y cuadrícula común (mayor y menor) para las magnitudes de cada eje."""
    for k, eje, lim in ((ex, ax.xaxis, ax.set_xlim), (ey, ax.yaxis, ax.set_ylim),
                        (ez, getattr(ax, "zaxis", None), getattr(ax, "set_zlim", None))):
        if not k:
            continue
        mayor, menor = CUAD[k]
        eje.set_major_locator(MultipleLocator(mayor))
        if ez is None:  # en 3D solo la cuadrícula mayor: la menor satura el dibujo
            eje.set_minor_locator(MultipleLocator(menor))
        if k in LIM:
            lim(*LIM[k])
    ax.grid(True, which="major", color="#8a93a3", alpha=0.45, lw=0.7)
    if ez is None:
        ax.grid(True, which="minor", color="#8a93a3", alpha=0.16, lw=0.45)
    ax.set_axisbelow(True)


def leyenda(ax, **kw):
    """Leyenda que se rehace en cada paso con solo lo visible."""
    ax._ley = kw
    ax.legend(**kw)


class Capas:
    """Agrupa lo que se dibuja entre dos cortes: cada corte cierra una capa."""

    def __init__(self, fig):
        self.fig, self.capas = fig, []
        self.vistos = self._hijos()

    def _hijos(self):
        return {id(c): c for ax in self.fig.axes for c in ax.get_children() if not isinstance(c, Legend)}

    def corte(self):
        nuevos = self._hijos()
        self.capas.append([c for k, c in nuevos.items() if k not in self.vistos])
        self.vistos = nuevos


def guardar(fig, nombre, capas=None, en_guia=None, pasos=None):
    """Guarda la figura de la guía y, si hay capas, un PNG por paso en graficos/pasos/."""
    fig.tight_layout()
    capas = capas.capas if isinstance(capas, Capas) else capas

    def mostrar(k):
        visibles = {id(c) for capa in capas[:k + 1] for c in capa}
        for c in (c for capa in capas for c in capa):
            c.set_visible(id(c) in visibles)
        for ax in fig.axes:
            if hasattr(ax, "_ley"):
                pares = [(h, l) for h, l in zip(*ax.get_legend_handles_labels()) if h.get_visible()]
                if ax.get_legend():
                    ax.get_legend().remove()
                if pares:
                    ax.legend(*zip(*pares), **ax._ley)

    if capas:
        PASOS.mkdir(exist_ok=True)
        for k in range(len(capas)):
            mostrar(k)
            fig.savefig(PASOS / f"{pasos}-{k + 1}.png")
        mostrar(len(capas) - 1 if en_guia is None else en_guia)
    if nombre:
        fig.savefig(SALIDA / nombre)
    plt.close(fig)
    print("  ", nombre or "", f"(+{len(capas)} pasos: {pasos}-k)" if capas else "")


def nota(ax, xy, texto, color=AZUL, **kw):
    kw.setdefault("fontsize", 8)
    kw.setdefault("bbox", dict(fc="white", ec="none", alpha=0.75, pad=0.8))
    return ax.annotate(texto, xy, color=color, fontweight="bold", **kw)


# ---------------------------------------------------------------- datos


def fig_dispersion():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    capas = Capas(fig)
    ax.scatter(xa, ya, color=AZUL, zorder=3)
    ax.axhline(0, color=GRIS, lw=0.8)
    ax.set(xlabel=EJE_X, ylabel=EJE_Y, title="Datos de Hubble (1929): 24 galaxias")
    ejes(ax, "x", "y")
    capas.corte()
    # 2. Tendencia: rango de velocidades a 2 Mpc y bajo 0.5 Mpc
    for x0, x1, y0, y1, txt in ((1.93, 2.07, 500, 1090, "500 a 1090"), (0.0, 0.5, -220, 290, "−220 a 290")):
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=NARANJA, alpha=0.15, ec=NARANJA, lw=1.2))
        nota(ax, (x0 + (x1 - x0) / 2, y1 + 30) if x0 < 1 else (1.9, 700), txt + " km/s", NARANJA,
             ha="center" if x0 < 1 else "right")
    capas.corte()
    # 3. Forma: la nube sube como una franja recta
    ax.annotate("", (2.05, 1130), (0.02, -60), arrowprops=dict(arrowstyle="-|>", color=VERDE, lw=2, ls="--"))
    nota(ax, (0.62, 760), "sube sin curvarse", VERDE, rotation=29)
    capas.corte()
    # 4. Dispersión: a 0.9 Mpc hay velocidades de −30 a 650
    ax.annotate("", (0.86, 650), (0.86, -30), arrowprops=dict(arrowstyle="<->", color=ROJO, lw=1.6))
    nota(ax, (0.82, 540), "680 km/s\na la misma distancia", ROJO, ha="right")
    capas.corte()
    guardar(fig, "01_dispersion.png", capas, en_guia=0, pasos="dispersion")


def fig_construccion():
    """Desglose de S para una recta cualquiera: predicción, residuos y cuadrados."""
    p, q = 204, 159
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    capas = Capas(fig)
    xs = np.array(LIM["x"])
    ax.scatter(xa, ya, color=AZUL, zorder=4, label="Datos $(x_i, y_i)$")
    ax.plot(xs, p * xs + q, color=GRIS, lw=1.8, label=f"Recta de prueba: a = {p}, b = {q}")
    ax.scatter(xa, p * xa + q, marker="_", s=90, color=GRIS, zorder=4, label=r"Predicción $\hat y_i = a x_i + b$")
    ax.set(xlabel=EJE_X, ylabel=EJE_Y, title="Cómo se calcula S(a, b) para una recta")
    ejes(ax, "x", "y")
    leyenda(ax, fontsize=8, loc="upper left")
    fig.tight_layout()
    capas.corte()
    r = ya - (p * xa + q)
    ax.vlines(xa, p * xa + q, ya, color=ROJO, lw=1.4, label=r"Residuo $e_i = y_i - \hat y_i$")
    capas.corte()
    # Cuadrado de lado |e_i| en pantalla: en unidades de x mide |e_i|·(px por km/s)/(px por Mpc)
    bb = ax.get_window_extent()
    k = (bb.height / np.ptp(LIM["y"])) / (bb.width / np.ptp(LIM["x"]))
    for xi, yi, ri in zip(xa, ya, r):
        ax.add_patch(Rectangle((xi, yi - ri), abs(ri) * k, ri, fc=ROJO, alpha=0.13, ec=ROJO, lw=0.5))
    ax.add_patch(Rectangle((0, 0), 0, 0, fc=ROJO, alpha=0.25, label=r"Cuadrado $e_i^2$"))
    S = rg.error_cuadratico(p, q, x, y)
    nota(ax, (1.25, -230), f"S = Σ eᵢ² = {S / 1e6:.2f} ×10⁶", ROJO, fontsize=10)
    capas.corte()
    guardar(fig, None, capas, pasos="construccion")


def fig_rectas():
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    xs = np.array(LIM["x"])
    ax.scatter(xa, ya, color=AZUL, zorder=3, label="Datos observados")
    otras = [(a + 250, b - 150, NARANJA), (a - 250, b + 200, VERDE), (a, b + 250, GRIS)]
    for p, q, c in otras:
        ax.plot(xs, p * xs + q, "--", color=c, lw=1.3,
                label=f"a={p:.0f}, b={q:.0f}  →  S={rg.error_cuadratico(p, q, x, y):,.0f}")
    ax.plot(xs, a * xs + b, color=ROJO, lw=2.2,
            label=f"Óptima: a*={a:.1f}, b*={b:.1f}  →  S={Smin:,.0f}")
    ax.set(xlabel=EJE_X, ylabel=EJE_Y, title="Recta de mínimos cuadrados frente a otras rectas")
    ejes(ax, "x", "y")
    ax.legend(fontsize=8, loc="upper left")
    guardar(fig, "02_recta_ajuste.png")


# ---------------------------------------------------------------- geometría


def fig_superficie():
    A, B = malla(90)
    Z = S_malla(A, B)
    fig = plt.figure(figsize=(7, 5.2))
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(A, B, Z / 1e6, cmap="viridis", alpha=0.85, linewidth=0)
    ax.contour(A, B, Z / 1e6, 12, zdir="z", offset=0, cmap="viridis", linewidths=0.7)
    ax.scatter([a], [b], [Smin / 1e6], color=ROJO, s=50, depthshade=False)
    ax.plot([a, a], [b, b], [0, Smin / 1e6], color=ROJO, lw=1)
    ax.set(xlabel=EJE_A, ylabel=EJE_B, zlabel=EJE_S, title="Superficie de error z = S(a, b)")
    ejes(ax, "a", "b", "S")
    ax.set_zlim(0)
    ax.view_init(elev=28, azim=-58)
    guardar(fig, "03_superficie.png")


def vertice_a(q):
    """Mejor a con b = q fijo: ∂S/∂a = 0  →  a = (Σxy − qΣx)/Σx²."""
    return (xa @ ya - q * xa.sum()) / (xa @ xa)


def vertice_b(p):
    """Mejor b con a = p fijo: ∂S/∂b = 0  →  b = (Σy − pΣx)/n."""
    return (ya.sum() - p * xa.sum()) / len(xa)


def fig_trazas():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.9))
    capas = Capas(fig)
    aa, bb = np.linspace(*LIM["a"], 200), np.linspace(*LIM["b"], 200)
    Sa = lambda q: S_malla(aa, np.full_like(aa, q)).ravel() / 1e6
    Sb = lambda p: S_malla(np.full_like(bb, p), bb).ravel() / 1e6
    ax1.plot(aa, Sa(b), color=ROJO, lw=2, label=f"b = {b:.0f}  (b*)")
    ax2.plot(bb, Sb(a), color=ROJO, lw=2, label=f"a = {a:.0f}  (a*)")
    ax1.axvline(a, color=GRIS, lw=0.8, ls=":")
    ax2.axvline(b, color=GRIS, lw=0.8, ls=":")
    ax1.set(xlabel=EJE_A, ylabel="S  (×10⁶)", title="Sección con b fijo: S(a, b₀)")
    ax2.set(xlabel=EJE_B, ylabel="S  (×10⁶)", title="Sección con a fijo: S(a₀, b)")
    for ax, k in ((ax1, "a"), (ax2, "b")):
        ejes(ax, k, "S")
        ax.set_ylim(0, 8)
        leyenda(ax, fontsize=8, loc="upper center")
    capas.corte()
    for d, c in ((200, NARANJA), (-200, VERDE)):
        ax1.plot(aa, Sa(b + d), "--", color=c, label=f"b = {b + d:.0f}")
        ax2.plot(bb, Sb(a + d), "--", color=c, label=f"a = {a + d:.0f}")
    capas.corte()
    # Lugar de los vértices: al subir b el mejor a baja (y viceversa)
    qs, ps = np.array([b - 200, b, b + 200]), np.array([a - 200, a, a + 200])
    ax1.plot(vertice_a(qs), [rg.error_cuadratico(vertice_a(q), q, x, y) / 1e6 for q in qs], "o-",
             color="black", ms=4, lw=1, label="Vértices")
    ax2.plot(vertice_b(ps), [rg.error_cuadratico(p, vertice_b(p), x, y) / 1e6 for p in ps], "o-",
             color="black", ms=4, lw=1, label="Vértices")
    capas.corte()
    ax1.plot(aa, Sa(0), ":", color="black", lw=1.6, label="b = 0  (traza)")
    ax2.plot(bb, Sb(0), ":", color="black", lw=1.6, label="a = 0  (traza)")
    va = vertice_a(0)
    ax1.plot([va], [rg.error_cuadratico(va, 0, x, y) / 1e6], "s", color="black", ms=5)
    nota(ax1, (va, rg.error_cuadratico(va, 0, x, y) / 1e6), f" a = {va:.1f}", "black", xytext=(4, -12),
         textcoords="offset points")
    capas.corte()
    guardar(fig, "04_trazas.png", capas, pasos="trazas")


def fig_curvas_nivel():
    A, B = malla(300)
    Z = S_malla(A, B)
    niveles = Smin + np.array([0.02, 0.1, 0.25, 0.5, 1, 1.75, 2.75, 4]) * 1e6
    fig, ax = plt.subplots(figsize=(5.6, 5.6))
    capas = Capas(fig)
    cs = ax.contour(A, B, Z, levels=niveles, cmap="viridis", linewidths=1.1)
    ax.clabel(cs, fmt=lambda v: f"{v / 1e6:.2f}", fontsize=7)
    ax.plot(a, b, "o", color=ROJO, ms=7, zorder=5, label=f"(a*, b*) = ({a:.1f}, {b:.1f})")
    ax.axvline(a, color=GRIS, lw=0.7, ls=":")
    ax.axhline(b, color=GRIS, lw=0.7, ls=":")
    ax.set(xlabel=EJE_A, ylabel=EJE_B, title="Curvas de nivel de S(a, b)  (valores ×10⁶)")
    ejes(ax, "a", "b")
    ax.set_aspect("equal")  # misma escala en a y b: la inclinación y la forma son las reales
    leyenda(ax, fontsize=7.5, loc="lower left")
    capas.corte()
    # Una curva: todas las rectas con S = Smin + 10⁶
    dS = 1e6
    t = np.linspace(0, 2 * np.pi, 200)
    ejes_e = np.sqrt(2 * dS / LAM)  # semiejes de la elipse ΔS = ½ vᵀHv
    elipse = np.array([a, b])[:, None] + VEC @ (ejes_e[:, None] * np.array([np.cos(t), np.sin(t)]))
    ax.plot(*elipse, color=NARANJA, lw=2.6, label=f"Mismo error: S = {(Smin + dS) / 1e6:.2f} ×10⁶")
    capas.corte()
    for i, c in ((0, AZUL), (1, VERDE)):  # ejes principales = vectores propios del Hessiano
        v = VEC[:, i] * 520
        ax.plot([a - v[0], a + v[0]], [b - v[1], b + v[1]], "--", color=c, lw=1.2,
                label=f"Eje propio λ = {LAM[i]:.2f}")
    capas.corte()
    for i, c in ((0, AZUL), (1, VERDE)):
        v = VEC[:, i] * ejes_e[i]
        ax.annotate("", (a + v[0], b + v[1]), (a, b), arrowprops=dict(arrowstyle="-|>", color=c, lw=2))
        nota(ax, (a + v[0], b + v[1]), f"{ejes_e[i]:.0f}", c, xytext=(-34, -4) if i else (8, 0), textcoords="offset points")
    nota(ax, (LIM["a"][1] - 15, LIM["b"][1] - 30), f"razón de ejes: {ejes_e[0]:.0f} / {ejes_e[1]:.0f} ≈ {ejes_e[0] / ejes_e[1]:.1f}",
         "black", ha="right")
    capas.corte()
    tg = np.linspace(0, 2 * np.pi, 13)[:-1]
    P = np.array([a, b])[:, None] + VEC @ (ejes_e[:, None] * np.array([np.cos(tg), np.sin(tg)]))
    G = H @ (P - np.array([a, b])[:, None])  # ∇S = H (p − p*): S es cuadrática
    G = G / np.linalg.norm(G, axis=0) * 90
    ax.quiver(*P, *G, color=ROJO, angles="xy", scale_units="xy", scale=1, width=0.006, zorder=6,
              label="∇S (perpendicular)")
    nota(ax, (a, b), "∇S = 0", ROJO, xytext=(-58, 6), textcoords="offset points", fontsize=9)
    capas.corte()
    guardar(fig, "05_curvas_nivel.png", capas, en_guia=0, pasos="curvas")


# ---------------------------------------------------------------- análisis


def fig_residuos():
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.axhline(0, color=ROJO, lw=1.2)
    ax.vlines(xa, 0, e, color=GRIS, lw=0.8)
    ax.scatter(xa, e, color=AZUL, zorder=3)
    for i in np.argsort(-np.abs(e))[:3]:
        ax.annotate(nombres[i], (xa[i], e[i]), textcoords="offset points", xytext=(6, 4), fontsize=7)
    ax.set(xlabel=EJE_X, ylabel="Residuo $e_i$ (km/s)", title="Residuos en función de la distancia")
    ejes(ax, "x", "e")
    guardar(fig, "06_residuos.png")

    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.hist(e, bins=np.arange(-500, 700, 100), color=AZUL, edgecolor="white")
    ax.axvline(0, color=ROJO, lw=1.2)
    ax.set(xlabel="Residuo $e_i$ (km/s)", ylabel="Número de galaxias", title="Histograma de los residuos")
    ejes(ax, "e")
    ax.yaxis.set_major_locator(MultipleLocator(1))
    guardar(fig, "07_histograma_residuos.png")


def fig_residuos_pasos():
    """Residuos e histograma con el mismo eje vertical, y la lectura de los residuos por capas."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.9), sharey=True, gridspec_kw={"width_ratios": [2.3, 1]})
    capas = Capas(fig)
    ax1.axhline(0, color=ROJO, lw=1.2)
    ax1.vlines(xa, 0, e, color=GRIS, lw=0.8)
    ax1.scatter(xa, e, color=AZUL, zorder=3)
    ax1.set(xlabel=EJE_X, ylabel="Residuo $e_i$ (km/s)", title="Residuos en función de la distancia")
    ax2.set(xlabel="Número de galaxias", title="Histograma")
    ejes(ax1, "x", "e")
    ejes(ax2, None, "e")
    ax2.set_xlim(0, 7)
    ax2.xaxis.set_major_locator(MultipleLocator(1))
    capas.corte()
    ax2.hist(e, bins=np.arange(-500, 700, 100), orientation="horizontal", color=AZUL, edgecolor="white")
    ax2.axhline(0, color=ROJO, lw=1.2)
    capas.corte()
    pos, neg = int((e > 0).sum()), int((e < 0).sum())
    nota(ax1, (1.45, 480), f"{pos} positivos", VERDE)
    nota(ax1, (1.45, -470), f"{neg} negativos   ·   media = {abs(e.mean()):.0f}", ROJO)
    capas.corte()
    for x0, x1 in ((0, 0.5), (0.5, 1), (1, 1.5), (1.5, 2.1)):  # promedio por tramos: ni U ni rampa
        m = e[(xa >= x0) & (xa < x1 + 1e-9)].mean()
        ax1.plot([x0, x1], [m, m], color=VERDE, lw=2.4)
    nota(ax1, (1.05, 330), "promedio por tramos ≈ 0", VERDE)
    capas.corte()
    ax1.axhspan(-RMSE, RMSE, color=GRIS, alpha=0.12)
    nota(ax1, (1.12, RMSE + 12), f"±RMSE = ±{RMSE:.0f}", GRIS)
    for n in ("NGC 1068", "NGC 3031", "NGC 4382"):
        i = idx(n)
        ax1.scatter([xa[i]], [e[i]], s=160, facecolors="none", edgecolors=ROJO, lw=1.6, zorder=4)
        nota(ax1, (xa[i], e[i]), f"{n} ({e[i]:+.0f})", ROJO, xytext=(8, -3), textcoords="offset points", fontsize=7)
    capas.corte()
    ax1.axvspan(0.2, 0.3, color=NARANJA, alpha=0.2)
    ax1.axvspan(0, 0.05, color=VERDE, alpha=0.2)
    nota(ax1, (0.21, 540), "todos < 0", NARANJA, fontsize=7)
    nota(ax1, (0.005, 400), "Magallanes", VERDE, fontsize=7, rotation=90)
    capas.corte()
    guardar(fig, None, capas, pasos="residuos")


def fig_calidad():
    """RMSE (residuos a la recta) frente a la variación total (desvíos a la media), mismos ejes."""
    xs, ym = np.array(LIM["x"]), ya.mean()
    SST = ((ya - ym) ** 2).sum()
    for nombre, ref, titulo, c in (
            ("rmse", a * xa + b, f"Residuos a la recta: S = {Smin / 1e6:.2f} ×10⁶", ROJO),
            ("r2", np.full_like(ya, ym), f"Desvíos a la media ȳ = {ym:.0f}: Σ(yᵢ−ȳ)² = {SST / 1e6:.2f} ×10⁶", VERDE)):
        fig, ax = plt.subplots(figsize=(5.2, 3.4))
        ax.vlines(xa, ref, ya, color=c, lw=1.4)
        ax.scatter(xa, ya, color=AZUL, zorder=3)
        if nombre == "rmse":
            ax.fill_between(xs, a * xs + b - RMSE, a * xs + b + RMSE, color=GRIS, alpha=0.15, label=f"±RMSE = ±{RMSE:.0f}")
            ax.plot(xs, a * xs + b, color=ROJO, lw=2, label="Recta ajustada")
        else:
            ax.plot(xs, [ym, ym], color=VERDE, lw=2, label="Modelo sin pendiente y = ȳ")
        ax.set(xlabel=EJE_X, ylabel="Velocidad $y$ (km/s)")
        ax.set_title(titulo, fontsize=9)
        ejes(ax, "x", "y")
        ax.legend(fontsize=7.5, loc="upper left")
        PASOS.mkdir(exist_ok=True)
        fig.tight_layout()
        fig.savefig(PASOS / f"calidad-{nombre}.png")
        plt.close(fig)
    print("   (calidad-rmse, calidad-r2)")


def fig_influencia():
    n = len(x)
    loo = [rg.ajustar(x[:i] + x[i + 1:], y[:i] + y[i + 1:]) for i in range(n)]
    da = np.array([p - a for p, _ in loo])
    k = int(np.argmax(np.abs(da)))
    j = idx("NGC 1068")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4), gridspec_kw={"width_ratios": [1.15, 1]})
    capas = Capas(fig)
    xs = np.array(LIM["x"])
    ax1.scatter(xa, ya, color=AZUL, zorder=3)
    ax1.plot(xs, a * xs + b, color=ROJO, lw=2, label=f"Con los 24 datos: a={a:.1f}, b={b:.1f}")
    ax1.set(xlabel=EJE_X, ylabel=EJE_Y, title="Recta con y sin el dato más influyente")
    ejes(ax1, "x", "y")
    leyenda(ax1, fontsize=7.5, loc="lower right")
    ax2.bar(range(1, n + 1), da, color=AZUL)
    ax2.axhline(0, color="black", lw=0.8)
    ax2.set(xlabel="Galaxia retirada (n.º de fila en la tabla)", ylabel="Cambio en la pendiente Δa (km/s/Mpc)",
            title="Efecto de quitar cada dato")
    ejes(ax2, None, None)
    ax2.yaxis.set_major_locator(MultipleLocator(10))
    ax2.yaxis.set_minor_locator(MultipleLocator(2))
    ax2.set_xticks(range(1, n + 1, 2))
    capas.corte()
    ax1.scatter([xa[k]], [ya[k]], s=130, facecolors="none", edgecolors=ROJO, lw=1.8, zorder=4,
                label=f"Punto retirado: {nombres[k]}")
    ax1.plot(xs, loo[k][0] * xs + loo[k][1], "--", color=VERDE, lw=2,
             label=f"Sin ese punto: a={loo[k][0]:.1f}, b={loo[k][1]:.1f}")
    ax2.bar([k + 1], [da[k]], color=ROJO)
    nota(ax2, (k + 1, da[k]), f"+{da[k]:.1f}", ROJO, xytext=(-30, -4), textcoords="offset points")
    capas.corte()
    ax1.axvline(xa.mean(), color="black", lw=1, ls=":")
    nota(ax1, (xa.mean(), 1110), f" x̄ = {xa.mean():.2f}", "black")
    for x0, x1 in ((0, 0.25), (1.65, 2.1)):
        ax1.axvspan(x0, x1, color=NARANJA, alpha=0.12)
    nota(ax1, (1.7, 1110), "palanca", NARANJA)
    nota(ax1, (0.02, 1110), "palanca", NARANJA)
    capas.corte()
    ax1.scatter([xa[j]], [ya[j]], s=130, facecolors="none", edgecolors=NARANJA, lw=1.8, zorder=4)
    nota(ax1, (xa[j], ya[j]), " NGC 1068", NARANJA, xytext=(6, 2), textcoords="offset points")
    ax2.bar([j + 1], [da[j]], color=NARANJA)
    nota(ax2, (j + 1, da[j]), f"{da[j]:.1f}", NARANJA, xytext=(-8, -12), textcoords="offset points")
    capas.corte()
    guardar(fig, "08_influencia.png", capas, en_guia=1, pasos="influencia")


if __name__ == "__main__":
    SALIDA.mkdir(exist_ok=True)
    print("Figuras generadas en graficos/:")
    fig_dispersion()
    fig_construccion()
    fig_rectas()
    fig_superficie()
    fig_trazas()
    fig_curvas_nivel()
    fig_residuos()
    fig_residuos_pasos()
    fig_calidad()
    fig_influencia()
