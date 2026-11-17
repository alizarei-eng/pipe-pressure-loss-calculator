"""Read pipe dimensions from the project's JSON database."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATABASE_PATH = Path(__file__).resolve().parents[1] / "databases" / "pipe_standards.json"


def load_pipe_database(path: Path = DATABASE_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def available_grades(database: dict[str, Any]) -> list[str]:
    grades = database["scope"]["supported_grade_sdr"]
    return sorted(grades)


def available_sdrs(database: dict[str, Any], grade: str) -> list[float]:
    grades = database["scope"]["supported_grade_sdr"]
    if grade not in grades:
        raise ValueError(f"Unsupported material grade: {grade}")
    return sorted(grades[grade])


def available_pipe_records(
    database: dict[str, Any], grade: str, sdr: float
) -> list[dict[str, Any]]:
    records = [
        pipe for pipe in database["pipes"]
        if pipe["material_grade"] == grade and float(pipe["sdr"]) == float(sdr)
    ]
    return sorted(records, key=lambda item: item["dn_od_mm"])


def find_pipe(
    database: dict[str, Any], grade: str, sdr: float, outside_diameter_mm: float
) -> dict[str, Any]:
    for pipe in available_pipe_records(database, grade, sdr):
        if float(pipe["dn_od_mm"]) == float(outside_diameter_mm):
            return pipe
    raise ValueError(
        f"No database record for {grade}, SDR {sdr}, OD {outside_diameter_mm} mm"
    )


def internal_diameter_m(pipe_record: dict[str, Any]) -> float:
    od_mm = float(pipe_record["dn_od_mm"])
    wall_mm = float(pipe_record["nominal_wall_thickness_mm"])
    inside_mm = od_mm - 2.0 * wall_mm
    if inside_mm <= 0:
        raise ValueError("Calculated internal diameter must be positive")
    return inside_mm / 1000.0
