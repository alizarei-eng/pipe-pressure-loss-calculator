"""Interactive command-line pipe head-loss calculator."""
from __future__ import annotations

import json
from pathlib import Path

from core.headloss import calculate_head_loss
from core.fluid_properties import estimate_from_ec
from core.pipe_database import (
    load_pipe_database, available_grades, available_sdrs,
    available_pipe_records, internal_diameter_m,
)

ROOT = Path(__file__).resolve().parent


def load_json(filename: str):
    with (ROOT / "databases" / filename).open("r", encoding="utf-8") as file:
        return json.load(file)


def choose_from_list(title: str, items: list[dict], label_key: str = "name") -> dict:
    print(f"\n{title}")
    for item in items:
        print(f"{item['id']}. {item[label_key]}")
    valid = {item["id"]: item for item in items}
    while True:
        try:
            selected = int(input("Enter option number: ").strip())
            if selected in valid:
                return valid[selected]
        except ValueError:
            pass
        print("Invalid selection. Enter one of the listed numbers.")


def ask_float(prompt: str, minimum: float | None = None, allow_zero: bool = False) -> float:
    while True:
        try:
            value = float(input(prompt).strip().replace(",", "."))
            if minimum is not None and (value < minimum or (not allow_zero and value == minimum)):
                raise ValueError
            return value
        except ValueError:
            print("Invalid value. Please enter a valid number.")


def choose_hdpe_diameter(database: dict, grade: str, sdr: float) -> dict:
    records = available_pipe_records(database, grade, sdr)
    print(f"\nAvailable outside diameters for {grade}, SDR {sdr:g}:")
    for index, pipe in enumerate(records, start=1):
        print(f"{index}. OD {pipe['dn_od_mm']:g} mm")
    while True:
        try:
            choice = int(input("Enter diameter option number: ").strip())
            if 1 <= choice <= len(records):
                return records[choice - 1]
        except ValueError:
            pass
        print("Invalid selection. Enter a number from the list.")


def collect_fittings(fittings: list[dict]) -> float:
    print("\nFittings and valves (enter 0 when finished):")
    for item in fittings:
        print(f"{item['id']}. {item['name']} (K = {item['k']:g})")
    total_k = 0.0
    while True:
        try:
            choice = int(input("Fitting option number (0 = finish): ").strip())
        except ValueError:
            print("Enter a number.")
            continue
        if choice == 0:
            break
        selected = next((item for item in fittings if item["id"] == choice), None)
        if selected is None:
            print("Invalid fitting number.")
            continue
        quantity = int(ask_float("Quantity: ", minimum=1))
        contribution = selected["k"] * quantity
        total_k += contribution
        print(f"Added K = {contribution:g}; running total K = {total_k:g}")
    return total_k


def collect_fluid_properties():
    print("\nFLUID INPUT — EC-BASED ESTIMATE")
    print("1. Generic water (fresh/brackish/well water; no ion split)")
    print("2. Natural seawater composition profile (assumed standard ion ratios)")
    profile_choice = input("Select composition profile [1-2]: ").strip()
    profile = "natural_seawater" if profile_choice == "2" else "generic"
    ec = ask_float("Electrical conductivity EC (mS/cm, temperature-compensated to 25 °C): ", minimum=0, allow_zero=True)
    temperature = ask_float("Water temperature (°C): ", minimum=0, allow_zero=True)
    factor = ask_float("TDS conversion factor [0.65]: ", minimum=0, allow_zero=True)
    if factor == 0:
        factor = 0.65
    return estimate_from_ec(
        ec_ms_cm=ec,
        temperature_c=temperature,
        tds_factor=factor,
        composition_profile=profile,
        ec_reference_temperature_c=25.0,
    )


