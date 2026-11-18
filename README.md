# Pipe Pressure Loss Calculator

## فارسی

### معرفی
این برنامه افت اصطکاکی طولی و افت موضعی اتصالات را برای یک بخش لوله با قطر داخلی و دبی مشخص محاسبه می‌کند. خروجی شامل سرعت، عدد رینولدز، رژیم جریان، ضریب اصطکاک Darcy، افت هد و افت فشار معادل است.

### قابلیت‌ها
- انتخاب جنس و سایز لوله و استفاده از زبری مرجع
- محاسبه افت طولی Darcy–Weisbach
- محاسبه افت اتصالات با ضرایب K
- نمایش سرعت، Reynolds و رژیم جریان

### اجرا
```bash
git clone https://github.com/alizarei-eng/pipe-pressure-loss-calculator.git
cd pipe-pressure-loss-calculator
python main.py
python -m unittest discover -s tests -v
```

### روابط
`V=Q/A`
`Re=VD/ν`
`hf=f(L/D)(V²/2g)`
`hm=ΣK(V²/2g)`
`ΔP=ρg(hf+hm)`

### مثال
برای Q=50 m³/h، قطر داخلی ۱۰۰ mm، طول ۱۰۰ m، زبری ۰٫۰۰۱۵ mm و مجموع K برابر ۵، سرعت حدود ۱٫۷۶۸ m/s است. با ضریب Darcy تقریبی ۰٫۰۱۵۸، افت طولی حدود ۲٫۵۲ m، افت موضعی حدود ۰٫۸۰ m و افت کل حدود ۳٫۳۱ m خواهد بود. افت فشار معادل حدود ۰٫۳۲ bar است.

### موارد کاربرد
محاسبه افت یک بخش لوله مستقیم با قطر یکنواخت، مقایسه قطر و زبری و بررسی سهم اتصالات در افت فشار.

### محدودیت‌ها
هر محاسبه یک قطر و یک دبی دارد. بخش‌های چندقطری و شبکه‌های شاخه‌دار خودکار حل نمی‌شوند. تمام ضرایب K با سرعت قطر مرجع محاسبه می‌شوند؛ اتصالات روی قطر دیگر باید جداگانه محاسبه شوند. هد ارتفاعی، افت تجهیزات، TDH، منحنی پمپ، NPSH و ضربه قوچ در این برنامه وجود ندارند. خواص مبتنی بر EC و ضرایب K تقریبی‌اند.

---

## English

### Overview
This application calculates straight-pipe friction loss and fitting minor loss for one pipe section with a defined internal diameter and flow rate. Outputs include velocity, Reynolds number, flow regime, Darcy friction factor, head loss and equivalent pressure drop.

### Features
- Pipe material and size inputs with reference roughness
- Darcy–Weisbach major-loss calculation
- Fitting losses using K coefficients
- Velocity, Reynolds number and flow-regime reporting

### Run
```bash
git clone https://github.com/alizarei-eng/pipe-pressure-loss-calculator.git
cd pipe-pressure-loss-calculator
python main.py
python -m unittest discover -s tests -v
```

### Equations
`V=Q/A`
`Re=VD/ν`
`hf=f(L/D)(V²/2g)`
`hm=ΣK(V²/2g)`
`ΔP=ρg(hf+hm)`

### Worked example
For Q=50 m³/h, ID=100 mm, L=100 m, roughness=0.0015 mm and total K=5, velocity is approximately 1.768 m/s. With an illustrative Darcy factor of 0.0158, major loss is about 2.52 m, minor loss about 0.80 m and total loss about 3.31 m. Equivalent pressure drop is about 0.32 bar.

### Suitable applications
Loss calculation for one straight, uniform-diameter section, comparison of diameters and roughness values, and evaluation of fitting contribution.

### Limitations
Each calculation uses one diameter and one flow rate. Multi-diameter sections and branched networks are not solved automatically. All K coefficients use the reference-diameter velocity; fittings on another diameter must be calculated separately. Elevation head, equipment losses, TDH, pump curves, NPSH and water hammer are not included. EC-based properties and K coefficients are approximate.
