"""
Dos gráficos para la slide 5:
1) Distribución del VC en IA por segmento (OECD 2025) - desglose ampliado
2) Serie de tiempo del Capex de hiperescaladores en data centers (2021-2025)
"""

import os
import pandas as pd
import plotly.graph_objects as go

OUT_DIR = os.path.join(os.path.dirname(__file__))

# ============================================================
# GRÁFICO 1: Distribución por segmento (OECD 2025) - 9 categorías
# ============================================================
# Datos OECD: IT Infraestructura y Hosting = 109.3 B USD (42% del total IA = 258.7 B)
# Resto = 149.4 B USD. La OECD NO desagrega el "Resto" en categorías para 2025.
# Las categorías siguientes son ESTIMACIONES basadas en:
#   - la lista de 20 industrias que usa la OECD (Preqin labels)
#   - las menciones cualitativas del informe sobre sectores
# "Otras industrias" es el remanente calculado.
# ADVERTENCIA EN CAPTION.

df_seg = pd.DataFrame({
    "segmento": [
        "IT Infraestructura y Hosting\n(data centers, cómputo, modelos)",
        "Servicios empresariales\n(estimado)",
        "Servicios de IT y software\n(estimado)",
        "Salud, farma y biotecnología\n(estimado)",
        "Comercio minorista y consumo\n(estimado)",
        "Movilidad y vehículos autónomos\n(estimado)",
        "Energía y cleantech\n(estimado)",
        "Finanzas y seguros\n(estimado)",
        "Otras industrias\n(media, educación, gobierno)",
    ],
    "valor": [109.3, 35.0, 20.0, 20.0, 18.0, 15.0, 15.0, 10.0, 8.4],
    "share": [42.3, 13.5, 7.7, 7.7, 7.0, 5.8, 5.8, 3.9, 3.2],
    "color": [
        "#008080",  # Infraestructura - teal destacado
        "#9aa5b1", "#9aa5b1", "#9aa5b1", "#9aa5b1",
        "#9aa5b1", "#9aa5b1", "#9aa5b1", "#9aa5b1",
    ],
})

fig1 = go.Figure()

fig1.add_trace(go.Bar(
    x=df_seg["valor"],
    y=df_seg["segmento"],
    orientation="h",
    marker_color=df_seg["color"],
    text=[f"${v:.1f} B ({s:.0f}%)" for v, s in zip(df_seg["valor"], df_seg["share"])],
    textposition="outside",
    textfont=dict(size=10),
    hovertemplate="<b>%{y}</b><br>Inversión: $%{x:.1f} B<extra></extra>",
))

fig1.update_layout(
    title=dict(
        text="El segmento de infraestructura es el que<br>más capital concentra (2025)",
        font=dict(size=13, color="#005f5f"),
        x=0.5, xanchor="center",
    ),
    xaxis=dict(
        title="Inversión VC en IA (miles de millones USD)",
        range=[0, 140],
        gridcolor="#e5e7eb",
        title_font=dict(size=10),
        tickfont=dict(size=9),
    ),
    yaxis=dict(
        tickfont=dict(size=9),
        autorange="reversed",
    ),
    height=480,
    margin=dict(t=55, b=45, l=20, r=130),
    plot_bgcolor="white",
    showlegend=False,
)

fig1.write_html(
    os.path.join(OUT_DIR, "segments_oecd.html"),
    include_plotlyjs="cdn",
    full_html=True,
    config={"displayModeBar": False, "displaylogo": False, "responsive": True},
)
print("✅ Generado: segments_oecd.html (9 categorías)")


# ============================================================
# GRÁFICO 2: Serie de tiempo Capex hiperescaladores (2021-2025)
# ============================================================
df_ts = pd.DataFrame({
    "year": [2021, 2022, 2023, 2024, 2025],
    "capex": [127.1, 149.8, 140.7, 224.4, 315.0],
})

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=df_ts["year"],
    y=df_ts["capex"],
    mode="lines+markers+text",
    text=[f"${v:.0f} B" for v in df_ts["capex"]],
    textposition="top center",
    textfont=dict(size=12),
    line=dict(color="#d00000", width=4),
    marker=dict(size=10, color="#d00000"),
    fill="tozeroy",
    fillcolor="rgba(208, 0, 0, 0.08)",
    hovertemplate="<b>%{x}</b><br>Capex: $%{y:.0f} B<extra></extra>",
))

fig2.update_layout(
    title=dict(
        text="La inversión en data centers crece de forma exponencial",
        font=dict(size=13, color="#005f5f"),
        x=0.5, xanchor="center",
    ),
    xaxis=dict(
        tickmode="array",
        tickvals=df_ts["year"],
        tickfont=dict(size=11),
        showgrid=False,
        range=[2020.5, 2025.8],
    ),
    yaxis=dict(
        title="Capex de hiperescaladores (miles de millones USD)",
        range=[0, 400],
        gridcolor="#e5e7eb",
        title_font=dict(size=10),
        tickfont=dict(size=10),
    ),
    height=480,
    margin=dict(t=55, b=45, l=65, r=35),
    plot_bgcolor="white",
    showlegend=False,
)

fig2.write_html(
    os.path.join(OUT_DIR, "datacenter_trend.html"),
    include_plotlyjs="cdn",
    full_html=True,
    config={"displayModeBar": False, "displaylogo": False, "responsive": True},
)
print("✅ Generado: datacenter_trend.html")