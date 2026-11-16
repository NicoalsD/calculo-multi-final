"""Gráficas 3D para la defensa.

1. presentacion/interactivo/*.html: superficie, trazas, curvas de nivel, recorrido hacia el
   mínimo e influencia de NGC 4382, que se giran con el mouse (Plotly; plotly.min.js queda al
   lado, así que funcionan sin internet).
2. presentacion/animacion/sup-*.jpg y rec-*.jpg: cuadros para el paquete animate de LaTeX
   (superficie girando y una recta que baja por el valle hasta el mínimo).
Mismos límites y cuadrícula que graficos.py (LIM, CUAD).

Uso:  .venv/bin/python codigo/graficos_3d.py
"""
import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import regresion as rg
from matplotlib.collections import LineCollection

from graficos import (AZUL, CUAD, EJE_X, EJE_Y, LAM, LIM, ROJO, VEC, VERDE, S_malla, a, b, ejes, idx, nombres,
                      Smin, x, xa, y, ya)

PRES = rg.RAIZ / "presentacion"
HTML, CUADROS = PRES / "interactivo", PRES / "animacion"
N_CUADROS = 36
M = 1e6  # S se muestra en millones

aa = np.linspace(*LIM["a"], 81)
bb = np.linspace(*LIM["b"], 81)
A, B = np.meshgrid(aa, bb)
Z = S_malla(A, B) / M
TOPE = float(np.ceil(Z.max()))
ESCENA = dict(xaxis=dict(title="a (km/s/Mpc)", range=LIM["a"], dtick=CUAD["a"][0]),
              yaxis=dict(title="b (km/s)", range=LIM["b"], dtick=CUAD["b"][0]),
              zaxis=dict(title="S(a,b) ×10⁶", range=[0, TOPE], dtick=2 * CUAD["S"][0]),
              aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.7),
              camera=dict(eye=dict(x=-1.4, y=-1.4, z=1.3)))
HOVER = "a = %{x:.1f}<br>b = %{y:.1f}<br>S = %{z:.3f} ×10⁶<extra></extra>"


def superficie(**kw):
    return go.Surface(x=aa, y=bb, z=Z, cmin=0, cmax=TOPE, colorscale="Viridis", hovertemplate=HOVER,
                      colorbar=dict(title="S ×10⁶", len=0.6), **kw)


def minimo():
    return go.Scatter3d(x=[a], y=[b], z=[Smin / M], mode="markers+text", marker=dict(size=6, color=ROJO),
                        text=[f"(a*, b*) = ({a:.1f}, {b:.1f})"], textposition="top center",
                        hovertemplate=HOVER, name="Mínimo")


def guardar(fig, nombre, titulo):
    fig.update_layout(title=titulo, template="plotly_white", margin=dict(l=0, r=0, t=110, b=0))
    fig.write_html(HTML / nombre, include_plotlyjs="directory", full_html=True)
    print("  ", nombre)


def html_superficie():
    plano = go.Surface(x=LIM["a"], y=LIM["b"], z=[[Smin / M] * 2] * 2, opacity=0.45, showscale=False,
                       colorscale=[[0, ROJO], [1, ROJO]], hoverinfo="skip", showlegend=True, visible="legendonly",
                       name="Plano tangente en el mínimo (∇S = 0, horizontal)")
    fig = go.Figure([superficie(contours_z=dict(show=True, usecolormap=True, project_z=True)), minimo(), plano])
    vistas = {"3D": dict(x=-1.4, y=-1.4, z=1.3), "Desde arriba (curvas de nivel)": dict(x=0, y=0, z=2.4),
              "Plano a–S (b fijo)": dict(x=0, y=-2.4, z=0.2), "Plano b–S (a fijo)": dict(x=2.4, y=0, z=0.2)}
    fig.update_layout(scene=ESCENA, updatemenus=[dict(type="buttons", direction="right", x=0, y=1.0, yanchor="bottom",
        buttons=[dict(label=k, method="relayout", args=[{"scene.camera.eye": v}]) for k, v in vistas.items()])])
    guardar(fig, "superficie.html", "Superficie de error z = S(a, b): arrastra para girar, rueda para acercar")


