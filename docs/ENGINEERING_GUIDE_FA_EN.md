# راهنمای مهندسی محاسبه‌گر افت فشار

## بخش فارسی

این برنامه افت طولی و موضعی یک بخش لوله با قطر داخلی ثابت و دبی پایا را محاسبه می‌کند.

### روابط
`V=Q/A`
`Re=VD/ν`
`hf=f(L/D)(V²/2g)`
`hm=ΣK(V²/2g)`
`ΔP=ρg(hf+hm)`

ضریب اصطکاک از نوع Darcy است. برای جریان آرام از رابطه 64/Re و برای جریان آشفته از رابطه Colebrook-White استفاده می‌شود.

### مثال
برای Q=50 m³/h، قطر داخلی ۱۰۰ mm، طول ۱۰۰ m، زبری ۰٫۰۰۱۵ mm و مجموع K برابر ۵، سرعت حدود ۱٫۷۶۸ m/s است. با f≈0.0158، افت طولی حدود ۲٫۵۲ m و افت موضعی حدود ۰٫۸۰ m است؛ افت کل حدود ۳٫۳۱ m و افت فشار حدود ۰٫۳۲ bar خواهد بود.

### کاربردها
محاسبه افت یک بخش مستقیم، مقایسه قطر و زبری و بررسی سهم اتصالات در افت فشار.

### محدودیت‌ها
هر محاسبه یک قطر و دبی دارد. اتصالات با قطر متفاوت باید جداگانه و با سرعت محلی محاسبه شوند. شبکه شاخه‌دار، هد ارتفاعی، افت تجهیزات، TDH، منحنی پمپ، NPSH و ضربه قوچ پشتیبانی نمی‌شوند.

## English Section

This application calculates major and minor losses for one steady-flow pipe section with a single internal diameter.

### Equations
`V=Q/A`
`Re=VD/ν`
`hf=f(L/D)(V²/2g)`
`hm=ΣK(V²/2g)`
`ΔP=ρg(hf+hm)`

The friction factor is Darcy. Laminar flow uses 64/Re and turbulent flow uses the Colebrook-White equation.

### Worked example
For Q=50 m³/h, ID=100 mm, L=100 m, roughness=0.0015 mm and total K=5, velocity is about 1.768 m/s. With f≈0.0158, major loss is about 2.52 m and minor loss about 0.80 m; total loss is about 3.31 m and pressure drop about 0.32 bar.

### Suitable applications
Loss calculation for one straight section, diameter and roughness comparison, and evaluation of fitting contribution.

### Limitations
Each calculation uses one diameter and flow rate. Fittings on different diameters must be calculated separately using local velocity. Branched networks, elevation head, equipment losses, TDH, pump curves, NPSH and water hammer are not supported.
