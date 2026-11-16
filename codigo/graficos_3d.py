"""Gráficas 3D para la defensa, como cuadros JPG para el paquete animate de LaTeX.

Todo se ve dentro del PDF (en Adobe Acrobat Reader se mueve; en otros lectores, primer cuadro):
  sup-*  superficie: vuelta completa y luego vista desde arriba, plano a–S y plano b–S
  rec-*  una recta que baja por el valle hasta el mínimo (datos a la izquierda, superficie a la derecha)
  trb-*, tra-*  planos b = b₀ y a = a₀ que barren la superficie y cortan sus secciones
  niv-*  la cámara sube hasta ver las curvas de nivel desde arriba
  inf-*  fondo del valle con y sin NGC 4382, girando
Mismos límites y cuadrícula que graficos.py (LIM, CUAD).

Uso:  .venv/bin/python codigo/graficos_3d.py
"""
import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

import regresion as rg
from graficos import AZUL, EJE_X, EJE_Y, LAM, LIM, NARANJA, ROJO, VEC, VERDE, S_malla, a, b, ejes, idx, Smin, x, xa, y, ya

CUADROS = rg.RAIZ / "presentacion" / "animacion"
M = 1e6  # S se muestra en millones

aa = np.linspace(*LIM["a"], 81)
bb = np.linspace(*LIM["b"], 81)
A, B = np.meshgrid(aa, bb)
Z = S_malla(A, B) / M
TOPE = float(np.ceil(Z.max()))


def escena(ax, zlim=None, paso_z=4):
    ax.set(xlabel="a (km/s/Mpc)", ylabel="b (km/s)", zlabel="S(a,b)  (×10⁶)")
    ejes(ax, "a", "b", "S")
    ax.zaxis.set_major_locator(matplotlib.ticker.MultipleLocator(paso_z))
    ax.set_zlim(0, zlim or TOPE)
    ax.computed_zorder = False  # curvas y puntos siempre por encima de la superficie
    ax.set_proj_type("ortho")  # sin perspectiva: las vistas de frente y desde arriba salen planas


def limpiar(prefijo):
    CUADROS.mkdir(parents=True, exist_ok=True)
    for f in CUADROS.glob(f"{prefijo}-*.jpg"):
        f.unlink()


def grabar(fig, prefijo, i):
    fig.savefig(CUADROS / f"{prefijo}-{i}.jpg", dpi=110, pil_kwargs={"quality": 85})


def recorrido_camara(paradas, n=12, quieto=8):
    """Interpola (elev, azim, título) entre paradas; en cada parada la cámara se queda quieta."""
    out = []
    for (e0, z0, _), (e1, z1, t1) in zip(paradas, paradas[1:]):
        s = (1 - np.cos(np.linspace(0, np.pi, n))) / 2  # arranca y frena suave
        out += [(e0 + (e1 - e0) * u, z0 + (z1 - z0) * u, "") for u in s[1:]]
        out += [(e1, z1, t1)] * quieto
    return out


def cuadros_giro():
    """Vuelta completa a la superficie y luego tres vistas: desde arriba, plano a–S y plano b–S."""
    limpiar("sup")
    fig = plt.figure(figsize=(6.4, 4.6))
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(A, B, Z, cmap="viridis", alpha=0.85, linewidth=0)
    ax.contour(A, B, Z, 12, zdir="z", offset=0, cmap="viridis", linewidths=0.7)
    ax.scatter([a], [b], [Smin / M], color=ROJO, s=50, depthshade=False)
    ax.plot([a, a], [b, b], [0, Smin / M], color=ROJO, lw=1)
    escena(ax)
    titulo = ax.set_title(" ", fontsize=11, fontweight="bold")
    fig.tight_layout()
    vistas = [(28, -58 + i * 10, "") for i in range(36)]
    vistas += recorrido_camara([(28, 302, ""), (89, 270, "Desde arriba: curvas de nivel"),
                                (0, 270, "Plano a–S: parábolas en a"), (0, 360, "Plano b–S: parábolas en b"),
                                (28, 302, "")])
    for i, (el, az, t) in enumerate(vistas):
        ax.view_init(elev=el, azim=az)
        titulo.set_text(t or " ")
        grabar(fig, "sup", i)
    plt.close(fig)
    print(f"   {len(vistas)} cuadros sup-*.jpg")


def recorrido(p0=(820.0, 20.0), n=40):
    """Camino de máximo descenso p' = −∇S = −H(p − p*): baja rápido al valle y luego lo recorre.
    Como S es cuadrática, la solución es exacta: p(t) = p* + V e^(−Λt) Vᵀ (p0 − p*)."""
    t = np.linspace(0, 0.7, 2000)
    d = VEC.T @ (np.array(p0) - [a, b])
    P = np.array([a, b])[:, None] + VEC @ (d[:, None] * np.exp(-LAM[:, None] * t))
    s = np.r_[0, np.cumsum(np.hypot(*np.diff(P)))]  # remuestreo por longitud de arco: velocidad pareja
    k = np.searchsorted(s, np.linspace(0, s[-1], n))
    return np.vstack([P[:, k].T, [[a, b]] * 6])  # el final se queda quieto unos cuadros


