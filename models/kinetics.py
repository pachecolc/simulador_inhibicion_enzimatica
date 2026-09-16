"""Modelo cinético para el simulador educativo de inhibición enzimática."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
import numpy as np

MECHANISMS = (
    "Sin inhibidor",
    "Competitiva",
    "Acompetitiva",
    "Mixta",
    "No competitiva pura",
)


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} debe ser positivo y finito.")
    return value


def _nonnegative(name: str, value: float) -> float:
    value = float(value)
    if not np.isfinite(value) or value < 0:
        raise ValueError(f"{name} debe ser no negativo y finito.")
    return value


def _substrate_array(S: Any) -> np.ndarray:
    arr = np.asarray(S, dtype=float)
    if np.any(~np.isfinite(arr)) or np.any(arr < 0):
        raise ValueError("[S] debe contener valores no negativos y finitos.")
    return arr


def _restore_type(original: Any, value: np.ndarray):
    return float(value) if np.ndim(original) == 0 else value


def michaelis_menten(S, Vmax: float, Km: float):
    """v0 = Vmax*S/(Km+S). Admite escalar o arreglo de S."""
    Vmax = _positive("Vmax", Vmax)
    Km = _positive("Km", Km)
    arr = _substrate_array(S)
    v = Vmax * arr / (Km + arr)
    return _restore_type(S, v)


def inhibition_factors(I: float, Kic: float, Kiu: float) -> tuple[float, float]:
    """Factores del modelo general reversible: alpha y alpha'."""
    I = _nonnegative("[I]", I)
    Kic = _positive("Kic", Kic)
    Kiu = _positive("Kiu", Kiu)
    return 1.0 + I / Kic, 1.0 + I / Kiu


def velocity_from_factors(S, Vmax: float, Km: float, alpha: float, alpha_p: float):
    """v = Vmax*S/(alpha*Km + alpha'*S)."""
    Vmax = _positive("Vmax", Vmax)
    Km = _positive("Km", Km)
    alpha = _positive("alpha", alpha)
    alpha_p = _positive("alpha'", alpha_p)
    arr = _substrate_array(S)
    den = alpha * Km + alpha_p * arr
    if np.any(den <= 0) or np.any(~np.isfinite(den)):
        raise ValueError("El denominador cinético no es válido.")
    v = Vmax * arr / den
    return _restore_type(S, v)


def inhibited_velocity(S, Vmax: float, Km: float, I: float, Kic: float, Kiu: float):
    alpha, alpha_p = inhibition_factors(I, Kic, Kiu)
    return velocity_from_factors(S, Vmax, Km, alpha, alpha_p)


def apparent_parameters(Vmax: float, Km: float, alpha: float, alpha_p: float) -> tuple[float, float]:
    """Retorna (Vmax_app, Km_app)."""
    Vmax = _positive("Vmax", Vmax)
    Km = _positive("Km", Km)
    alpha = _positive("alpha", alpha)
    alpha_p = _positive("alpha'", alpha_p)
    return Vmax / alpha_p, (alpha / alpha_p) * Km


def competitive(S, Vmax: float, Km: float, I: float, Kic: float):
    I = _nonnegative("[I]", I)
    Kic = _positive("Kic", Kic)
    return velocity_from_factors(S, Vmax, Km, 1.0 + I / Kic, 1.0)


def uncompetitive(S, Vmax: float, Km: float, I: float, Kiu: float):
    I = _nonnegative("[I]", I)
    Kiu = _positive("Kiu", Kiu)
    return velocity_from_factors(S, Vmax, Km, 1.0, 1.0 + I / Kiu)


def mixed(S, Vmax: float, Km: float, I: float, Kic: float, Kiu: float):
    return inhibited_velocity(S, Vmax, Km, I, Kic, Kiu)


def pure_noncompetitive(S, Vmax: float, Km: float, I: float, Ki: float):
    I = _nonnegative("[I]", I)
    Ki = _positive("Ki", Ki)
    alpha = 1.0 + I / Ki
    return velocity_from_factors(S, Vmax, Km, alpha, alpha)


def mechanism_velocity(
    mechanism: str,
    S,
    Vmax: float,
    Km: float,
    I: float = 0.0,
    Kic: float | None = None,
    Kiu: float | None = None,
    Ki: float | None = None,
):
    if mechanism not in MECHANISMS:
        raise ValueError(f"Mecanismo no reconocido: {mechanism}")
    if mechanism == "Sin inhibidor":
        return michaelis_menten(S, Vmax, Km)
    if mechanism == "Competitiva":
        return competitive(S, Vmax, Km, I, _positive("Kic", Kic))
    if mechanism == "Acompetitiva":
        return uncompetitive(S, Vmax, Km, I, _positive("Kiu", Kiu))
    if mechanism == "Mixta":
        return mixed(S, Vmax, Km, I, _positive("Kic", Kic), _positive("Kiu", Kiu))
    return pure_noncompetitive(S, Vmax, Km, I, _positive("Ki", Ki))


