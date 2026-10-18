"""
Genera un gráfico interactivo de la inversión global de VC (2021-2025)
con desglose IA vs No-IA, y lo exporta como vc_ai.html autónomo.
"""

import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

OUT_DIR = os.path.join(os.path.dirname(__file__))

# ============================================================
# 1. DATOS
# ============================================================
df = pd.DataFrame({
    "year":       [2021, 2022, 2023, 2024, 2025],
    "total_vc":   [702,  469,  307,  327,  405],
    "ai":         [97,   63,   64,   114,  202],
    "non_ai":     [605,  406,  243,  213,  203],
})
df["ai_share_pct"] = (df["ai"] / df["total_vc"] * 100).round(1)

# ============================================================
# 2. FIGURA
# ============================================================
fig = make_subplots(
    specs=[[{"secondary_y": True}]],
    subplot_titles=(
        "Inversión global de Venture Capital 2021–2025<br>"
        "<sup>Barras: capital en miles de millones USD · Línea: % del total destinado a IA</sup>",
    ),
)

fig.add_trace(
    go.Bar(
        x=df["year"],
        y=df["non_ai"],
        name="Segmentos No-IA",
        marker_color="#9aa5b1",
        hovertemplate="<b>%{x}</b><br>No-IA: $%{y:.0f} B<extra></extra>",
    ),
    secondary_y=False,
)

fig.add_trace(
    go.Bar(
        x=df["year"],
        y=df["ai"],
        name="Empresas de IA",
        marker_color="#008080",   # ← TEAL
        hovertemplate="<b>%{x}</b><br>IA: $%{y:.0f} B<extra></extra>",
    ),
    secondary_y=False,
)

for _, row in df.iterrows():
    fig.add_annotation(
        x=row["year"],
        y=row["total_vc"],
        text=f"<b>${row['total_vc']:.0f} B</b>",
        showarrow=False,
        yshift=14,
        font=dict(size=12, color="#222"),
    )

fig.add_trace(
    go.Scatter(
        x=df["year"],
        y=df["ai_share_pct"],
        name="% del VC global destinado a IA",
        mode="lines+markers+text",
        text=[f"{v:.0f}%" for v in df["ai_share_pct"]],
        textposition="top center",
        line=dict(color="#d00000", width=5, dash="dot"),   # ← ROJO, MÁS GRUESA
        marker=dict(size=10, color="#d00000"),
        hovertemplate="<b>%{x}</b><br>Participación IA: %{y:.1f}%<extra></extra>",
    ),
    secondary_y=True,
)

# ============================================================
# 3. LAYOUT
# ============================================================
fig.update_layout(
    title=dict(
        text=(
            "La IA pasó de 1 de cada 7 dólares de VC (2021) "
            "a 1 de cada 2 (2025)"
        ),
        x=0.5,
        xanchor="center",
        font=dict(size=18),
    ),
    barmode="stack",
    bargap=0.35,
    template="plotly_white",
    height=650,
    width=1100,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.12,
        xanchor="center",
        x=0.5,
        font=dict(size=12),
    ),
    hovermode="x unified",
    margin=dict(t=100, b=130, l=70, r=70),
)

fig.update_yaxes(
    title_text="Capital invertido (miles de millones USD)",
    range=[0, 780],
    secondary_y=False,
    gridcolor="#e5e7eb",
)
fig.update_yaxes(
    title_text="Participación de IA en el VC global (%)",
    range=[0, 65],
    ticksuffix="%",
    secondary_y=True,
    showgrid=False,
)
fig.update_xaxes(tickmode="array", tickvals=df["year"], tickfont=dict(size=13))

# --- Fuente al pie del gráfico ---
fig.add_annotation(
    text=(
        "Elaboración propia con datos de Crunchbase vía CNBC TV18 (feb 2026) · "
        "Cifras en miles de millones USD"
    ),
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.22,
    xanchor="center",
    yanchor="top",
    showarrow=False,
    font=dict(size=11, color="#555"),
)

# ============================================================
# 4. EXPORTAR
# ============================================================
fig.write_html(
    os.path.join(OUT_DIR, "vc_ai.html"),
    include_plotlyjs="cdn",
    full_html=True,
    config={
        "displayModeBar": True,
        "displaylogo": False,
        "responsive": True,
        "toImageButtonOptions": {
            "format": "png",
            "filename": "vc_ai_global_2021_2025",
            "scale": 2,
        },
    },
)

print("✅ Generado: vc_ai.html")
print(df.to_string(index=False))