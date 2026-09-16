"""Rutas seguras para recursos gráficos."""
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
MECHANISM_IMAGES = {
    "Sin inhibidor": "01_sin_inhibidor.png",
    "Competitiva": "02_competitiva.png",
    "Acompetitiva": "03_acompetitiva.png",
    "Mixta": "04_mixta.png",
    "No competitiva pura": "05_no_competitiva.png",
}


def mechanism_image_path(mechanism: str) -> Path | None:
    name = MECHANISM_IMAGES.get(mechanism)
    if not name:
        return None
    path = ASSETS / name
    return path if path.exists() else None


def optional_asset(name: str) -> Path | None:
    path = ASSETS / name
    return path if path.exists() else None
