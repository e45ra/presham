# 🎊 Presham - Nowruz Predictor | پیش‌بینی‌کننده نوروز

<div align="center">
  <a href="#english-readme">
    <img src="https://img.shields.io/badge/Language-English-blue.svg" alt="English Language"/>
  </a>
  <a href="#persian-readme">
    <img src="https://img.shields.io/badge/زبان-فارسی-green.svg" alt="Persian Language"/>
  </a>
</div>

---

<div id="english-readme">

## 📝 English Documentation

### Overview
Presham is a high-precision astronomical calculator that predicts the exact moment of Nowruz (Persian New Year) based on the vernal equinox. It uses either the Skyfield library for high-accuracy calculations or falls back to astronomical algorithms when Skyfield is not available.

### Features
- 🎯 Precise calculation of the vernal equinox moment
- 🌍 Tehran time zone automatic adjustment
- 🗓️ Persian (Shamsi) to Gregorian calendar conversion
- 🌐 International time zone display
- 🎨 Beautiful terminal interface with progress bars
- 📊 Detailed technical information display

### Requirements
- Python 3.x

(Optional for skyfield) Create a virtual environment
```bash
python3 -m venv nowruz_env
source nowruz_env/bin/activate

```

- Required packages:
  ```bash
  pip install skyfield
  ```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/e45ra/presham.git
   cd presham
   ```

2. Install dependencies:
   ```bash
   pip install skyfield
   ```

### Usage
Run the script:
```bash
python nowruz_predictor.py
```

Follow the prompts to:
1. Enter the Persian (Shamsi) year you want to predict
2. View detailed calculations and results
3. Choose to calculate for another year or exit

### Output Information
The program displays:
- Exact moment of vernal equinox in UTC and Tehran time
- Persian calendar date and time
- Nowruz date determination
- Technical calculation details
- International time conversions

### Technical Details
- Uses Skyfield for high-precision astronomical calculations
- Fallback to Jean Meeus' astronomical algorithms when Skyfield is unavailable
- Accurate Persian calendar conversion algorithms
- Tehran coordinates (35.6892°N, 51.3890°E) for precise calculations

The calculation is very accurate — maybe it’s off by 2 seconds.
this project is open source and anyone can use this without naming the project and algorithems to them selfs
</div>

---

<div id="persian-readme" dir="rtl">

## 📝 مستندات فارسی

### نمای کلی
پرشام یک محاسبه‌گر نجومی با دقت بالا است که لحظه دقیق تحویل سال نو (نوروز) را بر اساس اعتدال بهاری محاسبه می‌کند. این برنامه از کتابخانه Skyfield برای محاسبات با دقت بالا استفاده می‌کند و در صورت عدم دسترسی به آن، از الگوریتم‌های نجومی استفاده می‌کند.

### ویژگی‌ها
- 🎯 محاسبه دقیق لحظه اعتدال بهاری
- 🌍 تنظیم خودکار منطقه زمانی تهران
- 🗓️ تبدیل تقویم شمسی به میلادی
- 🌐 نمایش منطقه‌های زمانی بین‌المللی
- 🎨 رابط کاربری زیبا در ترمینال با نوار پیشرفت
- 📊 نمایش اطلاعات فنی دقیق

### پیش‌نیازها
- پایتون نسخه ۳
- بسته‌های مورد نیاز:
  ```bash
  pip install skyfield
  ```

### نصب
۱. کلون کردن مخزن:
   ```bash
   git clone https://github.com/e45ra/presham.git
   cd presham
   ```

۲. نصب وابستگی‌ها:
   ```bash
   pip install skyfield
   ```

### نحوه استفاده
اجرای اسکریپت:
```bash
python nowruz_predictor.py
```

مراحل استفاده:
۱. وارد کردن سال شمسی مورد نظر برای پیش‌بینی
۲. مشاهده محاسبات و نتایج دقیق
۳. انتخاب محاسبه برای سال دیگر یا خروج

### اطلاعات خروجی
برنامه موارد زیر را نمایش می‌دهد:
- لحظه دقیق اعتدال بهاری به وقت جهانی و تهران
- تاریخ و زمان به تقویم شمسی
- تعیین روز نوروز
- جزئیات فنی محاسبات
- تبدیل‌های زمانی بین‌المللی

### جزئیات فنی
- استفاده از Skyfield برای محاسبات نجومی با دقت بالا
- استفاده از الگوریتم‌های نجومی Jean Meeus در صورت عدم دسترسی به Skyfield
- الگوریتم‌های دقیق تبدیل تقویم شمسی
- استفاده از مختصات تهران (عرض جغرافیایی ۳۵.۶۸۹۲ درجه شمالی، طول جغرافیایی ۵۱.۳۸۹۰ درجه شرقی) برای محاسبات دقیق

</div>
