import requests
import datetime
import webbrowser
import math
import sys

# API Configuration (Get a free API key from openweathermap.org)
WEATHER_API_KEY = "18cbda1582490139dac2b37b43dcd916"  # Replace with your actual key

def get_current_time():
    """Get the current time in AM/PM format"""
    return datetime.datetime.now().strftime("%I:%M %p")

def get_current_date():
    """Get the current date in weekday, Month day, Year format"""
    return datetime.datetime.now().strftime("%A, %B %d, %Y")

def get_weather(city):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] == 200:
            weather = data["weather"][0]["description"].title()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            return (f"🌤️ Weather in {city.title()}:\n"
                   f"- Condition: {weather}\n"
                   f"- Temperature: {temp}°C\n"
                   f"- Humidity: {humidity}%")
        else:
            return f"Couldn't find weather data for {city}"
    except Exception as e:
        return "Weather service unavailable. Please try again later."

def calculate(expression):
    """Perform basic mathematical calculations"""
    try:
        # Remove "calculate" or "what is" from the expression
        expr = expression.lower()
        expr = expr.replace("calculate", "").replace("what is", "").strip()
        
        # Validate the expression contains only numbers and operators
        valid_chars = set("0123456789+-*/.() ")
        if all(c in valid_chars for c in expr):
            result = eval(expr)
            return f"🧮 Result: {expr} = {result}"
        else:
            return "Please enter a valid math expression with numbers and + - * / operators"
    except:
        return "I couldn't calculate that. Please check your expression."

def search_web(query, engine="google"):
    """Perform web searches using specified search engine"""
    try:
        query = query.strip()
        if not query:
            return "Please specify what to search for"
            
        if engine == "google":
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"🔍 Googling: {query}"
        else:  # wikipedia
            webbrowser.open(f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}")
            return f"📚 Searching Wikipedia for: {query}"
    except:
        return "Couldn't perform search right now. Please try again."

def process_command(command):
    """Process and respond to user commands"""
    command = command.lower().strip()
    
    if not command:
        return "Please say something."
    
    if command in ['hi', 'hello', 'hey']:
        return "Hello! How can I assist you today?"
    
    elif command in ['bye', 'goodbye', 'exit']:
        return "Goodbye! Have a great day!"
    
    elif any(word in command for word in ['time', 'current time']):
        return f"⏰ Current time: {get_current_time()}"
    
    elif any(word in command for word in ['date', 'today', 'today\'s date']):
        return f"📅 Today is: {get_current_date()}"
    
    elif command.startswith('weather'):
        city = command.replace('weather', '').replace('in', '').strip()
        return get_weather(city) if city else "Please specify a city (e.g. 'weather in Tokyo')"
    
    elif command.startswith(('calculate', 'what is ')):
        return calculate(command)
    
    elif command.startswith('search google'):
        query = command.replace('search google', '').strip()
        return search_web(query, "google") if query else "Please specify search terms for Google"
    
    elif command.startswith('search wikipedia'):
        query = command.replace('search wikipedia', '').strip()
        return search_web(query, "wikipedia") if query else "Please specify search terms for Wikipedia"
    
    else:
        return "I didn't understand that. Try asking about:\n- Time/Date\n- Weather\n- Calculations\n- Web searches"

def main():
    print("\n" + "="*60)
    print(" SMART PERSONAL ASSISTANT ".center(60, "🌟"))
    print("="*60)
    print("\nI can help you with:")
    print("- Getting current time and date")
    print("- Checking weather for any city")
    print("- Doing calculations (+, -, *, /)")
    print("- Searching Google or Wikipedia")
    print("- Type 'bye' to exit\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
                
            response = process_command(user_input)
            print("Assistant:", response)
            
            if user_input.lower() in ['bye', 'goodbye', 'exit']:
                break
                
        except KeyboardInterrupt:
            print("\nAssistant: Goodbye!")
            break
        except Exception as e:
            print("Assistant: Sorry, something went wrong. Please try again.")

if __name__ == "__main__":
    # Check if weather API key is set
    if WEATHER_API_KEY == "your_api_key_here":
        print("⚠️ Warning: Please get a free API key from openweathermap.org")
        print("and replace 'your_api_key_here' in the code to use weather features.")
    
    main()
