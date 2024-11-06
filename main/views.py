from django.shortcuts import render
import json
import urllib.request

def index(request):
    data = {}
    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            try:
                # API call to OpenWeatherMap
                api_key = 'e4ec3e0bae5e50dddc2a661a9f123cc6'  # جایگزین کردن کلید API
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
                response = urllib.request.urlopen(url)
                source = response.read()
                
                # Parse JSON data
                list_of_data = json.loads(source)
                
                # Convert temperature from Kelvin to Celsius
                temp_kelvin = list_of_data['main']['temp']
                temp_celsius = round(temp_kelvin - 273.15, 2)
                
                # Data to pass to the template
                data = {
                    "country_code": list_of_data['sys'].get('country', 'N/A'),
                    "coordinate": f"{list_of_data['coord'].get('lon', 'N/A')} {list_of_data['coord'].get('lat', 'N/A')}",
                    "temp": f"{temp_celsius}°C",
                    "pressure": list_of_data['main'].get('pressure', 'N/A'),
                    "humidity": list_of_data['main'].get('humidity', 'N/A'),
                    "suggestion": get_clothing_suggestion(temp_celsius)
                }
            except urllib.error.HTTPError:
                data['error'] = "City not found. Please enter a valid city name."
            except Exception as e:
                data['error'] = f"An error occurred: {e}"
    return render(request, "index.html", data)

def get_clothing_suggestion(temp_celsius):
    """Return a clothing suggestion based on temperature in Celsius."""
    if temp_celsius <= 0:
        return "Brrr! It's freezing! Bundle up with a warm coat, hat, and gloves 🧥🧣🧤"
    elif temp_celsius <= 15:
        return "Chilly weather! Wear a jacket or sweater 🧥🍂"
    elif temp_celsius <= 25:
        return "Nice weather! A light outfit would be perfect 👕👖"
    else:
        return "It's warm! Stay cool with shorts and a T-shirt 🌞👕🩳"
