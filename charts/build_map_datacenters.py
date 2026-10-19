import os
import json
import pandas as pd
import plotly.express as px

OUT_DIR = os.path.join(os.path.dirname(__file__))
DATA_DIR = os.path.join(OUT_DIR, "data")

# 1. DATOS DE MÉXICO (Capacidad en MW)
mexico_data = [
    {"lat": 20.5888, "lon": -100.3899, "ciudad": "Querétaro (El Marqués)", "pais": "México", "operador": "Microsoft, AWS, Google, Equinix", "mw": 82},
    {"lat": 20.5000, "lon": -100.3167, "ciudad": "Pedro Escobedo / Colón", "pais": "México", "operador": "KIO Networks (QRO2)", "mw": 149},
    {"lat": 20.5500, "lon": -100.3500, "ciudad": "Colón (Ascenty QRO 1)", "pais": "México", "operador": "Ascenty QRO 1", "mw": 25},
    {"lat": 20.5300, "lon": -100.3800, "ciudad": "Colón (Ascenty QRO 2)", "pais": "México", "operador": "Ascenty QRO 2", "mw": 31},
    {"lat": 25.7800, "lon": -100.1900, "ciudad": "Monterrey (Apodaca)", "pais": "México", "operador": "Equinix, KIO Networks", "mw": 5},
    {"lat": 19.3667, "lon": -99.2667, "ciudad": "CDMX (Santa Fe/Interlomas)", "pais": "México", "operador": "KIO Networks", "mw": 17},
    {"lat": 19.6500, "lon": -99.2167, "ciudad": "Tultitlán / Toluca", "pais": "México", "operador": "KIO Networks", "mw": 10},
    {"lat": 20.9167, "lon": -100.7500, "ciudad": "San Miguel de Allende", "pais": "México", "operador": "ODATA (Aligned)", "mw": 10},
    {"lat": 20.5500, "lon": -100.3833, "ciudad": "Apaseo el Grande", "pais": "México", "operador": "ODATA (Aligned)", "mw": 20},
    {"lat": 31.6900, "lon": -106.4200, "ciudad": "Ciudad Juárez", "pais": "México", "operador": "Microsoft", "mw": 30},
    {"lat": 29.0700, "lon": -110.9600, "ciudad": "Hermosillo", "pais": "México", "operador": "KIO Networks", "mw": 3},
    {"lat": 20.9700, "lon": -89.6200, "ciudad": "Mérida", "pais": "México", "operador": "KIO Networks", "mw": 3},
]
df_mx = pd.DataFrame(mexico_data)
# REFUERZO VISUAL: Tamaño mínimo de 25 MW para que los puntos mexicanos sean inconfundibles
df_mx["size_plot"] = df_mx["mw"].clip(lower=25) 

# 2. DATOS DE EE. UU.
with open(os.path.join(DATA_DIR, "facilities.json"), encoding="utf-8") as f:
    raw = json.load(f)

us_rows = []
for item in raw:
    if item.get("status") != "operational": continue
    loc = item.get("location", {})
    lat, lon = loc.get("lat"), loc.get("lon")
    if lat is None or lon is None: continue
    state = loc.get("state", "")
    if not (isinstance(state, str) and len(state) == 2): continue
    cap = item.get("capacityMw", {})
    mw = cap.get("operational") if isinstance(cap, dict) else None
    if mw is None or mw <= 0: continue
    
    us_rows.append({
        "lat": lat, "lon": lon,
        "ciudad": loc.get("city", "—") + ", " + state,
        "pais": "EE. UU.", "operador": item.get("operator", "—"), "mw": mw,
    })

df_us = pd.DataFrame(us_rows)
df_us["size_plot"] = df_us["mw"]

# 3. MAPA
df = pd.concat([df_mx, df_us], ignore_index=True)
color_map = {"México": "#008080", "EE. UU.": "#d97706"}

fig = px.scatter_mapbox(
    df, lat="lat", lon="lon", hover_name="ciudad",
    hover_data={"mw": ":.1f", "operador": True, "pais": True, "lat": False, "lon": False, "size_plot": False},
    color="pais", 
    color_discrete_map=color_map,
    size="size_plot", 
    size_max=45,  # Aumentado para dar más presencia a México
    zoom=3.2,
    center={"lat": 32.0, "lon": -100.0},
    mapbox_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json?key=cb1_4oen_1_58899ed8f4e28ff55e594d4c",
    title="Capacidad instalada de Data Centers (MW por sitio)",
)

# Forzamos el zoom y los controles (sin tocar marker.line)
fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    height=550,
    legend=dict(title="País", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    mapbox=dict(
        zoom=3.2,
        center={"lat": 32.0, "lon": -100.0},
        style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json?key=cb1_4oen_1_58899ed8f4e28ff55e594d4c"
    )
)

config = {
    "displayModeBar": True,         
    "displaylogo": False,
    "scrollZoom": True,             
    "responsive": True,
    "modeBarButtonsToAdd": ["zoomInMapbox", "zoomOutMapbox", "resetViewMapbox"] 
}

fig.write_html(
    os.path.join(OUT_DIR, "map_datacenters.html"),
    include_plotlyjs="cdn",
    full_html=True,
    config=config,
)

print(f"🇺🇸 EE. UU.: {len(df_us)} data centers")
print(f"🇲🇽 México: {len(df_mx)} puntos (tamaño mínimo reforzado a 25 MW)")
print("✅ Generado: map_datacenters.html con zoom habilitado")