def S_de(p, q):
    return float(((ya - p * xa - q) ** 2).sum())


def cuadros_recorrido():
    """Animación para la diapositiva: la recta (izquierda) y su punto en la superficie (derecha)."""
    limpiar("rec")
    camino = recorrido()
    xs = np.array(LIM["x"])
    fig = plt.figure(figsize=(10, 4.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.2])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], projection="3d")
    ax1.scatter(xa, ya, color=AZUL, zorder=3, s=22)
    ax1.set(xlabel=EJE_X, ylabel=EJE_Y)
    ejes(ax1, "x", "y")
    seg = LineCollection([], colors=ROJO, linewidths=1)
    ax1.add_collection(seg)
    (recta,) = ax1.plot([], [], color="#E0703A", lw=2.4)
    titulo = ax1.set_title("y = 000x +000     S = 0.00 ×10⁶", fontsize=11)
    ax2.plot_surface(A, B, Z, cmap="viridis", alpha=0.55, linewidth=0)
    ax2.contour(A, B, Z, 12, zdir="z", offset=0, cmap="viridis", linewidths=0.6)
    ax2.set(xlabel="a", ylabel="b", zlabel="S (×10⁶)")
    ejes(ax2, "a", "b", "S")
    ax2.zaxis.set_major_locator(matplotlib.ticker.MultipleLocator(4))
    ax2.computed_zorder = False  # el camino siempre por encima de la superficie
    ax2.set_zlim(0, TOPE)
    ax2.view_init(elev=34, azim=-50)
    (rastro,) = ax2.plot([], [], [], color="white", lw=2.2, zorder=10)
    (piso,) = ax2.plot([], [], [], color="#E0703A", lw=1.2, ls="--", zorder=10)
    (punto,) = ax2.plot([], [], [], "o", color="#E0703A", mec="black", ms=8, zorder=11)
    fig.tight_layout()
    for i, (p, q) in enumerate(camino):
        seg.set_segments([[(xi, yi), (xi, p * xi + q)] for xi, yi in zip(xa, ya)])
        recta.set_data(xs, p * xs + q)
        S = S_de(p, q)
        titulo.set_text(f"y = {p:.0f}x {q:+.0f}     S = {S / M:.2f} ×10⁶")
        h = camino[:i + 1]
        z = [S_de(*c) / M for c in h]
        rastro.set_data_3d(h[:, 0], h[:, 1], z)
        piso.set_data_3d(h[:, 0], h[:, 1], np.zeros(len(h)))
        punto.set_data_3d([p], [q], [S / M])
        grabar(fig, "rec", i)
    plt.close(fig)
    print(f"   {len(camino)} cuadros rec-*.jpg en presentacion/animacion/")


def barrido(lo, hi, n=40):
    """Ida y vuelta suave entre lo y hi."""
    return lo + (hi - lo) * (1 - np.cos(np.linspace(0, 2 * np.pi, n, endpoint=False))) / 2


def cuadros_trazas():
    """Un plano vertical recorre la superficie; su corte es una parábola que se desplaza."""
    for prefijo, fijo in (("trb", "b"), ("tra", "a")):
        limpiar(prefijo)
        fig = plt.figure(figsize=(5.6, 4.6))
        ax = fig.add_subplot(projection="3d")
        ax.plot_surface(A, B, Z, cmap="viridis", alpha=0.45, linewidth=0)
        ax.scatter([a], [b], [Smin / M], color=ROJO, s=40, depthshade=False, zorder=12)
        escena(ax)
        ax.view_init(elev=22, azim=-62 if fijo == "b" else -28)
        titulo = ax.set_title(" ", fontsize=11, fontweight="bold")
        fig.tight_layout()
        c = NARANJA if fijo == "b" else AZUL
        valores = barrido(b - 300, b + 300) if fijo == "b" else barrido(a - 300, a + 300)
        dibujos = []
        for i, v in enumerate(valores):
            for d in dibujos:
                d.remove()
            if fijo == "b":
                u = aa
                curva = S_malla(aa, np.full_like(aa, v)).ravel() / M
                lin = (u, np.full_like(u, v))
                p_opt = ((xa @ ya - v * xa.sum()) / (xa @ xa), v)
                titulo.set_text(f"Plano b = {v:.0f}:  S(a, {v:.0f})")
            else:
                u = bb
                curva = S_malla(np.full_like(bb, v), bb).ravel() / M
                lin = (np.full_like(u, v), u)
                p_opt = (v, (ya.sum() - v * xa.sum()) / len(xa))
                titulo.set_text(f"Plano a = {v:.0f}:  S({v:.0f}, b)")
            U, alto = np.meshgrid(u, [0.0, TOPE])
            P, Q = (U, np.full_like(U, v)) if fijo == "b" else (np.full_like(U, v), U)
            dibujos = [
                ax.plot_surface(P, Q, alto, color=c, alpha=0.18, linewidth=0, zorder=5),
                ax.plot(*lin, np.minimum(curva, TOPE), color=c, lw=3, zorder=10)[0],
                ax.plot(*lin, np.zeros_like(u), color=c, lw=1, ls="--", zorder=10)[0],
                ax.scatter([p_opt[0]], [p_opt[1]], [rg.error_cuadratico(*p_opt, x, y) / M], color="black",
                           s=25, depthshade=False, zorder=13),
            ]
            grabar(fig, prefijo, i)
        plt.close(fig)
    print(f"   {len(valores)} cuadros trb-*.jpg y tra-*.jpg")


