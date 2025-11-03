from datetime import datetime, timedelta
import math
import time
import sys

# Global flag for Skyfield availability
try:
    from skyfield.api import load, Topos
    from skyfield import almanac
    HAS_SKYFIELD = True
except ImportError:
    HAS_SKYFIELD = False

def progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """
    Create a progress bar in the terminal
    """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '░' * (length - filled_length)
    
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    
    if iteration == total:
        print()

class PersianCalendar:
    """Convert Gregorian dates to Persian calendar dates"""
    
    @staticmethod
    def gregorian_to_persian(gregorian_date):
        """Convert Gregorian date to Persian date"""
        g_year = gregorian_date.year
        g_month = gregorian_date.month
        g_day = gregorian_date.day
        
        # Persian year starts at Nowruz (around March 20-21)
        # If date is on or after Nowruz of current Gregorian year, Persian year = Gregorian year - 621
        # If date is before Nowruz of current Gregorian year, Persian year = Gregorian year - 622
        
        # Approximate Nowruz date (March 20-21)
        nowruz_date = PersianCalendar._approximate_nowruz(g_year)
        current_date = gregorian_date.date()
        
        if current_date >= nowruz_date:
            persian_year = g_year - 621
            start_date = nowruz_date
        else:
            persian_year = g_year - 622
            start_date = PersianCalendar._approximate_nowruz(g_year - 1)
        
        # Calculate days since Nowruz
        day_diff = (current_date - start_date).days
        
        # Persian month lengths
        month_lengths = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
        
        # Handle leap year (Esfand has 30 days in leap years)
        if PersianCalendar._is_persian_leap_year(persian_year):
            month_lengths[11] = 30
        
        # Find correct month and day
        day_counter = day_diff
        persian_month = 1
        persian_day = 1
        
        for month_idx, days_in_month in enumerate(month_lengths, 1):
            if day_counter < days_in_month:
                persian_month = month_idx
                persian_day = day_counter + 1
                break
            day_counter -= days_in_month
        
        return persian_year, persian_month, persian_day
    
    @staticmethod
    def _approximate_nowruz(gregorian_year):
        """Approximate Nowruz date for conversion purposes"""
        # Most Nowruz dates are March 20 or 21
        day = 20 if (gregorian_year % 4) == 0 else 21
        return datetime(gregorian_year, 3, day).date()
    
    @staticmethod
    def _is_persian_leap_year(persian_year):
        """Check if a Persian year is a leap year"""
        # Persian leap year: (year + 38) mod 2820 < 682
        return ((persian_year + 38) % 2820) < 682
    
    @staticmethod
    def get_persian_month_name(month):
        """Get Persian month names"""
        months = {
            1: "فروردین", 2: "اردیبهشت", 3: "خرداد", 
            4: "تیر", 5: "مرداد", 6: "شهریور",
            7: "مهر", 8: "آبان", 9: "آذر",
            10: "دی", 11: "بهمن", 12: "اسفند"
        }
        return months.get(month, "")
    
    @staticmethod
    def format_persian_datetime(gregorian_datetime):
        """Format datetime in Persian style"""
        year, month, day = PersianCalendar.gregorian_to_persian(gregorian_datetime)
        month_name = PersianCalendar.get_persian_month_name(month)
        
        time_str = gregorian_datetime.strftime("%H:%M:%S")
        
        return f"{day} {month_name} {year} - {time_str}"

