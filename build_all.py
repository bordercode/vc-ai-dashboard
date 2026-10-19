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

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

SCRIPTS = [
    "charts/build_vc_ai.py",
    "charts/build_segments.py",
    "charts/build_map_datacenters.py",   # ← descomentar cuando crees el mapa
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
        result = subprocess.run([sys.executable, str(script_path)], check=False)
        if result.returncode != 0:
            failed.append(script)
            print(f"❌ Falló: {script}\n")
        else:
            print(f"✅ OK: {script}\n")
    if failed:
        print("⚠️  Fallaron:", failed)
        sys.exit(1)
    print("🎉 Todos los gráficos regenerados.")

if __name__ == "__main__":
    main()