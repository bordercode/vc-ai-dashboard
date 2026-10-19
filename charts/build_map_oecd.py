"""
Mapa de concentración geográfica de la inversión en IA (2025).
Fuente: OECD, "AI firms capture 61% of global venture capital in 2025" (feb 2026).
Cifras: valor de deals de VC en IA atraídos por empresas de cada país/región.
"""

import os
import pandas as pd
import plotly.express as px

OUT_DIR = os.path.join(os.path.dirname(__file__))

# ============================================================
# DATOS OECD (2025) — valor de deals atraídos
# ============================================================
# Nota: la OECD reporta "EU27" como bloque, no países individuales.
# Para el mapa usamos los países que la OECD reporta por separado
# (EE.UU., China, Reino Unido) + el bloque UE27 como un valor agregado.
# Los países de la UE se colorean con el valor agregado (15.8 B) para
# evitar inventar cifras nacionales que la fuente no publica.

df = pd.DataFrame({
    "iso3":  ["USA", "CHN", "GBR", "EU27"],
    "pais":  ["Estados Unidos", "China", "Reino Unido", "Unión Europea (27)"],
    "valor_busd": [194.0, 13.9, 13.8, 15.8],
    "share_pct": [75, 5, 5, 6],
})

# Para el mapa, la OECD solo desagrega EE.UU., China y Reino Unido.
# La UE27 se representa con un valor agregado que aplicamos a sus miembros
# (con una nota en el pie). Para mantener el mapa limpio, coloreamos
# los 27 países de la UE con el mismo valor (15.8 B) y lo indicamos.
EU27_ISO3 = [
    "AUT","BEL","BGR","HRV","CYP","CZE","DNK","EST","FIN","FRA",
    "DEU","GRC","HUN","IRL","ITA","LVA","LTU","LUX","MLT","NLD",
    "POL","PRT","ROU","SVK","SVN","ESP","SWE",
]

rows = []
# Países con dato propio
for _, r in df[df["iso3"] != "EU27"].iterrows():
    rows.append({"iso3": r["iso3"], "pais": r["pais"],
                 "valor_busd": r["valor_busd"], "share_pct": r["share_pct"]})
# Miembros UE27 con el valor agregado del bloque
for iso in EU27_ISO3:
    rows.append({"iso3": iso, "pais": "Unión Europea (agregado)",
                 "valor_busd": 15.8, "share_pct": 6})

map_df = pd.DataFrame(rows)

# ============================================================
# MAPA
# ============================================================
fig = px.choropleth(
    map_df,
    locations="iso3",
    color="valor_busd",
    hover_name="pais",
    hover_data={
        "valor_busd": ":,.1f",
        "share_pct": ":.1f",
        "iso3": False,
    },
    labels={
        "valor_busd": "Inversión IA (B USD)",
        "share_pct": "% del total global",
    },
    color_continuous_scale=[
        [0.00, "#e5e7eb"],   # países sin dato
        [0.01, "#c7e9e5"],
        [0.30, "#5ab4ac"],
        [0.70, "#008080"],
        [1.00, "#005f5f"],
    ],
    range_color=(0, 200),
)

fig.update_geos(
    showcountries=True,
    countrycolor="#d1d5db",
    showcoastlines=False,
    showframe=False,
    projection_type="natural earth",
    fitbounds="locations",
)

fig.update_layout(
    margin=dict(t=10, b=10, l=10, r=10),
    height=520,
    coloraxis_colorbar=dict(
        title="B USD",
        thickness=14,
        len=0.7,
        tickfont=dict(size=10),
    ),
    geo=dict(bgcolor="rgba(0,0,0,0)"),
)

fig.write_html(
    os.path.join(OUT_DIR, "map_oecd.html"),
    include_plotlyjs="cdn",
    full_html=True,
    config={
        "displayModeBar": False,
        "displaylogo": False,
        "responsive": True,
    },
)

print("✅ Generado: map_oecd.html")
print(map_df[map_df["iso3"].isin(["USA","CHN","GBR"])].to_string(index=False))