def html_trazas():
    """Superficie cortada por un plano b = b0 y otro a = a0; los deslizadores mueven cada plano."""
    # Listas simples (no arrays de numpy): el restyle de los deslizadores no decodifica arrays binarios.
    # La curva se levanta 0.1 ×10⁶ para que la superficie opaca no la tape.
    def plano_b(q):  # plano vertical b = q y su curva S(a, q)
        u, w = aa.tolist(), [float(q)] * len(aa)
        return dict(x=[u, u], y=[w, w], z=[[0.0] * len(u), [TOPE] * len(u)]), \
               dict(x=u, y=w, z=(S_malla(aa, np.full_like(aa, q)).ravel() / M + 0.1).tolist())
    def plano_a(p):  # plano vertical a = p y su curva S(p, b)
        u, w = [float(p)] * len(bb), bb.tolist()
        return dict(x=[u, u], y=[w, w], z=[[0.0] * len(w), [TOPE] * len(w)]), \
               dict(x=u, y=w, z=(S_malla(np.full_like(bb, p), bb).ravel() / M + 0.1).tolist())
    pb, cb = plano_b(b)
    pa, ca = plano_a(a)
    plano = dict(showscale=False, opacity=0.3, hoverinfo="skip")
    fig = go.Figure([
        superficie(showscale=False),
        go.Surface(**pb, colorscale=[[0, "#E0703A"], [1, "#E0703A"]], **plano),
        go.Scatter3d(**cb, mode="lines", line=dict(color="#C4561F", width=10), name="Sección b = b₀", hovertemplate=HOVER),
        go.Surface(**pa, colorscale=[[0, "#3E6FB0"], [1, "#3E6FB0"]], **plano),
        go.Scatter3d(**ca, mode="lines", line=dict(color="#1F4E79", width=10), name="Sección a = a₀", hovertemplate=HOVER),
        minimo(),
    ])
    def pasos(valores, f, trazas):
        out = []
        for v in valores:
            p, c = f(v)
            out.append(dict(method="restyle", label=f"{v:.0f}", args=[
                {k: [p[k], c[k]] for k in "xyz"}, trazas]))
        return out
    vb = np.round(np.linspace(b - 300, b + 300, 13))
    va = np.round(np.linspace(a - 300, a + 300, 13))
    fig.update_layout(scene=ESCENA, legend=dict(x=0.75, y=0.95), sliders=[
        dict(active=6, currentvalue=dict(prefix="Plano naranja: b₀ = "), pad=dict(t=10), y=0.02, len=0.45, x=0.02,
             steps=pasos(vb, plano_b, [1, 2])),
        dict(active=6, currentvalue=dict(prefix="Plano azul: a₀ = "), pad=dict(t=10), y=0.02, len=0.45, x=0.53,
             steps=pasos(va, plano_a, [3, 4])),
    ])
    guardar(fig, "trazas.html", "Trazas y secciones: mueve los planos y mira la parábola que cortan")


def html_curvas():
    niveles = dict(start=1.25, end=TOPE, size=0.75)
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "scene"}, {"type": "xy"}]], column_widths=[0.55, 0.45],
                        subplot_titles=("Curvas de nivel sobre la superficie", "Mapa de curvas de nivel"))
    fig.add_trace(superficie(showscale=False, opacity=0.9,
                             contours_z=dict(show=True, color="white", width=2, **niveles)), 1, 1)
    fig.add_trace(minimo(), 1, 1)
    fig.add_trace(go.Contour(x=aa, y=bb, z=Z, colorscale="Viridis", contours=dict(coloring="lines", showlabels=True, **niveles),
                             line=dict(width=2), hovertemplate=HOVER, colorbar=dict(title="S ×10⁶")), 1, 2)
    fig.add_trace(go.Scatter(x=[a], y=[b], mode="markers", marker=dict(size=11, color=ROJO), name="(a*, b*)",
                             hovertemplate="a* = %{x:.2f}<br>b* = %{y:.2f}<extra></extra>"), 1, 2)
    fig.update_layout(scene=ESCENA, showlegend=False,
                      xaxis=dict(title="a (km/s/Mpc)", range=LIM["a"], dtick=CUAD["a"][0], minor=dict(dtick=CUAD["a"][1], showgrid=True)),
                      yaxis=dict(title="b (km/s)", range=LIM["b"], dtick=CUAD["b"][0], minor=dict(dtick=CUAD["b"][1], showgrid=True),
                                 scaleanchor="x"))
    guardar(fig, "curvas_nivel.html", "Curvas de nivel de S(a, b): elipses centradas en (a*, b*)")


