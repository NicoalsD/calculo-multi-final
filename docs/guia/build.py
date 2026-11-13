"""Regenera resultados, figuras y el PDF de la guía.

Uso:  .venv/bin/python docs/guia/build.py
"""
import subprocess
import sys
from pathlib import Path

import typst

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "Guia_Proyecto_Calculo_Multivariable.pdf"

for script in ("verificacion.py", "graficos.py"):
    subprocess.run([sys.executable, str(RAIZ / "codigo" / script)], check=True, stdout=subprocess.DEVNULL)

typst.compile(str(RAIZ / "docs" / "guia" / "guia.typ"), output=str(SALIDA), root=str(RAIZ))
print(f"PDF generado: {SALIDA.name}")
