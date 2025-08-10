import requests
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

# Configuration
API_KEY = "f37cc4ce5484cee326635b86c1cf0db4"  
CITY = "Mumbai,IN"
UNITS = "metric"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data():
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": UNITS
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def create_dashboard(data):
    # Extract data with local timezone conversion
    main = data["main"]
    weather = data["weather"][0]
    wind = data["wind"]
    city = data["name"]
    
    # Fixed time conversion (using timezone-aware datetime)
    local_time = datetime.fromtimestamp(data["dt"], tz=timezone.utc)
    
    # visualization data
    metrics = {
        "Temperature": f"{main['temp']:.1f}°C",
        "Feels Like": f"{main['feels_like']:.1f}°C",
        "Humidity": f"{main['humidity']}%",
        "Pressure": f"{main['pressure']} hPa",
        "Wind Speed": f"{wind['speed']} m/s"
    }
    
    #figure with custom layout
    plt.figure(figsize=(14, 10))
    plt.suptitle(f"Mumbai Weather Dashboard | {local_time.strftime('%Y-%m-%d %H:%M')} IST", 
                 fontsize=20, fontweight="bold", color="#2c3e50")
    
    #grid layout
    gs = gridspec.GridSpec(3, 3, figure=plt.gcf(), height_ratios=[1, 1, 0.5])
    
    # Main weather panel
    ax1 = plt.subplot(gs[0, 0])
    ax1.set_title("Current Conditions", fontsize=14, pad=20)
    
    # Weather icon based on condition
    weather_icon = {
        "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", 
        "Thunderstorm": "⛈️", "Drizzle": "🌦️", "Snow": "❄️",
        "Mist": "🌫️", "Smoke": "💨", "Haze": "🌫️", 
        "Dust": "💨", "Fog": "🌫️", "Sand": "💨", 
        "Ash": "🌋", "Squall": "💨", "Tornado": "🌪️"
    }.get(weather["main"], "🌡️")
    
    ax1.text(0.5, 0.7, weather_icon, 
             fontsize=60, ha="center", va="center")
    ax1.text(0.5, 0.5, weather["description"].capitalize(), 
             fontsize=22, ha="center", va="center", color="#2980b9")
    ax1.text(0.5, 0.3, f"{main['temp']:.1f}°C", 
             fontsize=36, ha="center", va="center", color="#e74c3c")
    ax1.text(0.5, 0.1, f"Feels like: {main['feels_like']:.1f}°C", 
             fontsize=14, ha="center", va="center", color="#7f8c8d")
    ax1.axis("off")
    
    # Temperature gauge
    ax2 = plt.subplot(gs[0, 1])
    ax2.set_title("Temperature Range", fontsize=14)
    
    # Temperature range visualization
    temp_min = main["temp_min"]
    temp_max = main["temp_max"]
    current_temp = main["temp"]
    
    # temperature gauge
    ax2.barh(0.5, temp_max - temp_min, left=temp_min, height=0.3, color="#e0e0e0")
    ax2.barh(0.5, current_temp - temp_min, left=temp_min, height=0.3, color="#e74c3c")
    
    # current temperature indicator
    ax2.plot([current_temp, current_temp], [0.35, 0.65], color="#2c3e50", linewidth=3)
    
    #labels
    ax2.text(temp_min, 0.7, f"Min: {temp_min}°C", fontsize=10, ha="left")
    ax2.text(temp_max, 0.7, f"Max: {temp_max}°C", fontsize=10, ha="right")
    ax2.text(current_temp, 0.2, f"Current: {current_temp}°C", 
             fontsize=12, ha="center", fontweight="bold")
    
    ax2.set_xlim(temp_min - 2, temp_max + 2)
    ax2.set_ylim(0, 1)
    ax2.set_yticks([])
    ax2.grid(axis="x", alpha=0.3)
    
    # Humidity panel
    ax3 = plt.subplot(gs[0, 2])
    ax3.set_title("Humidity", fontsize=14)
    
    # Humidity gauge
    humidity = main["humidity"]
    ax3.bar(0, humidity, width=0.6, color="#3498db")
    ax3.bar(0, 100 - humidity, bottom=humidity, width=0.6, color="#ecf0f1")
    
    #percentage label
    ax3.text(0, humidity/2, f"{humidity}%", 
             fontsize=24, ha="center", va="center", color="white")
    ax3.text(0, humidity + (100-humidity)/2, "Dry", 
             fontsize=12, ha="center", va="center", color="#7f8c8d")
    
    ax3.set_xlim(-0.5, 0.5)
    ax3.set_ylim(0, 100)
    ax3.set_xticks([])
    ax3.grid(axis="y", alpha=0.3)
    
    # Metrics panel
    ax4 = plt.subplot(gs[1, :])
    ax4.set_title("Weather Metrics", fontsize=14)
    
    #metric cards
    card_height = 0.8
    card_width = 0.18
    spacing = 0.05
    colors = ["#3498db", "#2ecc71", "#9b59b6", "#e67e22", "#1abc9c"]
    
    for i, (key, value) in enumerate(metrics.items()):
        left = i * (card_width + spacing) + 0.05
        bottom = 0.1
        
        #card background
        rect = mpatches.Rectangle(
            (left, bottom), card_width, card_height,
            facecolor=colors[i], alpha=0.8,
            edgecolor="#34495e", linewidth=1.5
        )
        ax4.add_patch(rect)
        
        #metric text
        ax4.text(left + card_width/2, bottom + card_height - 0.15, key,
                fontsize=14, ha="center", va="center", color="white", fontweight="bold")
        ax4.text(left + card_width/2, bottom + card_height/2 - 0.1, value,
                fontsize=22, ha="center", va="center", color="white")
    
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis("off")
    
    # Wind panel
    ax5 = plt.subplot(gs[2, :], projection='polar')
    ax5.set_title("Wind Direction", fontsize=14)
    
    # Converted wind direction to radians
    wind_dir = wind.get("deg", 0)
    wind_rad = wind_dir * (3.14159/180)
    
    # Plot wind direction
    ax5.plot([0, wind_rad], [0, wind["speed"]], 
             marker='o', color='#e74c3c', linewidth=2)
    
    # compass labels
    ax5.set_thetagrids(range(0, 360, 45), 
                      labels=["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
    
    #wind speed label
    ax5.text(wind_rad, wind["speed"] + 0.5, f"{wind['speed']} m/s",
            fontsize=12, ha="center", va="bottom")
    
    #direction label
    ax5.text(0, 0, f"{wind_dir}°", 
            fontsize=14, ha="center", va="center", bbox=dict(facecolor='white', alpha=0.8))
    
    # Final layout
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.subplots_adjust(top=0.92, hspace=0.3)
    plt.savefig("mumbai_weather_dashboard.png", dpi=120, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    try:
        print("Fetching Mumbai weather data...")
        weather_data = get_weather_data()
        print("Data fetched successfully!")
        create_dashboard(weather_data)
        print("Dashboard created: 'mumbai_weather_dashboard.png'")
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
    except KeyError as e:
        print(f"Data Parsing Error: {str(e)} - Check API response structure")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")