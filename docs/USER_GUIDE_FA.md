# راهنمای کاربر محاسبه‌گر افت فشار

## بخش فارسی

### ترتیب ورود اطلاعات
۱. پروفایل سیال را انتخاب کنید.
۲. EC جبران‌شده تا ۲۵°C و دمای واقعی آب را وارد کنید.
۳. جنس و سایز لوله را تعیین کنید؛ برای HDPE گرید، SDR و OD انتخاب می‌شود و ID از بانک محاسبه می‌شود.
۴. زبری مرجع را بررسی کنید.
۵. دبی و طول مستقیم را وارد کنید.
۶. نوع و تعداد اتصالات را مشخص کنید.
۷. افت طولی، موضعی، کل و افت فشار معادل را بخوانید.

### روابط
`Q(m³/s)=Q(m³/h)/3600`
`V=Q/A`
`Re=VD/ν`
`hf=f(L/D)(V²/2g)`
`hm=ΣK(V²/2g)`

### اجرا
```bash
python main.py
python -m unittest discover -s tests -v
```

### محدودیت
نتیجه مربوط به همان بخش لوله است. برای خط چندقطری هر بخش را جدا محاسبه کنید. برای شبکه شاخه‌دار از حل‌کننده شبکه استفاده کنید.

## English Section

### Input workflow
1. Select the fluid profile.
2. Enter EC compensated to 25°C and actual water temperature.
3. Select pipe material and size; for HDPE choose grade, SDR and OD, and ID is calculated from the database.
4. Review the reference roughness.
5. Enter flow rate and straight length.
6. Select fitting types and quantities.
7. Review major, minor and total head loss and equivalent pressure drop.

### Equations
`Q(m³/s)=Q(m³/h)/3600`
`V=Q/A`
`Re=VD/ν`
`hf=f(L/D)(V²/2g)`
`hm=ΣK(V²/2g)`

### Run
```bash
python main.py
python -m unittest discover -s tests -v
```

### Limitation
The result applies to the entered pipe section only. Calculate each segment separately for a multi-diameter line. Use a network solver for branched systems.