def cuadros_giro():
    """Superficie de graficos.fig_superficie vista desde N_CUADROS ángulos (una vuelta completa)."""
    for f in CUADROS.glob("sup-*.jpg"):
        f.unlink()
    fig = plt.figure(figsize=(6.4, 4.6))
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(A, B, Z, cmap="viridis", alpha=0.85, linewidth=0)
    ax.contour(A, B, Z, 12, zdir="z", offset=0, cmap="viridis", linewidths=0.7)
    ax.scatter([a], [b], [Smin / M], color=ROJO, s=50, depthshade=False)
    ax.plot([a, a], [b, b], [0, Smin / M], color=ROJO, lw=1)
    ax.set(xlabel="a (km/s/Mpc)", ylabel="b (km/s)", zlabel="S(a,b)  (×10⁶)")
    ejes(ax, "a", "b", "S")
    ax.zaxis.set_major_locator(matplotlib.ticker.MultipleLocator(4))
    ax.set_zlim(0, TOPE)
    fig.tight_layout()
    for i in range(N_CUADROS):
        ax.view_init(elev=28, azim=-58 + i * 360 / N_CUADROS)
        fig.savefig(CUADROS / f"sup-{i}.jpg", dpi=110, pil_kwargs={"quality": 85})
    plt.close(fig)
    print(f"   {N_CUADROS} cuadros en presentacion/animacion/")


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


def residuos(p, q):
    """Segmentos verticales de cada dato a la recta, como una sola traza (None separa)."""
    u, w = [], []
    for xi, yi in zip(xa, ya):
        u += [xi, xi, None]
        w += [yi, p * xi + q, None]
    return u, w


def html_recorrido():
    camino = recorrido()
    xs = list(LIM["x"])
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "xy"}, {"type": "scene"}]], column_widths=[0.45, 0.55],
                        subplot_titles=("La recta en los datos", "Su punto (a, b) en la superficie S"))
    p, q = camino[0]
    fig.add_trace(go.Scatter(x=xa, y=ya, mode="markers", marker=dict(color=AZUL, size=8), name="Datos", text=nombres,
                             hovertemplate="%{text}<br>x = %{x} Mpc<br>y = %{y} km/s<extra></extra>"), 1, 1)
    u, w = residuos(p, q)
    fig.add_trace(go.Scatter(x=u, y=w, mode="lines", line=dict(color=ROJO, width=1.5), name="Residuos", hoverinfo="skip"), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=[p * v + q for v in xs], mode="lines", line=dict(color="#E0703A", width=4), name="Recta"), 1, 1)
    fig.add_trace(superficie(showscale=False, opacity=0.85), 1, 2)
    fig.add_trace(go.Scatter3d(x=[p], y=[q], z=[S_de(p, q) / M], mode="lines", line=dict(color="white", width=6),
                               name="Camino", hoverinfo="skip"), 1, 2)
    fig.add_trace(go.Scatter3d(x=[p], y=[q], z=[S_de(p, q) / M], mode="markers", marker=dict(size=7, color="#E0703A"),
                               name="(a, b) actual", hovertemplate=HOVER), 1, 2)
    cuadros = []
    for i, (p, q) in enumerate(camino):
        u, w = residuos(p, q)
        hecho = camino[:i + 1]
        z = [S_de(*c) / M + 0.05 for c in hecho]
        cuadros.append(go.Frame(name=str(i), traces=[1, 2, 4, 5], data=[
            go.Scatter(x=u, y=w), go.Scatter(x=xs, y=[p * v + q for v in xs]),
            go.Scatter3d(x=hecho[:, 0].tolist(), y=hecho[:, 1].tolist(), z=z),
            go.Scatter3d(x=[p], y=[q], z=[z[-1]])],
            layout=dict(title_text=f"Recta y = {p:.1f}·x + ({q:.1f})   →   S = {S_de(p, q) / M:.3f} ×10⁶")))
    fig.frames = cuadros
    anim = dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))
    fig.update_layout(
        scene=ESCENA, showlegend=False,
        xaxis=dict(title=EJE_X.replace("$", ""), range=LIM["x"], dtick=CUAD["x"][0], minor=dict(dtick=CUAD["x"][1], showgrid=True)),
        yaxis=dict(title=EJE_Y.replace("$", ""), range=LIM["y"], dtick=CUAD["y"][0], minor=dict(dtick=CUAD["y"][1], showgrid=True)),
        updatemenus=[dict(type="buttons", x=0, y=-0.08, xanchor="left", direction="right", buttons=[
            dict(label="▶ Bajar por el valle", method="animate",
                 args=[None, dict(frame=dict(duration=110, redraw=True), fromcurrent=True, transition=dict(duration=0))]),
            dict(label="❚❚ Pausa", method="animate", args=[[None], anim])])],
        sliders=[dict(active=0, x=0.25, len=0.75, y=-0.05, currentvalue=dict(prefix="Paso "),
                      steps=[dict(label=str(i), method="animate", args=[[str(i)], anim]) for i in range(len(camino))])])
    guardar(fig, "recorrido.html", f"Recta y = {camino[0][0]:.1f}·x + ({camino[0][1]:.1f})   →   S = {S_de(*camino[0]) / M:.3f} ×10⁶")


