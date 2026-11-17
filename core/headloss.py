"""Pipe head-loss calculations using Darcy-Weisbach."""
from __future__ import annotations

import math
from .friction import darcy_friction_factor

GRAVITY_M_S2 = 9.80665
WATER_DENSITY_KG_M3 = 998.2
WATER_KINEMATIC_VISCOSITY_M2_S = 1.004e-6


def calculate_head_loss(
    flow_m3_h: float,
    length_m: float,
    internal_diameter_m: float,
    roughness_mm: float,
    minor_loss_k: float = 0.0,
) -> dict[str, float | str | None]:
    """Calculate flow regime and major/minor/total head loss."""
    values = (flow_m3_h, length_m, internal_diameter_m, roughness_mm, minor_loss_k)
    if any(not math.isfinite(float(value)) for value in values):
        raise ValueError("All inputs must be finite numbers")
    if flow_m3_h <= 0 or length_m < 0 or internal_diameter_m <= 0:
        raise ValueError("Flow and diameter must be positive; length cannot be negative")
    if roughness_mm < 0 or minor_loss_k < 0:
        raise ValueError("Roughness and total K cannot be negative")

    flow_m3_s = flow_m3_h / 3600.0
    area_m2 = math.pi * internal_diameter_m**2 / 4.0
    velocity_m_s = flow_m3_s / area_m2
    reynolds = velocity_m_s * internal_diameter_m / WATER_KINEMATIC_VISCOSITY_M2_S

    if reynolds < 2300:
        flow_regime = "Laminar"
    elif reynolds <= 4000:
        flow_regime = "Transitional"
    else:
        flow_regime = "Turbulent"

    relative_roughness = (roughness_mm / 1000.0) / internal_diameter_m
    friction_factor, warning = darcy_friction_factor(reynolds, relative_roughness)
    velocity_head_m = velocity_m_s**2 / (2.0 * GRAVITY_M_S2)
    major_head_m = friction_factor * (length_m / internal_diameter_m) * velocity_head_m
    minor_head_m = minor_loss_k * velocity_head_m
    total_head_m = major_head_m + minor_head_m
    pressure_drop_bar = WATER_DENSITY_KG_M3 * GRAVITY_M_S2 * total_head_m / 100000.0

    return {
        "flow_m3_h": flow_m3_h,
        "length_m": length_m,
        "internal_diameter_mm": internal_diameter_m * 1000.0,
        "roughness_mm": roughness_mm,
        "velocity_m_s": velocity_m_s,
        "reynolds": reynolds,
        "flow_regime": flow_regime,
        "friction_factor_darcy": friction_factor,
        "velocity_head_m": velocity_head_m,
        "major_head_loss_m": major_head_m,
        "minor_head_loss_m": minor_head_m,
        "total_head_loss_m": total_head_m,
        "pressure_drop_bar": pressure_drop_bar,
        "warning": warning,
    }