def cuadros_niveles():
    """Curvas de nivel dibujadas sobre la superficie y proyectadas al piso; la cámara sube a vista cenital."""
    limpiar("niv")
    niveles = Smin / M + np.array([0.25, 0.5, 1, 1.75, 2.75, 4, 6, 8.5])
    fig = plt.figure(figsize=(6.4, 4.6))
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(A, B, Z, cmap="viridis", alpha=0.35, linewidth=0)
    ax.contour(A, B, Z, levels=niveles, cmap="viridis", linewidths=2)
    ax.contour(A, B, Z, levels=niveles, zdir="z", offset=0, cmap="viridis", linewidths=1.2)
    ax.scatter([a], [b], [0], color=ROJO, s=40, depthshade=False, zorder=12)
    ax.plot([a, a], [b, b], [0, Smin / M], color=ROJO, lw=1.2, zorder=12)
    escena(ax)
    titulo = ax.set_title(" ", fontsize=11, fontweight="bold")
    fig.tight_layout()
    vistas = [(25, -58, "Cada curva: rectas con el mismo S")] * 8
    vistas += recorrido_camara([(25, -58, ""), (89, -90, "Vista desde arriba: elipses alrededor de (a*, b*)")],
                               n=26, quieto=14)
    vistas += recorrido_camara([(89, -90, ""), (25, -58, "")], n=16, quieto=2)
    for i, (el, az, t) in enumerate(vistas):
        ax.view_init(elev=el, azim=az)
        titulo.set_text(t or " ")
        grabar(fig, "niv", i)
    plt.close(fig)
    print(f"   {len(vistas)} cuadros niv-*.jpg")


def cuadros_influencia():
    """Fondo del valle con los 24 datos (azul) y sin NGC 4382 (naranja), girando."""
    limpiar("inf")
    k = idx("NGC 4382")
    Zk = Z - (ya[k] - A * xa[k] - B) ** 2 / M
    a2, b2 = rg.ajustar(x[:k] + x[k + 1:], y[:k] + y[k + 1:])
    S2 = rg.error_cuadratico(a2, b2, x[:k] + x[k + 1:], y[:k] + y[k + 1:]) / M
    tope = 3.5  # solo el fondo: más arriba los dos valles casi coinciden
    niveles = np.arange(1.25, tope, 0.5)
    fig = plt.figure(figsize=(6.4, 4.6))
    ax = fig.add_subplot(projection="3d")
    for zz, c in ((Z, AZUL), (Zk, NARANJA)):  # anillos a su altura (la forma del valle) y su sombra en el piso
        ax.contour(A, B, zz, levels=niveles, colors=c, linewidths=1.8)
        ax.contour(A, B, zz, levels=niveles, zdir="z", offset=0, colors=c, linewidths=0.7, alpha=0.6)
    for (p, q, s_), c, t in (((a, b, Smin / M), AZUL, "con los 24"), ((a2, b2, S2), NARANJA, "sin NGC 4382")):
        ax.scatter([p], [q], [s_], color=c, edgecolor="black", s=60, depthshade=False, zorder=12)
        ax.plot([p, p], [q, q], [0, s_], color=c, lw=1.2, zorder=12)
        ax.scatter([p], [q], [0], color=c, edgecolor="black", s=30, depthshade=False, zorder=12, label=f"Mínimo {t}: ({p:.0f}, {q:.0f})")
    ax.plot([a, a2], [b, b2], [0, 0], color="black", lw=2, zorder=12)
    escena(ax, zlim=tope, paso_z=0.5)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    for i in range(36):
        ax.view_init(elev=30, azim=-58 + i * 10)
        grabar(fig, "inf", i)
    plt.close(fig)
    print("   36 cuadros inf-*.jpg")


if __name__ == "__main__":
    print("Gráficas 3D (cuadros para animate):")
    cuadros_giro()
    cuadros_recorrido()
    cuadros_trazas()
    cuadros_niveles()
    cuadros_influencia()