def html_influencia():
    """S con los 24 datos y S sin NGC 4382: quitar un dato desplaza todo el valle."""
    k = idx("NGC 4382")
    A, B = np.meshgrid(aa, bb)
    Zk = (S_malla(A, B) - (ya[k] - A * xa[k] - B) ** 2) / M
    tope = 3.5  # solo el fondo del valle: más arriba las dos superficies casi coinciden
    corta = lambda z: np.where(z <= tope, z, np.nan)
    piso = lambda c: dict(show=True, color=c, start=1.25, end=tope, size=0.5, project_z=True)
    a2, b2 = rg.ajustar(x[:k] + x[k + 1:], y[:k] + y[k + 1:])
    S2 = rg.error_cuadratico(a2, b2, x[:k] + x[k + 1:], y[:k] + y[k + 1:]) / M
    fig = go.Figure([
        go.Surface(x=aa, y=bb, z=corta(Z), colorscale=[[0, "#1F4E79"], [1, "#9ec5e8"]], showscale=False, opacity=0.7,
                   contours_z=piso("#1F4E79"), hovertemplate=HOVER, name="Con los 24 datos"),
        go.Surface(x=aa, y=bb, z=corta(Zk), colorscale=[[0, "#C4561F"], [1, "#f3c3a5"]], showscale=False, opacity=0.7,
                   contours_z=piso("#C4561F"), hovertemplate=HOVER, name="Sin NGC 4382"),
        minimo(),
        go.Scatter3d(x=[a2], y=[b2], z=[S2], mode="markers+text", marker=dict(size=6, color=VERDE),
                     text=[f"sin NGC 4382: ({a2:.1f}, {b2:.1f})"], textposition="bottom center", hovertemplate=HOVER,
                     name="Mínimo sin NGC 4382"),
        go.Scatter3d(x=[a, a2], y=[b, b2], z=[0, 0], mode="lines+markers", line=dict(color="black", width=5),
                     marker=dict(size=3), name="Desplazamiento en el piso", hoverinfo="skip"),
    ])
    vis = {"Las dos": [True] * 5, "Con los 24": [True, False, True, False, True],
           "Sin NGC 4382": [False, True, False, True, True]}
    escena = {**ESCENA, "zaxis": {**ESCENA["zaxis"], "range": [0, tope], "dtick": 0.5},
              "aspectratio": dict(x=1, y=1, z=0.5)}
    fig.update_layout(scene=escena, legend=dict(x=0.75, y=0.95), updatemenus=[dict(
        type="buttons", direction="right", x=0, y=1.0, yanchor="bottom",
        buttons=[dict(label=k, method="restyle", args=[{"visible": v}]) for k, v in vis.items()])])
    guardar(fig, "influencia.html", f"Quitar NGC 4382 mueve el fondo del valle: a* {a:.1f} → {a2:.1f}, b* {b:.1f} → {b2:.1f}")


def cuadros_recorrido():
    """Animación para la diapositiva: la recta (izquierda) y su punto en la superficie (derecha)."""
    for f in CUADROS.glob("rec-*.jpg"):
        f.unlink()
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
    A, B = np.meshgrid(aa, bb)
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
        fig.savefig(CUADROS / f"rec-{i}.jpg", dpi=110, pil_kwargs={"quality": 85})
    plt.close(fig)
    print(f"   {len(camino)} cuadros rec-*.jpg en presentacion/animacion/")


if __name__ == "__main__":
    HTML.mkdir(parents=True, exist_ok=True)
    CUADROS.mkdir(parents=True, exist_ok=True)
    print("Gráficas 3D:")
    html_superficie()
    html_trazas()
    html_curvas()
    html_recorrido()
    html_influencia()
    cuadros_giro()
    cuadros_recorrido()
