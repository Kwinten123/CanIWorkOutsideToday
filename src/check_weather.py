import os
import requests

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
LAT = os.getenv("LAT")
LON = os.getenv("LON")

PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")

CAN_WORK_OUTSIDE_MESSAGE = "Yes, weather's beautiful"
CANNOT_WORK_OUTSIDE_MESSAGE = "No luck today."

def getWeather(): #TODO get weather data from openweather api
    return "bad weather data"

def canWorkOutside(data):#TODO write logic for being able to work outside or not
    return False # weathers terrible today. 

def sendNotification(message):
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER,
        "message": message
    })

def main():
    data = getWeather()

    if canWorkOutside(data):
        sendNotification(CAN_WORK_OUTSIDE_MESSAGE)
    else :
        sendNotification(CANNOT_WORK_OUTSIDE_MESSAGE)

main()


 