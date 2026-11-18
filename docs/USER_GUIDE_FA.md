# Pipe Pressure Loss Calculator — User Guide | راهنمای استفاده

## 1. Purpose | هدف
**EN:** This command-line program calculates steady-state major friction loss and minor fitting loss for one pipe section represented by one internal diameter and one flow rate. It reports velocity, Reynolds number, flow regime, Darcy friction factor, head loss and equivalent pressure drop.

**FA:** این برنامه خط فرمان، افت طولی و موضعی پایا را برای یک بخش لوله با یک قطر داخلی و یک دبی محاسبه می‌کند. سرعت، عدد رینولدز، رژیم جریان، ضریب اصطکاک Darcy، افت هد و افت فشار معادل گزارش می‌شوند.

## 2. Run | اجرا
```bash
python main.py
python -m unittest discover -s tests -v
```

## 3. Input sequence | ترتیب ورود اطلاعات
1. **Fluid profile | پروفایل سیال:** choose generic water/groundwater/brackish water, or the assumed natural-seawater ionic-ratio profile. | آب عمومی/زیرزمینی/لب‌شور یا پروفایل فرضی نسبت‌های یونی آب دریای طبیعی را انتخاب کنید.
2. **EC | هدایت الکتریکی:** enter EC in mS/cm already compensated to 25°C. | EC را بر حسب mS/cm و از قبل جبران‌شده تا ۲۵ درجه وارد کنید.
3. **Operating temperature | دمای کارکرد:** enter actual water temperature separately in °C. | دمای واقعی آب را جداگانه بر حسب درجه سانتی‌گراد وارد کنید.
4. **Pipe material | جنس لوله:** select a listed material. | جنس را از فهرست انتخاب کنید.
5. **Pipe size | سایز لوله:** for HDPE select grade → SDR → OD; the nominal ID is calculated from the database wall thickness. For other listed materials enter ID in mm. | برای HDPE گرید ← SDR ← OD را انتخاب کنید؛ ID اسمی از ضخامت بانک محاسبه می‌شود. برای سایر مواد قطر داخلی را بر حسب میلی‌متر وارد کنید.
6. **Roughness | زبری:** accept the material reference value or override it; if the material has no default, enter roughness in mm. | مقدار مرجع جنس را بپذیرید یا اصلاح کنید؛ اگر مقدار پیش‌فرض موجود نیست زبری را بر حسب میلی‌متر وارد کنید.
7. **Flow and length | دبی و طول:** enter flow in m³/h and straight length in m. | دبی را بر حسب m³/h و طول مستقیم را بر حسب متر وارد کنید.
8. **Fittings | اتصالات:** select fitting types and quantities; enter 0 to finish. | نوع و تعداد اتصالات را وارد کنید؛ صفر برای پایان.
9. **Review results | بررسی خروجی:** inspect major/minor/total head loss and equivalent pressure drop. | افت طولی، موضعی، کل و افت فشار معادل را بررسی کنید.

## 4. Equations | روابط
`Q(m³/s)=Q(m³/h)/3600`
`A=πD²/4; V=Q/A; Re=VD/ν`
`hf=f(L/D)(V²/2g)`
`hm=ΣK(V²/2g)`
`ΔP=ρg(hf+hm)`

The friction factor is Darcy, not Fanning. Laminar flow uses f=64/Re; turbulent flow uses iterative Colebrook-White. The 2300–4000 transition range is flagged as uncertain.

ضریب اصطکاک از نوع Darcy است، نه Fanning. برای جریان آرام f=64/Re و برای جریان آشفته حل تکراری Colebrook-White استفاده می‌شود. محدوده گذار ۲۳۰۰ تا ۴۰۰۰ با هشدار عدم‌قطعیت مشخص می‌شود.

## 5. Worked example | مثال
Assume Q=50 m³/h, ID=100 mm, L=100 m, ε=0.0015 mm, total K=5, water at 25°C with ρ≈997 kg/m³ and ν≈0.89×10⁻⁶ m²/s.

- Q=50/3600=0.013889 m³/s
- A=π(0.1)²/4=0.007854 m²
- V≈1.768 m/s
- Re≈1.99×10⁵ (turbulent)
- With a Darcy factor near 0.018, major loss is about 2.86 m
- Minor loss for K=5 is about 0.80 m
- Total head loss is about 3.66 m; pressure drop is about 0.36 bar.

فرض مثال آموزشی است؛ خروجی دقیق به ضریب اصطکاک محاسبه‌شده و خواص سیال بستگی دارد. اگر K=5 متعلق به اتصالات همین قطر مرجع نباشد، باید افت آن‌ها جداگانه محاسبه شود.

## 6. Suitable applications | موارد کاربرد مناسب
- **EN:** One uniform-diameter pipe section at a known steady flow; preliminary friction and fitting-loss checks; comparison of alternative diameters, lengths or roughness assumptions.
- **FA:** یک بخش لوله با قطر یکنواخت و دبی پایا؛ کنترل اولیه افت طولی و اتصالات؛ مقایسه قطر، طول یا زبری‌های مختلف.

## 7. Limitations and when to use another method | محدودیت‌ها و زمان استفاده از روش دیگر
- **EN:** One calculation uses one internal diameter and one flow rate. Different-diameter sections are not assembled automatically. Calculate each uniform section separately and sum the losses.
- **FA:** هر محاسبه یک قطر داخلی و یک دبی دارد. بخش‌های با قطر متفاوت خودکار به هم متصل نمی‌شوند؛ هر بخش یکنواخت را جداگانه محاسبه و افت‌ها را جمع کنید.
- **EN:** All selected K values use the same reference-pipe velocity. If fittings are installed on different diameters, group and calculate them separately using the local velocity.
- **FA:** تمام Kهای انتخابی با سرعت لوله مرجع محاسبه می‌شوند. اگر اتصالات روی قطرهای متفاوت‌اند، آن‌ها را بر اساس سرعت محلی جداگانه محاسبه کنید.
- **EN:** No branched network, flow distribution, elevation head, equipment pressure drop, pump TDH, pump curve, NPSH, water hammer or transient analysis.
- **FA:** شبکه شاخه‌دار، توزیع دبی، هد ارتفاعی، افت تجهیزات، TDH پمپ، منحنی پمپ، NPSH، ضربه قوچ یا تحلیل گذرا وجود ندارد.
- **EN:** EC-based density/viscosity and default roughness are screening values. Use laboratory properties and verified roughness/K data for concentrated brine or critical design.
- **FA:** چگالی/ویسکوزیته مبتنی بر EC و زبری پیش‌فرض مقادیر غربالگری‌اند. برای شورابه غلیظ یا طراحی حساس از خواص آزمایشگاهی و داده معتبر زبری/K استفاده کنید.

## 8. Output interpretation | تفسیر خروجی
- Velocity: average velocity in the selected internal diameter. | سرعت متوسط در قطر داخلی انتخابی.
- Reynolds/flow regime: laminar, transitional or turbulent classification. | طبقه‌بندی جریان آرام، گذار یا آشفته.
- Major head loss: straight-pipe friction. | افت اصطکاکی طول مستقیم.
- Minor head loss: selected fitting K losses. | افت اتصالات انتخابی.
- Total head loss: sum of major and minor loss. | مجموع افت طولی و موضعی.
- Pressure drop: pressure equivalent based on estimated/supplied density. | افت فشار معادل بر اساس چگالی تخمینی/ورودی.

The result is the loss for the entered section only, not automatically the complete system TDH.
نتیجه مربوط به بخش واردشده است و به‌صورت خودکار TDH کل سیستم نیست.
