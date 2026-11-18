# Engineering Guide | راهنمای مهندسی
## Pipe Pressure Loss Calculator | محاسبه‌گر افت فشار لوله

## 1. Purpose | هدف
**EN:** Calculate major friction loss and minor fitting loss in a steady, single-path pipe calculation. The primary result is head loss in metres of the flowing fluid; pressure drop is derived using fluid density.

**FA:** محاسبه افت اصطکاکی طولی و افت موضعی فیتینگ‌ها در یک مسیر جریان پایا. خروجی اصلی افت هد بر حسب متر سیال است و افت فشار با استفاده از چگالی محاسبه می‌شود.

## 2. Inputs | ورودی‌ها
- Fluid EC (mS/cm), already compensated to 25°C | EC بر حسب mS/cm و جبران‌شده تا ۲۵ درجه
- Actual operating temperature (°C) | دمای واقعی کارکرد آب
- Composition profile: generic or natural seawater | پروفایل آب عمومی یا آب دریای طبیعی
- Pipe material; HDPE grade, SDR and OD, or ID for other materials | جنس لوله؛ برای HDPE گرید، SDR و OD؛ برای سایر مواد ID
- Flow rate (m³/h), straight length (m) | دبی و طول مستقیم
- Fitting types and quantities | نوع و تعداد فیتینگ‌ها
- Roughness from database or explicit override where available | زبری بانک یا مقدار جایگزین در صورت ارائه گزینه

## 3. Geometry | هندسه
For HDPE, the database supplies nominal wall thickness and the program calculates nominal ID:
`ID = OD - 2e`.
For other materials, the current CLI requests internal diameter directly. Convert mm to m before hydraulic calculations.

برای HDPE ضخامت اسمی از بانک خوانده و قطر داخلی از رابطه بالا محاسبه می‌شود. برای سایر مواد، نسخه فعلی قطر داخلی را مستقیماً از کاربر می‌گیرد. محاسبات هیدرولیکی با واحد متر انجام می‌شوند.

## 4. Hydraulic equations | معادلات هیدرولیکی
`Q_s = Q_h/3600`
`A = πD²/4`
`V = Q_s/A`
`Re = VD/ν`
`ε_r = ε/D`
`hf = f(L/D)(V²/(2g))`
`hm = K_total(V²/(2g))`
`h_total = hf + hm`
`ΔP = ρg h_total`

The roughness ε and diameter D must use the same unit. In the implementation, roughness is entered/stored in mm and converted to metres for relative roughness.

زبری مطلق و قطر باید هم‌واحد باشند. برنامه زبری میلی‌متری را برای محاسبه زبری نسبی به متر تبدیل می‌کند.

## 5. Flow regime and friction factor | رژیم جریان و ضریب اصطکاک
- Re < 2300: Laminar; f=64/Re.
- 2300 ≤ Re ≤ 4000: Transitional; result is flagged as uncertain.
- Re > 4000: Turbulent; iterative Colebrook-type relation.

این حدود برای طبقه‌بندی جریان در برنامه استفاده می‌شوند. ناحیه گذار ذاتاً حساس است؛ نتیجه را با احتیاط تفسیر کنید. ضریب استفاده‌شده Darcy است، نه Fanning؛ این دو چهار برابر اختلاف دارند.

## 6. Worked example | مثال کامل
Given Q=50 m³/h, D=0.100 m, L=100 m, ε=0.007 mm, Ktotal=5, ρ=997 kg/m³ and ν=0.89×10⁻⁶ m²/s:

1. Q = 50/3600 = 0.013889 m³/s.
2. A = π×0.1²/4 = 0.007854 m².
3. V = 0.013889/0.007854 ≈ 1.768 m/s.
4. Re = 1.768×0.1/(0.89×10⁻⁶) ≈ 1.99×10⁵; turbulent.
5. Relative roughness = 0.000007/0.1 = 0.00007.
6. For f≈0.0185, hf≈0.0185×(100/0.1)×(1.768²/(2×9.80665)) ≈ 2.94 m.
7. hm = 5×(1.768²/(2×9.80665)) ≈ 0.80 m.
8. Total head loss ≈ 3.74 m.
9. ΔP ≈ 997×9.80665×3.74/100000 ≈ 0.365 bar.

مقادیر مثال تقریبی‌اند؛ اختلاف جزئی با خروجی برنامه به حل عددی f و خواص سیال بستگی دارد. افت فشار فقط برای طول و فیتینگ‌های واردشده معتبر است؛ افت تجهیزات فرایندی در این برنامه جداگانه مدل نشده است.

## 7. Fittings and K values | فیتینگ‌ها و ضرایب K
The user selects a fitting record and enters its quantity. The program adds K×quantity to the running total. Minor loss is then calculated using the reference pipe velocity. Real K depends on fitting geometry, diameter ratio, opening, flow path and Reynolds number; use manufacturer or validated references for critical design.

کاربر نوع فیتینگ و تعداد را انتخاب می‌کند و برنامه Kها را جمع می‌زند. افت موضعی با سرعت لوله مرجع محاسبه می‌شود. K واقعی به هندسه، نسبت قطرها، میزان بازشدگی شیر، مسیر جریان و Reynolds وابسته است؛ برای طراحی حساس از داده معتبر استفاده کنید.

## 8. EC and temperature | EC و دما
EC is entered as a value already temperature-compensated to 25°C. Operating temperature is a separate input used for the water-property estimate. The internal TDS factor is 0.65; it is not a user-entered conversion parameter. Generic mode does not invent ion concentrations. Natural seawater mode reports assumed ion ratios only.

EC باید از قبل به ۲۵ درجه جبران شده باشد. دمای کارکرد ورودی مستقلی است و در تخمین چگالی و ویسکوزیته استفاده می‌شود. ضریب TDS درون برنامه ۰٫۶۵ است و ورودی کاربر نیست. حالت عمومی یون‌های منفرد را حدس نمی‌زند؛ حالت آب دریا نسبت‌های فرضی را گزارش می‌کند.

## 9. Result interpretation | تفسیر نتایج
- Velocity: average cross-sectional velocity | سرعت متوسط مقطع
- Reynolds and flow regime: flow classification | عدد Reynolds و طبقه‌بندی رژیم
- Darcy friction factor: dimensionless major-loss coefficient | ضریب بی‌بعد افت طولی
- Major head loss: straight-pipe friction loss | افت طولی
- Minor head loss: fitting/valve loss | افت موضعی
- Total head loss: sum of major and minor | مجموع افت‌ها
- Pressure drop: equivalent pressure difference for supplied density | افت فشار معادل با چگالی ورودی

## 10. Limitations and design checks | محدودیت‌ها و کنترل طراحی
The calculation is steady-state and single-path. It does not include elevation, pump TDH, branched networks, multiple reference diameters, equipment pressure drops, pump curves, NPSH or water hammer. The EC model is approximate, especially for concentrated brines. Confirm actual internal diameter, pipe condition, roughness, fitting K, fluid properties and operating flow before using results for design or procurement.

محاسبه پایا و تک‌مسیره است و ارتفاع، TDH، شبکه شاخه‌دار، چند قطر، افت تجهیزات، منحنی پمپ، NPSH یا ضربه قوچ را شامل نمی‌شود. مدل EC به‌ویژه برای شورابه غلیظ تقریبی است. پیش از استفاده طراحی، قطر واقعی، وضعیت لوله، زبری، K، خواص سیال و دبی را کنترل کنید.

## 11. Tests | تست‌ها
```bash
python -m unittest discover -s tests -v
```
