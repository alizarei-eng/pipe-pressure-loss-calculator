"""Darcy friction-factor calculations."""
from __future__ import annotations

import math


def darcy_friction_factor(reynolds: float, relative_roughness: float) -> tuple[float, str | None]:
    """Return Darcy friction factor and an optional flow-regime warning."""
    if reynolds <= 0:
        raise ValueError("Reynolds number must be positive")
    if relative_roughness < 0:
        raise ValueError("Relative roughness cannot be negative")

    if reynolds < 2300:
        return 64.0 / reynolds, None

    warning = None
    if reynolds < 4000:
        warning = (
            "Flow is in the transition region (Re 2300–4000); "
            "friction-factor prediction is uncertain."
        )

    # Colebrook-White equation, solved by fixed-point iteration.
    # The turbulent relation is also evaluated in the transition region,
    # but the warning above must be retained.
    factor = 0.25 / (
        math.log10(relative_roughness / 3.7 + 5.74 / reynolds**0.9) ** 2
    )
    for _ in range(100):
        term = relative_roughness / 3.7 + 2.51 / (reynolds * math.sqrt(factor))
        updated = 1.0 / (-2.0 * math.log10(term)) ** 2
        if abs(updated - factor) < 1e-12:
            factor = updated
            break
        factor = updated

    return factor, warning
