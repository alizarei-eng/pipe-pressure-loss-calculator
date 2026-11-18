# Pipe Pressure Loss Calculator

Interactive Python calculator for Darcy-Weisbach major losses and K-based minor losses.

## Current features
- HDPE dimensions from the shared 506-record pipe catalogue; other pipe materials use manual ID.
- Numbered menus for material, grade, SDR, diameter and fittings.
- EC-based estimates for TDS, density and viscosity.
- Density and kinematic viscosity are passed into the hydraulic calculation: viscosity affects Reynolds number/friction factor; density converts head loss to pressure drop.
- Flow regime output: Laminar, Transitional, Turbulent.

## Run
```bash
python main.py
python -m unittest discover -s tests -v
```

## EC model limitations
TDS ≈ EC(µS/cm) × selected factor (default 0.65). EC must be temperature-compensated to 25 °C. Generic water mode does not invent individual ion concentrations. Optional natural-seawater ratios are estimates only and are not valid by default for groundwater or RO concentrate. Density and viscosity are approximate screening estimates; use laboratory/validated properties for concentrated brine and final design.

This calculator is steady-state and single-diameter per calculation. It does not yet calculate static elevation, pump TDH, network hydraulics or water hammer.
