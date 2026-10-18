r"""
Script maestro: regenera todos los gráficos del deck.

Uso (desde la raíz del repo):
    python build_all.py

El script detecta automáticamente la carpeta del proyecto,
sin importar dónde esté alojado en el sistema de archivos.
"""

import subprocess
import sys
import os
from pathlib import Path

# Asegurarnos de ejecutar desde la raíz del repo (donde vive este archivo)
ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

# Lista de scripts a ejecutar, en orden.
# Cuando agregues un gráfico nuevo, añade aquí su build_*.py
SCRIPTS = [
    "charts/build_vc_ai.py",
    # "charts/build_map_geo.py",      # ← descomentar cuando exista
    # "charts/build_segments.py",     # ← descomentar cuando exista
    # "charts/build_sources.py",
    # "charts/build_deal_size.py",
]

def main():
    print(f"📁 Directorio de trabajo: {ROOT}\n")

    failed = []
    for script in SCRIPTS:
        script_path = ROOT / script
        if not script_path.exists():
            print(f"⚠️  No encontrado: {script} — se omite")
            continue

        print(f"▶️  Ejecutando {script} ...")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=False,            # no abortar si uno falla
        )
        if result.returncode != 0:
            failed.append(script)
            print(f"❌ Falló: {script} (código {result.returncode})\n")
        else:
            print(f"✅ OK: {script}\n")

    if failed:
        print("⚠️  Algunos scripts fallaron:")
        for s in failed:
            print(f"   - {s}")
        sys.exit(1)
    else:
        print("🎉 Todos los gráficos fueron regenerados correctamente.")

if __name__ == "__main__":
    main()