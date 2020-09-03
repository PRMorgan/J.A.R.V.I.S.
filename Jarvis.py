### Jarvis recreation ###

"""
A simple recreation of the JARVIS system from the Iron Man comics and movies.
The inspiration came from a scene in Iron Man 2, where JARVIS woke tony up and
gave him a report of the weather.
So, this 'recreation" is really just an overcomplicated alarm clock that reads
off the weather from the OpenWeather API. Nothing too fancy... yet.

Author: Patrick Morgan
GitHub: PRMorgan
"""

from gtts import gTTS
from playsound import playsound
import datetime
import requests, json
import time

# API key for OpenWeather
api_key = "" #get your own, lil api thieves

# base_url variable to store url 
base_url = "http://api.openweathermap.org/data/2.5/weather?"
  
city_name = input("Enter your city name: ") #Prompt the user for the city for which they'd like weather data
complete_url = base_url + "appid=" + api_key + "&q=" + city_name #Reference OpenWeather
  
response = requests.get(complete_url) 

waitFlag = True #Flag to check if the correct time has been reached
correctTime = input("Enter desired time in HH:MM 24 hour format: ") #Prompt user for desired wake-up time
print("Waiting for " + correctTime)

while waitFlag: #Loop that checks whether or not the desired wake up time has been reached
    if (time.strftime("%H:%M") != correctTime): #If it's not time to wake up, go back to sleep for 10 seconds and try again
        print(time.strftime("%H:%M:%S")) #print the current time, with seconds, to show how much time is remaining
        print("not ready")
        time.sleep(10)
    else: #Correct wake up time has been reached
        print("correct time reached: " + correctTime)
        print("ready")
        waitFlag = False

        #Process weather data from OpenWeather API
        x = response.json()

        #if NOT 404 error (page not found)
        if x["cod"] != "404":
  
            y = x["main"]
            current_temperature = y["temp"] #Store temperature from OpenWeather API
            current_pressure = y["pressure"] #Store atmospheric pressure from OpenWeather API
            current_humidity = y["humidity"] #Store humidity from OpenWeather API
            z = x["weather"]
            weather_description = z[0]["description"] #Store sky conditions from OpenWeather API
        
            # print following values 
            print(" Temperature (in kelvin unit) = " +
                            str(current_temperature) + 
                "\n atmospheric pressure (in hPa unit) = " +
                            str(current_pressure) +
                "\n humidity (in percentage) = " +
                            str(current_humidity) +
                "\n description = " +
                            str(weather_description)) 
        else: 
            print(" City Not Found ") #If 404 error returned

        temp_f = ((current_temperature-273.15) * 9/5 + 32) #Convert temperature from Kelvin to Fahrenheit

        # The text that you want to convert to audio
        theTime = "It is " + str(time.strftime("%H:%M"))
        theTemp = "It is currently " + str(int(temp_f)) + " degrees outside."
        thePressure = "The atmospheric pressure is: " + str(current_pressure) + "hPa."
        theHumidity = "The humidity is at " + str(current_humidity) + " percent."
        theCondition = "Description: " + str(weather_description)

        # Language in which you want to convert
        language = 'en'
        
        print("Before Speak")

        # Pass the text and language to the engine,  
        # then save the file so it can be played back
        myobj = gTTS(text=theTime, lang=language, slow=False) #Pass to the engine
        myobj.save("theTime.mp3") #Save the file
        playsound("theTime.mp3") #Playback

        myobj = gTTS(text=theTemp, lang=language, slow=False)
        myobj.save("theTemp.mp3")
        playsound("theTemp.mp3")

        myobj = gTTS(text=thePressure, lang=language, slow=False)
        myobj.save("thePressure.mp3")
        playsound("thePressure.mp3")

        myobj = gTTS(text=theHumidity, lang=language, slow=False)
        myobj.save("theHumidity.mp3")
        playsound("theHumidity.mp3")

        myobj = gTTS(text=theCondition, lang=language, slow=False)
        myobj.save("theCondition.mp3")
        playsound("theCondition.mp3")

        print("After Speak")

print("Loop ended")