class NowruzPredictor:
    def __init__(self):
        # Use Tehran coordinates for accurate calculation
        self.lat = 35.6892  # Tehran latitude
        self.lon = 51.3890  # Tehran longitude
        
        if HAS_SKYFIELD:
            try:
                self.ts = load.timescale()
                self.eph = load('de421.bsp')
                self.earth = self.eph['earth']
                self.sun = self.eph['sun']
                self.location = Topos(self.lat, self.lon)
                self.skyfield_loaded = True
            except Exception as e:
                print(f"⚠️  Skyfield error: {e}")
                self.skyfield_loaded = False
        else:
            self.skyfield_loaded = False
    
    def calculate_exact_equinox(self, shamsi_year):
        """Calculate exact moment of vernal equinox for given Shamsi year"""
        # The Gregorian year when this Shamsi year starts
        gregorian_year = shamsi_year + 621
        
        print(f"\n⏳ Calculating لحظه تحویل سال for {shamsi_year}...")
        
        # Show progress bar
        steps = 4
        for i in range(steps + 1):
            if i == 0:
                progress_bar(i, steps, prefix='🌞 Calculating solar position', suffix='Starting...')
            elif i == 1:
                progress_bar(i, steps, prefix='🌞 Calculating solar position', suffix='Finding equinox...')
            elif i == 2:
                progress_bar(i, steps, prefix='🌞 Calculating solar position', suffix='Precise timing...')
            elif i == 3:
                progress_bar(i, steps, prefix='🌞 Calculating solar position', suffix='Converting...')
            elif i == 4:
                progress_bar(i, steps, prefix='🌞 Calculating solar position', suffix='Complete!')
            
            if i < steps:
                time.sleep(0.4)
        
        # Calculate exact vernal equinox moment
        if self.skyfield_loaded:
            equinox_time = self._calculate_with_skyfield(gregorian_year)
        else:
            equinox_time = self._calculate_with_fallback(gregorian_year)
        
        return equinox_time
    
    def _calculate_with_skyfield(self, gregorian_year):
        """Calculate exact equinox using Skyfield"""
        try:
            # Search around March 19-22 for vernal equinox
            t0 = self.ts.utc(gregorian_year, 3, 19)
            t1 = self.ts.utc(gregorian_year, 3, 22)
            t, y = almanac.find_discrete(t0, t1, almanac.seasons(self.eph))
            
            for time, season in zip(t, y):
                if season == 0:  # Vernal equinox (0 = March equinox)
                    return time.utc_datetime()
        except Exception as e:
            print(f"⚠️  Skyfield calculation failed: {e}")
        
        return self._calculate_with_fallback(gregorian_year)
    
    def _calculate_with_fallback(self, gregorian_year):
        """Calculate using astronomical formulas"""
        # More precise astronomical calculation
        y = gregorian_year - 2000
        
        # Astronomical formula for vernal equinox (Jean Meeus)
        jde = 2451623.80984 + 365242.37404 * y/1000 + 0.05169 * (y/1000)**2 - 0.00411 * (y/1000)**3 - 0.00057 * (y/1000)**4
        
        # Convert Julian Ephemeris Day to datetime
        jd = jde - 0.5
        z = int(jd)
        f = jd - z
        
        if z < 2299161:
            a = z
        else:
            alpha = int((z - 1867216.25) / 36524.25)
            a = z + 1 + alpha - int(alpha / 4)
        
        b = a + 1524
        c = int((b - 122.1) / 365.25)
        d = int(365.25 * c)
        e = int((b - d) / 30.6001)
        
        day = b - d - int(30.6001 * e) + f
        day_int = int(day)
        month = e - 1 if e < 14 else e - 13
        year_calc = c - 4716 if month > 2 else c - 4715
        
        # Convert fractional day to time
        fractional_day = day - day_int
        total_seconds = int(fractional_day * 86400)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        return datetime(year_calc, month, day_int, hours, minutes, seconds)
    
    def predict_nowruz(self, shamsi_year):
        """Predict لحظه تحویل سال for given Shamsi year"""
        # Calculate exact astronomical moment of vernal equinox
        exact_equinox = self.calculate_exact_equinox(shamsi_year)
        
        # This exact moment IS the لحظه تحویل سال
        # Now determine if Nowruz is same day or next day based on solar noon rule
        
        # For Iran: if equinox is before 12:00 Tehran time, Nowruz is same day
        # If after 12:00 Tehran time, Nowruz is next day
        tehran_time = exact_equinox + timedelta(hours=3, minutes=30)  # Convert UTC to Tehran time
        
        if tehran_time.hour >= 12:
            nowruz_date = exact_equinox.date() + timedelta(days=1)
            decision = "بعد از ظهر - فردا نوروز"
        else:
            nowruz_date = exact_equinox.date()
            decision = "قبل از ظهر - امروز نوروز"
        
        return {
            'shamsi_year': shamsi_year,
            'exact_equinox_utc': exact_equinox,
            'exact_equinox_tehran': tehran_time,
            'nowruz_date': nowruz_date,
            'decision': decision,
            'calculation_method': 'Skyfield (High Accuracy)' if self.skyfield_loaded else 'Astronomical Algorithm'
        }

def display_header():
    """Display beautiful header"""
    print("=" * 70)
    print("🎊 NOWRUZ PREDICTION TOOL - محاسبه لحظه تحویل سال")
    print("📅 Persian Calendar Astronomical Calculator")
    print("=" * 70)
    print()

