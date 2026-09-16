"""Gráficas Plotly para Michaelis-Menten y Lineweaver-Burk."""
from __future__ import annotations
import numpy as np
import plotly.graph_objects as go
from models.kinetics import evaluate_condition, mechanism_velocity

CONTROL_COLOR = "#1f77b4"
INHIBITED_COLOR = "#c63d3d"
COMPARE_COLORS = {
    "Sin inhibidor": "#1f77b4",
    "Competitiva": "#c63d3d",
    "Acompetitiva": "#2f8f46",
    "Mixta": "#7a4fa3",
    "No competitiva pura": "#d28f22",
}


def _curve(mechanism, S_grid, Vmax, Km, I, Kic, Kiu, Ki):
    return mechanism_velocity(mechanism, S_grid, Vmax, Km, I=I, Kic=Kic, Kiu=Kiu, Ki=Ki)


def michaelis_plot(result, show_references: bool = True, s_max: float = 20.0) -> go.Figure:
    S_grid = np.linspace(0.01, max(20.0, s_max), 400)
    v_control = mechanism_velocity("Sin inhibidor", S_grid, result.Vmax, result.Km)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=S_grid, y=v_control, mode="lines", name="Control",
        line=dict(color=CONTROL_COLOR, width=3),
        hovertemplate="[S]=%{x:.2f} mM<br>v=%{y:.2f} unidades/min<br>Control<extra></extra>",
    ))
    v_control_current = mechanism_velocity("Sin inhibidor", result.S, result.Vmax, result.Km)
    fig.add_trace(go.Scatter(
        x=[result.S], y=[v_control_current], mode="markers", name="Punto control",
        marker=dict(color=CONTROL_COLOR, size=10, symbol="circle-open", line=dict(width=2)),
        hovertemplate="[S]=%{x:.2f} mM<br>v=%{y:.2f} unidades/min<br>Control actual<extra></extra>",
    ))

    if result.mechanism != "Sin inhibidor":
        v_inh = _curve(result.mechanism, S_grid, result.Vmax, result.Km, result.I, result.Kic, result.Kiu, result.Ki)
        fig.add_trace(go.Scatter(
            x=S_grid, y=v_inh, mode="lines", name=result.mechanism,
            line=dict(color=INHIBITED_COLOR, width=3),
            hovertemplate=f"[S]=%{{x:.2f}} mM<br>v=%{{y:.2f}} unidades/min<br>{result.mechanism}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=[result.S], y=[result.velocity], mode="markers", name="Punto actual",
            marker=dict(color=INHIBITED_COLOR, size=11),
            hovertemplate=f"[S]=%{{x:.2f}} mM<br>v=%{{y:.2f}} unidades/min<br>{result.mechanism} actual<extra></extra>",
        ))

    if show_references:
        fig.add_hline(y=result.Vmax, line_dash="dot", line_width=1, annotation_text="Vmax", annotation_position="top right")
        fig.add_hline(y=result.Vmax / 2, line_dash="dot", line_width=1, annotation_text="Vmax/2", annotation_position="bottom right")
        fig.add_vline(x=result.Km, line_dash="dot", line_width=1, annotation_text="Km", annotation_position="top")
        if result.mechanism != "Sin inhibidor":
            fig.add_hline(y=result.Vmax_app, line_dash="dash", line_width=1, annotation_text="Vmax app", annotation_position="top left")
            fig.add_hline(y=result.Vmax_app / 2, line_dash="dash", line_width=1, annotation_text="Vmax app/2", annotation_position="bottom left")
            fig.add_vline(x=result.Km_app, line_dash="dash", line_width=1, annotation_text="Km app", annotation_position="bottom")

    fig.update_layout(
        title="Cinética de Michaelis-Menten",
        xaxis_title="Concentración de sustrato [S] (mM)",
        yaxis_title="Velocidad inicial v₀ (unidades/min)",
        template="plotly_white", hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=20, r=20, t=70, b=20),
    )
    fig.update_xaxes(range=[0, max(20.0, s_max)])
    fig.update_yaxes(rangemode="tozero")
    return fig