@dataclass(frozen=True)
class KineticResult:
    mechanism: str
    S: float
    I: float
    Km: float
    Vmax: float
    Kic: float | None
    Kiu: float | None
    Ki: float | None
    alpha: float
    alpha_p: float
    Km_app: float
    Vmax_app: float
    velocity: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_condition(
    mechanism: str,
    S: float,
    Vmax: float,
    Km: float,
    I: float = 0.0,
    Kic: float | None = None,
    Kiu: float | None = None,
    Ki: float | None = None,
) -> KineticResult:
    S = _nonnegative("[S]", S)
    I = _nonnegative("[I]", I)
    Vmax = _positive("Vmax", Vmax)
    Km = _positive("Km", Km)
    if mechanism not in MECHANISMS:
        raise ValueError(f"Mecanismo no reconocido: {mechanism}")

    used_kic = used_kiu = used_ki = None
    if mechanism == "Sin inhibidor":
        alpha = alpha_p = 1.0
        I = 0.0
    elif mechanism == "Competitiva":
        used_kic = _positive("Kic", Kic)
        alpha, alpha_p = 1.0 + I / used_kic, 1.0
    elif mechanism == "Acompetitiva":
        used_kiu = _positive("Kiu", Kiu)
        alpha, alpha_p = 1.0, 1.0 + I / used_kiu
    elif mechanism == "Mixta":
        used_kic = _positive("Kic", Kic)
        used_kiu = _positive("Kiu", Kiu)
        alpha, alpha_p = inhibition_factors(I, used_kic, used_kiu)
    else:
        used_ki = _positive("Ki", Ki)
        alpha = alpha_p = 1.0 + I / used_ki

    Vmax_app, Km_app = apparent_parameters(Vmax, Km, alpha, alpha_p)
    v = velocity_from_factors(S, Vmax, Km, alpha, alpha_p)
    return KineticResult(
        mechanism=mechanism, S=S, I=I, Km=Km, Vmax=Vmax,
        Kic=used_kic, Kiu=used_kiu, Ki=used_ki,
        alpha=alpha, alpha_p=alpha_p,
        Km_app=Km_app, Vmax_app=Vmax_app, velocity=float(v),
    )


def mixed_tendency(alpha: float, alpha_p: float, rtol: float = 1e-3) -> str:
    if np.isclose(alpha, alpha_p, rtol=rtol, atol=rtol):
        return "cercano a no competitivo puro"
    if alpha > alpha_p:
        return "predominio competitivo"
    return "predominio acompetitivo"


def validate_model_cases(tol: float = 1e-6) -> list[dict[str, Any]]:
    """Casos de prueba científicos del material de referencia."""
    cases = []

    r1 = evaluate_condition("Sin inhibidor", 2, 100, 2)
    cases.append({"Caso": 1, "Resultado esperado": "v=50", "Resultado obtenido": f"v={r1.velocity:.6g}", "Estado": abs(r1.velocity - 50) < tol})

    r2 = evaluate_condition("Competitiva", 2, 100, 2, I=2, Kic=2)
    cases.append({"Caso": 2, "Resultado esperado": "Km_app=4; Vmax_app=100", "Resultado obtenido": f"Km_app={r2.Km_app:.6g}; Vmax_app={r2.Vmax_app:.6g}", "Estado": abs(r2.Km_app - 4) < tol and abs(r2.Vmax_app - 100) < tol})

    r3 = evaluate_condition("Acompetitiva", 2, 100, 2, I=2, Kiu=2)
    cases.append({"Caso": 3, "Resultado esperado": "Km_app=1; Vmax_app=50", "Resultado obtenido": f"Km_app={r3.Km_app:.6g}; Vmax_app={r3.Vmax_app:.6g}", "Estado": abs(r3.Km_app - 1) < tol and abs(r3.Vmax_app - 50) < tol})

    r4 = evaluate_condition("No competitiva pura", 2, 100, 2, I=2, Ki=2)
    cases.append({"Caso": 4, "Resultado esperado": "Km_app=2; Vmax_app=50", "Resultado obtenido": f"Km_app={r4.Km_app:.6g}; Vmax_app={r4.Vmax_app:.6g}", "Estado": abs(r4.Km_app - 2) < tol and abs(r4.Vmax_app - 50) < tol})

    # alpha=2 y alpha'=1.5 se obtienen, por ejemplo, con I=1, Kic=1, Kiu=2.
    r5 = evaluate_condition("Mixta", 2, 100, 2, I=1, Kic=1, Kiu=2)
    cases.append({"Caso": 5, "Resultado esperado": "Km_app≈2.6667; Vmax_app≈66.6667", "Resultado obtenido": f"Km_app={r5.Km_app:.6g}; Vmax_app={r5.Vmax_app:.6g}", "Estado": abs(r5.Km_app - 8/3) < tol and abs(r5.Vmax_app - 200/3) < tol})
    return cases
