import os
import requests

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
LAT = os.getenv("LAT")
LON = os.getenv("LON")

PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")

CAN_WORK_OUTSIDE_MESSAGE = "Yes, weather's beautiful."
CAN_MAYBE_WORK_OUTSIDE_MESSAGE = "Maybe, I recommend checking the weather."
CANNOT_WORK_OUTSIDE_MESSAGE = "No luck today."

def getWeather(): #TODO get weather data from openweather api

    weatherAPIURL = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&appid={API_KEY}"

    response = 0;
    try :
        response = requests.get(
            weatherAPIURL
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")
    
    data = response.json()

    weatherData = {
        "temp": data["current"]["temp"],
        "feels_like": data["current"]["feels_like"],
        "wind_speed": data["current"]["wind_speed"],
        "rain": data["current"].get("rain", {}).get("1h", 0),
        "clouds": data["current"]["clouds"]
    }
    
    return weatherData
# Determines whether it is suitable to work outside based on weather conditions.
#
# Rules:
#
# Temperature (°C):
# - Good:        15 to 28       → +2 points
# - Moderate:    10 to 15 or 28 to 32 → +1 point
# - Bad:         <10 or >32     → -2 points
#
# Wind (m/s):
# - Good:        < 6            → +1 point
# - Moderate:    6 to 10        → 0 points
# - Bad:         > 10           → -2 points
#
# Rain (mm per hour):
# - None:        0              → +2 points
# - Light:       < 1            → +1 point
# - Rainy:       ≥ 1            → -3 points
#
# Cloud coverage (%):
# - Light:       < 70%          → +1 point
# - Moderate:    70–90%         → 0 points
# - Heavy:       > 90%          → -1 point
#
# Final score:
# - Score ≥ 4   → 1 (YES, suitable to work outside)
# - Score ≥ 1   → 2 (MAYBE, check conditions manually)
# - Score < 1   → 0 (NO, not suitable to work outside)
#
# returns int
def canWorkOutside(data): 
   
    temp = data["temp"]
    wind = data["wind_speed"]
    rain = data["rain"]
    clouds = data["clouds"]

    score = 0

    # Temperatuur
    if 15 <= temp <= 28:
        score += 2
    elif 10 <= temp < 15 or 28 < temp <= 32:
        score += 1
    else:
        score -= 2

    # Wind
    if wind < 6:
        score += 1
    elif wind > 10:
        score -= 2

    # Regen
    if rain == 0:
        score += 2
    elif rain < 1:
        score += 1
    else:
        score -= 3

    # Bewolking
    if clouds < 70:
        score += 1
    elif clouds > 90:
        score -= 1

    # Eindbeslissing
    if score >= 4:
        return 1  # JA
    elif score >= 1:
        return 2  # MISSCHIEN
    else:
        return 0  # NEE
    
def sendNotification(message):
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER,
        "message": message
    })

def main():
    data = getWeather()
    result = canWorkOutside(data)

    if result == 1:
        sendNotification(CAN_WORK_OUTSIDE_MESSAGE)
    elif result == 2:
        sendNotification(CAN_MAYBE_WORK_OUTSIDE_MESSAGE)
    else:
        sendNotification(CANNOT_WORK_OUTSIDE_MESSAGE)

main()


 