def comparison_plot(mechanisms, Vmax, Km, I, Kic, Kiu, Ki, s_max: float = 20.0) -> go.Figure:
    S_grid = np.linspace(0.01, max(20.0, s_max), 400)
    fig = go.Figure()
    for mechanism in mechanisms:
        y = _curve(mechanism, S_grid, Vmax, Km, I if mechanism != "Sin inhibidor" else 0.0, Kic, Kiu, Ki)
        fig.add_trace(go.Scatter(
            x=S_grid, y=y, mode="lines", name=mechanism,
            line=dict(width=3, color=COMPARE_COLORS.get(mechanism)),
            hovertemplate=f"[S]=%{{x:.2f}} mM<br>v=%{{y:.2f}} unidades/min<br>{mechanism}<extra></extra>",
        ))
    fig.update_layout(
        title="Comparación de mecanismos",
        xaxis_title="Concentración de sustrato [S] (mM)",
        yaxis_title="Velocidad inicial v₀ (unidades/min)",
        template="plotly_white", hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=20, r=20, t=70, b=20),
    )
    fig.update_yaxes(rangemode="tozero")
    return fig


def lineweaver_burk_plot(result, s_min: float = 0.1, s_max: float = 20.0) -> go.Figure:
    S_grid = np.linspace(max(s_min, 1e-6), max(s_max, s_min + 0.1), 300)
    x = 1.0 / S_grid
    y_control = 1.0 / mechanism_velocity("Sin inhibidor", S_grid, result.Vmax, result.Km)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y_control, mode="lines", name="Control",
        line=dict(color=CONTROL_COLOR, width=3),
        hovertemplate="1/[S]=%{x:.3f} mM⁻¹<br>1/v=%{y:.4f} min/unidad<extra></extra>",
    ))
    if result.mechanism != "Sin inhibidor":
        y_inh = 1.0 / _curve(result.mechanism, S_grid, result.Vmax, result.Km, result.I, result.Kic, result.Kiu, result.Ki)
        fig.add_trace(go.Scatter(
            x=x, y=y_inh, mode="lines", name=result.mechanism,
            line=dict(color=INHIBITED_COLOR, width=3),
            hovertemplate="1/[S]=%{x:.3f} mM⁻¹<br>1/v=%{y:.4f} min/unidad<extra></extra>",
        ))
    fig.update_layout(
        title="Representación de Lineweaver-Burk",
        xaxis_title="1/[S] (mM⁻¹)", yaxis_title="1/v (min/unidad)",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=20, r=20, t=70, b=20),
    )
    return fig


def comparison_table(mechanisms, Vmax, Km, I, Kic, Kiu, Ki):
    rows = []
    rescue = {
        "Sin inhibidor": "No aplica",
        "Competitiva": "Sí, idealmente",
        "Acompetitiva": "No",
        "Mixta": "No completamente",
        "No competitiva pura": "No",
    }
    for m in mechanisms:
        if m == "Sin inhibidor":
            r = evaluate_condition(m, 2.0, Vmax, Km)
        elif m == "Competitiva":
            r = evaluate_condition(m, 2.0, Vmax, Km, I=I, Kic=Kic)
        elif m == "Acompetitiva":
            r = evaluate_condition(m, 2.0, Vmax, Km, I=I, Kiu=Kiu)
        elif m == "Mixta":
            r = evaluate_condition(m, 2.0, Vmax, Km, I=I, Kic=Kic, Kiu=Kiu)
        else:
            r = evaluate_condition(m, 2.0, Vmax, Km, I=I, Ki=Ki)
        if np.isclose(r.Km_app, Km): km_change = "="
        elif r.Km_app > Km: km_change = "↑"
        else: km_change = "↓"
        if np.isclose(r.Vmax_app, Vmax): vmax_change = "="
        elif r.Vmax_app > Vmax: vmax_change = "↑"
        else: vmax_change = "↓"
        rows.append({
            "Mecanismo": m,
            "Km aparente (mM)": round(r.Km_app, 3),
            "Vmax aparente (unidades/min)": round(r.Vmax_app, 3),
            "Cambio de Km": km_change,
            "Cambio de Vmax": vmax_change,
            "¿Exceso de S rescata?": rescue[m],
        })
    return rows
