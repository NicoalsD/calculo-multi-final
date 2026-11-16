"""Gráficas 3D para la defensa.

1. presentacion/interactivo/*.html: superficie, trazas y curvas de nivel que se giran con el
   mouse (Plotly; plotly.min.js queda al lado, así que funcionan sin internet).
2. presentacion/animacion/sup-*.jpg: cuadros de la superficie girando, para el paquete
   animate de LaTeX (diapositiva de la superficie).

Uso:  .venv/bin/python codigo/graficos_3d.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import regresion as rg
from graficos import S_malla, a, b, Smin, x, y, ROJO

PRES = rg.RAIZ / "presentacion"
HTML, CUADROS = PRES / "interactivo", PRES / "animacion"
N_CUADROS = 36
M = 1e6  # S se muestra en millones

aa = np.linspace(a - 350, a + 350, 80)  # dominio más estrecho que en los PNG: así se ve el tazón
bb = np.linspace(b - 350, b + 350, 80)
A, B = np.meshgrid(aa, bb)
Z = S_malla(A, B) / M
TOPE = float(np.ceil(Z.max()))
ESCENA = dict(xaxis_title="a (km/s/Mpc)", yaxis_title="b (km/s)", zaxis=dict(title="S(a,b) ×10⁶", range=[0, TOPE]),
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
    fig = go.Figure([superficie(contours_z=dict(show=True, usecolormap=True, project_z=True)), minimo()])
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
    fig.update_layout(scene=ESCENA, xaxis_title="a (km/s/Mpc)", yaxis_title="b (km/s)", showlegend=False)
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
    ax.set_zlim(0)
    fig.tight_layout()
    for i in range(N_CUADROS):
        ax.view_init(elev=28, azim=-58 + i * 360 / N_CUADROS)
        fig.savefig(CUADROS / f"sup-{i}.jpg", dpi=110, pil_kwargs={"quality": 85})
    plt.close(fig)
    print(f"   {N_CUADROS} cuadros en presentacion/animacion/")


if __name__ == "__main__":
    HTML.mkdir(parents=True, exist_ok=True)
    CUADROS.mkdir(parents=True, exist_ok=True)
    print("Gráficas 3D:")
    html_superficie()
    html_trazas()
    html_curvas()
    cuadros_giro()
