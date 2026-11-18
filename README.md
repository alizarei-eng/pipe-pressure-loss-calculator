# Pipe Pressure Loss Calculator | محاسبه‌گر افت فشار لوله

**FA:** ابزار تعاملی Python برای محاسبه افت هد طولی Darcy–Weisbach، افت موضعی مبتنی بر K، سرعت، عدد Reynolds، رژیم جریان و افت فشار معادل.

**EN:** An interactive Python tool for Darcy–Weisbach major losses, K-based minor losses, flow velocity, Reynolds number, flow regime and equivalent pressure drop.

## Features | قابلیت‌ها
- HDPE grade/SDR/OD selection with nominal ID lookup | انتخاب گرید، SDR و OD لوله HDPE و محاسبه ID اسمی
- Other materials use entered internal diameter | برای سایر مواد ورود قطر داخلی
- Material-based roughness lookup | بارگذاری زبری بر اساس جنس لوله
- EC-based screening estimates for fluid properties | تخمین غربالگری خواص سیال از EC
- Darcy friction factor and flow regime | ضریب اصطکاک Darcy و رژیم جریان
- Major and minor head loss separately | نمایش جداگانه افت طولی و موضعی
- Pressure drop in bar | افت فشار معادل بر حسب bar

## Installation and run | نصب و اجرا
```bash
git clone https://github.com/alizarei-eng/pipe-pressure-loss-calculator.git
cd pipe-pressure-loss-calculator
python main.py
python -m unittest discover -s tests -v
```

## Input workflow | ترتیب ورود اطلاعات
1. Select generic water or natural-seawater composition profile. | انتخاب پروفایل آب عمومی یا نسبت‌های آب دریای طبیعی
2. Enter EC in mS/cm, already temperature-compensated to 25°C, and actual water temperature in °C. | ورود EC جبران‌شده تا ۲۵ درجه و دمای واقعی آب به‌صورت مستقل
3. Select pipe material. | انتخاب جنس لوله
4. For HDPE, select grade → SDR → OD; nominal ID is read/calculated. For other materials, enter ID in mm. | برای HDPE گرید ← SDR ← OD؛ برای سایر مواد قطر داخلی وارد می‌شود.
5. Accept database roughness or override it where offered. | پذیرش زبری بانک یا ورود مقدار جایگزین در صورت نیاز
6. Enter flow (m³/h) and straight length (m). | ورود دبی و طول مستقیم
7. Add fitting types and quantities; enter 0 to finish. | انتخاب فیتینگ و تعداد؛ صفر برای پایان
8. Review head-loss and pressure-drop results. | بررسی نتایج افت هد و افت فشار

## Governing equations | روابط اصلی
`V = Q/A`; `Re = VD/ν`; `hf = f(L/D)(V²/2g)`; `hm = ΣK(V²/2g)`; `ΔP = ρg(hf+hm)`.

The friction factor is the Darcy factor. Laminar flow uses f=64/Re. Turbulent flow uses an iterative Colebrook-type solution; the transition range is flagged as uncertain.

ضریب اصطکاک از نوع Darcy است. در جریان آرام از f=64/Re استفاده می‌شود. در جریان آشفته رابطه Colebrook به‌صورت تکراری حل می‌شود. ناحیه گذار با هشدار عدم‌قطعیت مشخص می‌شود.

## Worked example | مثال عددی
Illustrative inputs: Q=50 m³/h, ID=100 mm, L=100 m, absolute roughness=0.007 mm, total K=5, water at about 25°C (ρ≈997 kg/m³, ν≈0.89×10⁻⁶ m²/s).

- Q = 50/3600 = 0.013889 m³/s
- Area = π(0.1)²/4 = 0.007854 m²
- Velocity ≈ 1.768 m/s
- Reynolds ≈ 1.99×10⁵ (turbulent)
- With a Darcy friction factor around 0.018–0.019, major loss ≈ 2.9–3.0 m
- Minor loss = 5×(1.768²/(2×9.80665)) ≈ 0.80 m
- Total head loss ≈ 3.7–3.8 m
- Pressure drop ≈ 0.36 bar

این مثال صرفاً آموزشی است. مقدار دقیق ضریب اصطکاک و افت خروجی برنامه به خواص سیال و محاسبه عددی الگوریتم وابسته است. برای خط واقعی، ID واقعی، زبری متناسب با وضعیت لوله و K متناظر با هندسه واقعی را وارد کنید.

## Fluid-property model | مدل خواص سیال
TDS ≈ EC(µS/cm) × 0.65. EC must already be compensated to 25°C. Density and viscosity are screening correlations, not a validated brine equation of state. The natural-seawater profile scales assumed standard ion ratios; it does not infer ions from EC.

TDS با ضریب پیش‌فرض ۰٫۶۵ از EC تخمین زده می‌شود. EC باید از قبل در ۲۵°C جبران شده باشد. چگالی و ویسکوزیته تخمینی‌اند و برای شورابه غلیظ مدل معتبر خواص محسوب نمی‌شوند. پروفایل آب دریا نسبت‌های یونی استاندارد را فرض می‌کند و غلظت واقعی یون‌ها را از EC استخراج نمی‌کند.

## Limitations | محدودیت‌ها
Steady-state, single flow path and one reference diameter per calculation. No static elevation, pump TDH, branched network, pump curve, NPSH or water-hammer analysis. Fitting K values are approximate references and all selected K values use the same reference pipe velocity.

محاسبه پایا، تک‌مسیره و با یک قطر مرجع است. اختلاف ارتفاع، TDH پمپ، شبکه شاخه‌دار، منحنی پمپ، NPSH و ضربه قوچ در این مخزن محاسبه نمی‌شوند. ضرایب K تقریبی‌اند و همه با سرعت لوله مرجع همین محاسبه ارزیابی می‌شوند.

See [the bilingual engineering guide](docs/ENGINEERING_GUIDE_FA_EN.md) for the full explanation and worked example.
