# Pipe Pressure Loss Calculator

A Python command-line engineering tool for calculating major and minor hydraulic head losses in pressurized pipes.

**Primary result:** total head loss in metres of water column (mH2O).

## Initial features

- Darcy-Weisbach major head-loss calculation.
- Laminar Darcy friction factor and iterative Colebrook-White solution for turbulent flow.
- Minor losses from numbered fitting and valve menus.
- Numbered material, HDPE grade, SDR, and pipe-size selection.
- HDPE dimensions imported from the companion `hdpe-pipe-diameter-selector` project's JSON reference database.
- Supporting outputs: velocity, Reynolds number, Darcy friction factor, and equivalent pressure drop.

## Run

Python 3.10 or newer is recommended.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python main.py
```

Run tests:

```powershell
python -m unittest discover -s tests -v
```

## Calculation basis

```
Q = flow rate converted from m3/h to m3/s
A = pi * D^2 / 4
V = Q / A
Re = V * D / nu
hf = f * (L / D) * (V^2 / (2*g))
hm = sum(K) * (V^2 / (2*g))
htotal = hf + hm
```

The friction factor is the **Darcy** friction factor, not the Fanning factor.

## Data notes and limitations

- The HDPE dimensional database is imported from the companion project without changing its records or caveats. Some wall thicknesses are ratio-derived and require verification against a controlled copy of the applicable standard before design use.
- Roughness and fitting K values are indicative defaults. Actual values depend on pipe condition, fitting geometry, manufacturer, and installation.
- In this initial version, HDPE uses the dimensional database. Other materials require a manually entered internal diameter.
- Water properties are held at a 20 °C reference condition; temperature is not a user input in this version.
- The transition region (Re 2300–4000) is flagged because friction-factor prediction is uncertain.
- This tool calculates steady-state pipe losses only. It does not yet model elevation change, pumps, transients/water hammer, non-Newtonian fluids, or networks.

This software is an engineering aid, not a substitute for project-specific verification.