def main() -> None:
    material_data = load_json("pipe_materials.json")
    fitting_data = load_json("fittings.json")
    pipe_database = load_pipe_database()

    print("=" * 62)
    print("PIPE HEAD-LOSS CALCULATOR")
    print("Main result: total head loss in metres of fluid (m)")
    print("=" * 62)

    fluid = collect_fluid_properties()
    material = choose_from_list("Select pipe material:", material_data["materials"])
    pipe_record = None

    if material["uses_hdpe_database"]:
        grades = [{"id": i, "name": grade} for i, grade in enumerate(available_grades(pipe_database), 1)]
        grade_choice = choose_from_list("Select HDPE material grade:", grades)
        grade = grade_choice["name"]
        sdrs = [{"id": i, "name": f"SDR {sdr:g}", "value": sdr}
                for i, sdr in enumerate(available_sdrs(pipe_database, grade), 1)]
        sdr_choice = choose_from_list("Select SDR:", sdrs)
        pipe_record = choose_hdpe_diameter(pipe_database, grade, sdr_choice["value"])
        diameter_m = internal_diameter_m(pipe_record)
        print(f"Selected pipe: {grade}, SDR {sdr_choice['value']:g}, OD {pipe_record['dn_od_mm']:g} mm, ID {diameter_m*1000:.2f} mm")
    else:
        diameter_m = ask_float("Enter pipe internal diameter (mm): ", minimum=0) / 1000.0

    roughness = material["roughness_mm"]
    if roughness is None:
        roughness = ask_float("Enter absolute roughness (mm): ", minimum=0, allow_zero=True)
    else:
        print(f"Default absolute roughness: {roughness:g} mm ({material['roughness_label']})")
        if input("Use this default? [Y/n]: ").strip().lower() == "n":
            roughness = ask_float("Enter absolute roughness (mm): ", minimum=0, allow_zero=True)

    flow = ask_float("\nFlow rate (m3/h): ", minimum=0)
    length = ask_float("Straight pipe length (m): ", minimum=0, allow_zero=True)
    total_k = collect_fittings(fitting_data["fittings"])

    result = calculate_head_loss(
        flow_m3_h=flow, length_m=length, internal_diameter_m=diameter_m,
        roughness_mm=roughness, minor_loss_k=total_k,
        density_kg_m3=fluid.density_kg_m3,
        kinematic_viscosity_m2_s=fluid.kinematic_viscosity_m2_s,
    )

    print("\n" + "=" * 62)
    print("FLUID PROPERTY ESTIMATES")
    print("=" * 62)
    print(f"EC                        : {fluid.ec_ms_cm:.3f} mS/cm")
    print(f"Estimated TDS             : {fluid.tds_mg_l:.0f} mg/L")
    print(f"Estimated density         : {fluid.density_kg_m3:.3f} kg/m3")
    print(f"Estimated dynamic viscosity: {fluid.dynamic_viscosity_pa_s:.6g} Pa.s")
    print(f"Estimated kinematic viscosity: {fluid.kinematic_viscosity_m2_s:.6g} m2/s")
    for warning in fluid.warnings:
        print(f"NOTE: {warning}")

    print("\nCALCULATION RESULTS")
    print("=" * 62)
    print(f"Flow rate                 : {result['flow_m3_h']:.3f} m3/h")
    print(f"Pipe internal diameter    : {result['internal_diameter_mm']:.2f} mm")
    print(f"Flow velocity             : {result['velocity_m_s']:.3f} m/s")
    print(f"Reynolds number           : {result['reynolds']:.0f}")
    print(f"Flow regime               : {result['flow_regime']}")
    print(f"Darcy friction factor     : {result['friction_factor_darcy']:.5f}")
    print(f"Total minor-loss K        : {total_k:.3f}")
    print("-" * 62)
    print(f"Major head loss           : {result['major_head_loss_m']:.4f} m")
    print(f"Minor head loss           : {result['minor_head_loss_m']:.4f} m")
    print(f"TOTAL HEAD LOSS           : {result['total_head_loss_m']:.4f} m")
    print(f"Equivalent pressure drop  : {result['pressure_drop_bar']:.4f} bar")
    if result["warning"]:
        print(f"WARNING: {result['warning']}")
    print("=" * 62)


if __name__ == "__main__":
    main()