def display_installation_info():
    """Show installation information if needed"""
    if not HAS_SKYFIELD:
        print("⚠️  For better accuracy, install Skyfield:")
        print("    pip install skyfield")
        print("    (Using astronomical algorithms)")
        print()
    else:
        print("✅ Skyfield installed - Using high accuracy calculations")
        print()

def get_user_input():
    """Get Shamsi year from user"""
    while True:
        try:
            print("🔢 Enter the Persian (Shamsi) year you want to predict:")
            print("   Example: 1403, 1404, 1405, etc.")
            shamsi_year = int(input("   📅 Year: "))
            
            if 1300 <= shamsi_year <= 1500:
                return shamsi_year
            else:
                print("   ❌ Please enter a year between 1300 and 1500")
        except ValueError:
            print("   ❌ Please enter a valid number")

def display_results(result):
    """Display results in a beautiful format"""
    print("\n" + "=" * 70)
    print("🎉 NOWRUZ PREDICTION RESULTS - نتایج محاسبه")
    print("=" * 70)
    
    # لحظه تحویل سال (Exact moment of vernal equinox)
    equinox_utc = result['exact_equinox_utc']
    equinox_tehran = result['exact_equinox_tehran']
    
    print(f"\n🌞 لحظه تحویل سال (Exact Vernal Equinox):")
    print(f"   🕐 UTC Time:    {equinox_utc.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   🕐 Tehran Time: {equinox_tehran.strftime('%Y-%m-%d %H:%M:%S')} (UTC+3:30)")
    print(f"   📅 Persian:     {PersianCalendar.format_persian_datetime(equinox_tehran)}")
    print(f"   📝 Decision:    {result['decision']}")
    
    # Nowruz date
    nowruz_date = result['nowruz_date']
    nowruz_persian = PersianCalendar.format_persian_datetime(
        datetime(nowruz_date.year, nowruz_date.month, nowruz_date.day, 0, 0, 0)
    )
    
    print(f"\n🎊 نوروز (Nowruz) - 1st Farvardin:")
    print(f"   📅 Gregorian: {nowruz_date.strftime('%Y-%m-%d')}")
    print(f"   📅 Persian:   {nowruz_persian.split(' - ')[0]}")
    print(f"   🌍 For all of Iran (سراسر ایران)")
    
    print(f"\n📊 TECHNICAL DETAILS:")
    print(f"   🔢 Persian Year: {result['shamsi_year']}")
    print(f"   🔢 Gregorian Year: {result['shamsi_year'] + 621}")
    print(f"   🕰️  Tehran Time: {equinox_tehran.strftime('%H:%M:%S')}")
    print(f"   🎯 Calculation: {result['calculation_method']}")
    
    # International times
    print(f"\n🌐 INTERNATIONAL TIMES:")
    ny_time = equinox_utc - timedelta(hours=4)  # EST
    london_time = equinox_utc + timedelta(hours=1)  # BST
    tokyo_time = equinox_utc + timedelta(hours=9)  # JST
    
    print(f"   🇺🇸 New York:  {ny_time.strftime('%Y-%m-%d %H:%M:%S')} (EST)")
    print(f"   🇪🇺 London:    {london_time.strftime('%Y-%m-%d %H:%M:%S')} (BST)")
    print(f"   🇯🇵 Tokyo:     {tokyo_time.strftime('%Y-%m-%d %H:%M:%S')} (JST)")
    print(f"   🇮🇷 Tehran:    {equinox_tehran.strftime('%Y-%m-%d %H:%M:%S')} (IRST)")

def main():
    """Main function"""
    display_header()
    display_installation_info()
    
    while True:
        # Get user input
        shamsi_year = get_user_input()
        
        # Calculate Nowruz
        predictor = NowruzPredictor()
        result = predictor.predict_nowruz(shamsi_year)
        
        # Display results
        display_results(result)
        
        # Ask if user wants to continue
        print("\n" + "=" * 70)
        continue_calc = input("\n🔍 Predict another year? (y/n): ").lower().strip()
        if continue_calc not in ['y', 'yes', 'بله', 'y']:
            break
    
    print("\n" + "=" * 70)
    print("🎊 نوروزتان پیروز! - Happy Nowruz!")
    print("=" * 70)

if __name__ == "__main__":
    main()