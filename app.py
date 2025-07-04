import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class WeatherDataAnalyzer:
    
    def __init__(self, days=1095):
        self.days = days
        self.dates = None
        self.temperature = None
        self.humidity = None
        self.precipitation = None
        self.wind_speed = None
        self.pressure = None
        
    def generate_weather_data(self):
        print("Generating synthetic weather data...")
        
        start_date = datetime(2021, 1, 1)
        self.dates = np.array([start_date + timedelta(days=i) for i in range(self.days)])
        
        day_of_year = np.array([date.timetuple().tm_yday for date in self.dates])
        
        seasonal_temp = 20 + 15 * np.sin(2 * np.pi * day_of_year / 365.25 - np.pi/2)
        daily_variation = np.random.normal(0, 5, self.days)
        for i in range(1, self.days):
            daily_variation[i] += 0.3 * daily_variation[i-1]
        
        self.temperature = seasonal_temp + daily_variation
        
        base_humidity = 70 - 0.5 * (self.temperature - 20)
        humidity_noise = np.random.normal(0, 10, self.days)
        self.humidity = np.clip(base_humidity + humidity_noise, 10, 100)
        
        precip_probability = (self.humidity - 30) / 70
        precip_probability = np.clip(precip_probability, 0, 1)
        
        rain_events = np.random.random(self.days) < (precip_probability * 0.3)
        self.precipitation = np.where(rain_events, 
                                    np.random.exponential(5, self.days), 
                                    0)
        
        base_wind = 8 + 0.3 * self.precipitation + np.random.normal(0, 3, self.days)
        self.wind_speed = np.clip(base_wind, 0, 50)
        
        seasonal_pressure = 1013 + 10 * np.sin(2 * np.pi * day_of_year / 365.25)
        pressure_variation = np.random.normal(0, 8, self.days)
        pressure_drop = -5 * (self.precipitation > 0)
        self.pressure = seasonal_pressure + pressure_variation + pressure_drop
        
        print(f"Generated {self.days} days of weather data")
        
    def basic_statistics(self):
        print("\n" + "="*50)
        print("BASIC WEATHER STATISTICS")
        print("="*50)
        
        variables = {
            'Temperature (°C)': self.temperature,
            'Humidity (%)': self.humidity,
            'Precipitation (mm)': self.precipitation,
            'Wind Speed (km/h)': self.wind_speed,
            'Pressure (hPa)': self.pressure
        }
        
        for name, data in variables.items():
            print(f"\n{name}:")
            print(f"  Mean: {np.mean(data):.2f}")
            print(f"  Median: {np.median(data):.2f}")
            print(f"  Std Dev: {np.std(data):.2f}")
            print(f"  Min: {np.min(data):.2f}")
            print(f"  Max: {np.max(data):.2f}")
            print(f"  Range: {np.ptp(data):.2f}")
            
    def seasonal_analysis(self):
        print("\n" + "="*50)
        print("SEASONAL ANALYSIS")
        print("="*50)
        
        months = np.array([date.month for date in self.dates])
        
        seasons = {
            'Winter': [12, 1, 2],
            'Spring': [3, 4, 5],
            'Summer': [6, 7, 8],
            'Fall': [9, 10, 11]
        }
        
        print("\nSeasonal Temperature Averages:")
        for season, season_months in seasons.items():
            season_mask = np.isin(months, season_months)
            season_temps = self.temperature[season_mask]
            
            avg_temp = np.mean(season_temps)
            print(f"  {season}: {avg_temp:.1f}°C")
            
        print("\nMonthly Precipitation Totals:")
        for month in range(1, 13):
            month_mask = months == month
            month_precip = np.sum(self.precipitation[month_mask])
            month_name = datetime(2021, month, 1).strftime('%B')
            print(f"  {month_name}: {month_precip:.1f} mm")
            
    def correlation_analysis(self):
        print("\n" + "="*50)
        print("CORRELATION ANALYSIS")
        print("="*50)
        
        weather_data = np.column_stack([
            self.temperature,
            self.humidity,
            self.precipitation,
            self.wind_speed,
            self.pressure
        ])
        
        corr_matrix = np.corrcoef(weather_data.T)
        
        variables = ['Temperature', 'Humidity', 'Precipitation', 'Wind Speed', 'Pressure']
        
        print("\nCorrelation Matrix:")
        print("                ", end="")
        for var in variables:
            print(f"{var[:8]:>10}", end="")
        print()
        
        for i, var in enumerate(variables):
            print(f"{var[:15]:15}", end="")
            for j in range(len(variables)):
                print(f"{corr_matrix[i,j]:10.3f}", end="")
            print()
            
        print("\nStrong Correlations (|r| > 0.3):")
        for i in range(len(variables)):
            for j in range(i+1, len(variables)):
                corr = corr_matrix[i,j]
                if abs(corr) > 0.3:
                    print(f"  {variables[i]} vs {variables[j]}: {corr:.3f}")
                    
    def extreme_weather_analysis(self):
        print("\n" + "="*50)
        print("EXTREME WEATHER ANALYSIS")
        print("="*50)
        
        temp_hot = np.percentile(self.temperature, 95)
        temp_cold = np.percentile(self.temperature, 5)
        heavy_rain = np.percentile(self.precipitation[self.precipitation > 0], 90)
        high_wind = np.percentile(self.wind_speed, 95)
        
        print(f"\nExtreme Weather Thresholds:")
        print(f"  Hot days: > {temp_hot:.1f}°C")
        print(f"  Cold days: < {temp_cold:.1f}°C")
        print(f"  Heavy rain: > {heavy_rain:.1f} mm")
        print(f"  High wind: > {high_wind:.1f} km/h")
        
        hot_days = np.sum(self.temperature > temp_hot)
        cold_days = np.sum(self.temperature < temp_cold)
        heavy_rain_days = np.sum(self.precipitation > heavy_rain)
        high_wind_days = np.sum(self.wind_speed > high_wind)
        
        print(f"\nExtreme Event Counts:")
        print(f"  Hot days: {hot_days}")
        print(f"  Cold days: {cold_days}")
        print(f"  Heavy rain days: {heavy_rain_days}")
        print(f"  High wind days: {high_wind_days}")
        
        hot_day_mask = self.temperature > temp_hot
        heat_waves = self.find_consecutive_events(hot_day_mask, min_length=3)
        print(f"  Heat waves (3+ consecutive hot days): {heat_waves}")
        
        temp_normalized = np.abs((self.temperature - np.mean(self.temperature)) / np.std(self.temperature))
        wind_normalized = (self.wind_speed - np.mean(self.wind_speed)) / np.std(self.wind_speed)
        precip_normalized = (self.precipitation - np.mean(self.precipitation)) / np.std(self.precipitation)
        
        extreme_score = temp_normalized + wind_normalized + precip_normalized
        most_extreme_day = np.argmax(extreme_score)
        
        print(f"\nMost Extreme Weather Day:")
        print(f"  Date: {self.dates[most_extreme_day].strftime('%Y-%m-%d')}")
        print(f"  Temperature: {self.temperature[most_extreme_day]:.1f}°C")
        print(f"  Precipitation: {self.precipitation[most_extreme_day]:.1f} mm")
        print(f"  Wind Speed: {self.wind_speed[most_extreme_day]:.1f} km/h")
        
    def find_consecutive_events(self, boolean_array, min_length=3):
        changes = np.diff(np.concatenate(([False], boolean_array, [False])).astype(int))
        
        starts = np.where(changes == 1)[0]
        ends = np.where(changes == -1)[0]
        
        lengths = ends - starts
        return np.sum(lengths >= min_length)
        
    def moving_averages(self):
        print("\n" + "="*50)
        print("TREND ANALYSIS - MOVING AVERAGES")
        print("="*50)
        
        window_7 = 7
        window_30 = 30
        
        temp_7day = np.convolve(self.temperature, np.ones(window_7)/window_7, mode='valid')
        temp_30day = np.convolve(self.temperature, np.ones(window_30)/window_30, mode='valid')
        
        print(f"Temperature Trends:")
        print(f"  Original data range: {np.ptp(self.temperature):.2f}°C")
        print(f"  7-day average range: {np.ptp(temp_7day):.2f}°C")
        print(f"  30-day average range: {np.ptp(temp_30day):.2f}°C")
        print(f"  Smoothing effect: {((np.ptp(self.temperature) - np.ptp(temp_30day)) / np.ptp(self.temperature) * 100):.1f}% reduction in variability")
        
        days_array = np.arange(len(self.temperature))
        slope, intercept = np.polyfit(days_array, self.temperature, 1)
        
        print(f"\nOverall Temperature Trend:")
        print(f"  Slope: {slope:.4f}°C per day")
        print(f"  Annual change: {slope * 365.25:.2f}°C per year")
        
        trend_direction = "warming" if slope > 0 else "cooling"
        print(f"  Direction: {trend_direction}")
        
    def precipitation_patterns(self):
        print("\n" + "="*50)
        print("PRECIPITATION PATTERNS")
        print("="*50)
        
        rainy_days = np.sum(self.precipitation > 0)
        total_precipitation = np.sum(self.precipitation)
        avg_rainy_day = np.mean(self.precipitation[self.precipitation > 0])
        
        print(f"Precipitation Summary:")
        print(f"  Total rainy days: {rainy_days}")
        print(f"  Rainy day percentage: {rainy_days/self.days*100:.1f}%")
        print(f"  Total precipitation: {total_precipitation:.1f} mm")
        print(f"  Average per rainy day: {avg_rainy_day:.1f} mm")
        
        no_rain = self.precipitation == 0
        dry_spell_lengths = []
        
        current_spell = 0
        for day in no_rain:
            if day:
                current_spell += 1
            else:
                if current_spell > 0:
                    dry_spell_lengths.append(current_spell)
                current_spell = 0
        
        if current_spell > 0:
            dry_spell_lengths.append(current_spell)
            
        dry_spell_lengths = np.array(dry_spell_lengths)
        
        if len(dry_spell_lengths) > 0:
            print(f"\nDry Spell Analysis:")
            print(f"  Number of dry spells: {len(dry_spell_lengths)}")
            print(f"  Average dry spell: {np.mean(dry_spell_lengths):.1f} days")
            print(f"  Longest dry spell: {np.max(dry_spell_lengths)} days")
            print(f"  Shortest dry spell: {np.min(dry_spell_lengths)} days")
            
    def generate_report(self):
        print("\n" + "="*60)
        print("COMPREHENSIVE WEATHER ANALYSIS REPORT")
        print("="*60)
        
        self.basic_statistics()
        self.seasonal_analysis()
        self.correlation_analysis()
        self.extreme_weather_analysis()
        self.moving_averages()
        self.precipitation_patterns()
        
        print("\n" + "="*50)
        print("KEY INSIGHTS")
        print("="*50)
        
        temp_range = np.ptp(self.temperature)
        temp_mean = np.mean(self.temperature)
        print(f"1. Temperature varied by {temp_range:.1f}°C around a mean of {temp_mean:.1f}°C")
        
        wet_days = np.sum(self.precipitation > 0)
        print(f"2. It rained on {wet_days} days ({wet_days/self.days*100:.1f}% of the time)")
        
        temp_humid_corr = np.corrcoef(self.temperature, self.humidity)[0,1]
        print(f"3. Temperature and humidity correlation: {temp_humid_corr:.3f}")
        
        hot_threshold = np.percentile(self.temperature, 95)
        hot_days = np.sum(self.temperature > hot_threshold)
        print(f"4. Experienced {hot_days} extremely hot days (>{hot_threshold:.1f}°C)")
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)


def main():
    analyzer = WeatherDataAnalyzer(days=1095)
    
    analyzer.generate_weather_data()
    
    analyzer.generate_report()
    
    try:
        plt.figure(figsize=(12, 6))
        
        plt.subplot(2, 1, 1)
        plt.plot(analyzer.dates[:365], analyzer.temperature[:365])
        plt.title('Daily Temperature - First Year')
        plt.ylabel('Temperature (°C)')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 1, 2)
        plt.bar(analyzer.dates[:365], analyzer.precipitation[:365], alpha=0.7)
        plt.title('Daily Precipitation - First Year')
        plt.ylabel('Precipitation (mm)')
        plt.xlabel('Date')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
    except ImportError:
        print("\nNote: matplotlib not available for plotting")
        print("Install with: pip install matplotlib")


if __name__ == "__main__":
    main()
