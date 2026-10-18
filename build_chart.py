"""
Genera un gráfico interactivo de la inversión global de VC (2021-2025)
con desglose IA vs No-IA, y lo exporta como index.html autónomo
para desplegar en Netlify.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# 1. DATOS (fuente principal: Crunchbase vía CNBC TV18, feb 2026)
# ============================================================
df = pd.DataFrame({
    "year":       [2021, 2022, 2023, 2024, 2025],
    "total_vc":   [702,  469,  307,  327,  405],   # miles de millones USD
    "ai":         [97,   63,   64,   114,  202],
    "non_ai":     [605,  406,  243,  213,  203],
})
df["ai_share_pct"] = (df["ai"] / df["total_vc"] * 100).round(1)

# ============================================================
# 2. FIGURA: barras apiladas + línea de participación IA
# ============================================================
fig = make_subplots(
    specs=[[{"secondary_y": True}]],
    subplot_titles=(
        "Inversión global de Venture Capital 2021–2025<br>"
        "<sup>Barras: capital en miles de millones USD · Línea: % del total destinado a IA</sup>",
    ),
)

# --- Barras apiladas: No-IA (base) ---
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

# --- Barras apiladas: IA (encima) ---
fig.add_trace(
    go.Bar(
        x=df["year"],
        y=df["ai"],
        name="Empresas de IA",
        marker_color="#e63946",
        hovertemplate="<b>%{x}</b><br>IA: $%{y:.0f} B<extra></extra>",
    ),
    secondary_y=False,
)

# --- Etiquetas del total sobre cada barra ---
for _, row in df.iterrows():
    fig.add_annotation(
        x=row["year"],
        y=row["total_vc"],
        text=f"<b>${row['total_vc']:.0f} B</b>",
        showarrow=False,
        yshift=14,
        font=dict(size=12, color="#222"),
    )

# --- Línea: % de IA sobre el total (eje secundario) ---
fig.add_trace(
    go.Scatter(
        x=df["year"],
        y=df["ai_share_pct"],
        name="% del VC global destinado a IA",
        mode="lines+markers+text",
        text=[f"{v:.0f}%" for v in df["ai_share_pct"]],
        textposition="top center",
        line=dict(color="#1d3557", width=3, dash="dot"),
        marker=dict(size=10, color="#1d3557"),
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
            "a 1 de cada 2 (2025)<br>"
            "<sup>Fuente: Crunchbase vía CNBC TV18 (feb 2026) · "
            "Cifras en miles de millones USD</sup>"
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
        y=-0.18,
        xanchor="center",
        x=0.5,
        font=dict(size=12),
    ),
    hovermode="x unified",
    margin=dict(t=110, b=90, l=70, r=70),
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

# ============================================================
# 4. EXPORTAR HTML AUTÓNOMO (para Netlify)
# ============================================================
fig.write_html(
    "index.html",
    include_plotlyjs="cdn",   # más ligero; Netlify sirve el CDN
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

print("✅ Generado: index.html")
print(df.to_string(index=False))