#!/usr/bin/env python3
"""Genera las miniaturas WebP de las galerias a partir de los JPG originales.

Uso (desde la raiz del proyecto):  python tools/generar-galerias.py
Requiere Pillow con soporte WebP. No modifica los originales.
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "images" / "galeria-web"
GALERIAS = ["barcelona", "valencia", "marbella"]
ANCHO_MAX = 800
CALIDAD = 78
METHOD = 6


def numero(ruta):
    return int(re.search(r"-(\d+)\.jpg$", ruta.name).group(1))


def main():
    errores = 0
    for torneo in GALERIAS:
        origen = RAIZ / "images" / f"galeria-{torneo}"
        salida = DESTINO / torneo / "thumb"
        salida.mkdir(parents=True, exist_ok=True)
        fotos = sorted(origen.glob(f"{torneo}-*.jpg"), key=numero)
        total = 0
        for f in fotos:
            try:
                with Image.open(f) as im:
                    im = ImageOps.exif_transpose(im).convert("RGB")
                    if im.width > ANCHO_MAX:
                        alto = round(im.height * ANCHO_MAX / im.width)
                        im = im.resize((ANCHO_MAX, alto), Image.LANCZOS)
                    destino = salida / f"{torneo}-{numero(f):02d}.webp"
                    # sin exif/icc: Pillow solo los escribe si se piden
                    im.save(destino, "WEBP", quality=CALIDAD, method=METHOD)
                    total += 1
            except Exception as e:
                errores += 1
                print(f"ERROR {f}: {e}", file=sys.stderr)
        print(f"{torneo}: {total}/{len(fotos)} miniaturas -> {salida.relative_to(RAIZ)}")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
